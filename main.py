# Flask documentation: https://flask.palletsprojects.com/en/latest/
from __future__ import annotations

try:
    from flask import Flask, render_template, request, redirect, url_for, send_file, session
    from werkzeug.utils import secure_filename
    import os
    from crypto import crypto, check_key
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    raise ImportError("Please install the needed libraries, "
                      "consult https://github.com/maxcap12/BSP1-online-encryption/blob/main/requirements.txt")


# initialisation of the app
app = Flask(__name__)

# define the path to save the uploaded files
upload_path = "temp_files"
# define the maximum size for uploaded files
max_size = 2 * 1024 * 1024

# set the upload path
app.config["UPLOAD_FOLDER"] = upload_path
# set the maximum size for uploaded files
app.config["MAX_CONTENT_LENGTH"] = max_size

# secret key of the app (should hide it in the final version)
app.secret_key = "f360afc809f0e2eeff15da041d703ff7eef519a5257e79d996c3b9e2bb59082c"
# disable the permanent session
app.config["Session_permanent"] = False

# create the folder to save the uploaded files if it doesn't exist
if not os.path.exists(upload_path):
    os.mkdir(upload_path)

# Set up of the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    """
    Object representing a row of the users’ table to store user accounts information
    """
    # column for the primary key
    _id = db.Column("id", db.Integer, primary_key=True)
    # column to store the username
    idt = db.Column(db.String(120), unique=True, nullable=False)
    # column to store the password
    pw = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, idt, pw):
        self.idt = idt
        self.pw = pw


class Keys(db.Model):
    """
    Object representing a column of the keys' table to store the keys saved by the users
    """
    # column for the primary key
    _id = db.Column("id", db.Integer, primary_key=True)
    # column to store the username
    user = db.Column(db.String(120), unique=False, nullable=False)
    # column to store the description of the key
    key_name = db.Column(db.String(120), unique=False, nullable=False)
    # column to store the key
    key = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, user, key_name, key):
        self.user = user
        self.key_name = key_name
        self.key = key


@app.route("/")
def index() -> str:
    """
    display the index page of the website
    :return: index page
    """
    # initialise the variables
    error = []
    filled = False
    saved_keys = {}

    if "error" in session:
        # get the error if any
        error = session["error"]
        # reset the error field of the session
        session.pop("error")

    if "filled" in session:
        # check if the form has already been filled
        filled = session["filled"]
        # reset the field
        session.pop("filled")

    if "dont_ask" not in session:
        # check if the user clicked on the stop asking button
        session["dont_ask"] = False

    # check if we are supposed to show the popup or not
    show_popup = False if "show_popup" not in session else session["show_popup"]
    # reset the field
    session["show_popup"] = False

    # check if the user is logged in
    if "idt" in session:
        # get all the keys saved by the user
        saved_keys = key_query(session["idt"])

    sess = session

    return render_template("index.html", error_messages=error, is_filled=filled, session=sess, keys=saved_keys, show=show_popup)


@app.route("/log_out")
def log_out() -> Response:
    """
    log out the user
    :return: index page
    """
    # log out the user
    session.clear()
    return redirect(url_for("index"))


@app.route("/sign_in", methods=["POST", "GET"])
def sign_in_page() -> str | Response:
    """
    display the sign-in page and connect the user if the username and the password are correct
    :return: index page if the user signed-in successfully, sign-in page if not
    """
    # check if the user posted information
    if request.method == "POST":
        # get the username
        idt = request.form["id"]
        # get the password
        pw = request.form["pw"]
        hash_pw = hash(pw)

        # check if the username and the password are valid
        if Users.query.filter_by(idt=idt, pw=hash_pw).first():
            # save the username in the session
            session["idt"] = idt
            return redirect(url_for("index"))

        else:
            return render_template("sign-in.html", error=True)

    return render_template("sign-in.html", error=False)


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up() -> str | Response:
    """
    display the sign-up page and create an account if the username and the password are correct
    :return: index page if the user signed-up successfully, sign-in page if not
    """
    # check if the user posted information
    if request.method == "POST":
        # get the username
        idt = request.form["id"]
        # get the password
        pw = request.form["pw"]

        # check if the username is not already used by another account
        if Users.query.filter_by(idt=idt).first():
            return render_template("sign-up.html", error=True)

        else:
            # hash the password
            hash_pw = hash(pw)
            # create the column
            new_user = Users(idt, hash_pw)
            # place the column in the users table
            db.session.add(new_user)
            # save the database
            db.session.commit()
            # save the username in the session
            session["idt"] = idt
            return redirect(url_for("index"))

    return render_template("sign-up.html", error=False)


@app.route("/information_page")
def info_page() -> str:
    """
    display the information page
    :return: information page
    """
    return render_template("information-page.html")


@app.route("/upload", methods=["POST", "GET"])
def upload() -> Response:
    """
    encrypt or decrypt the file selected by the user with the algorithm and key of its choice
    :return: index page
    """
    # get access to the global variable new_file_name
    global new_file_name

    # check if the user posted information
    if request.method == "POST":
        session["filled"] = True
        # get the key from the type key input
        key = request.form["key"]
        # check if the user is logged in
        if "idt" in session:
            session["show_popup"] = True

        # check if the variable is an empty string
        if not key:
            # if it is, get the value of the select key input
            key = request.form["saved-key"]
            # the user has selected a key which is already saved, so the popup doesn't appear
            session["show_popup"] = False

        # save the last key in the session in case the user wants to save it
        session["last_key"] = key
        # get the encryption method
        method = request.form["method"]

        # check if the key is valid
        if not check_key(method, key):
            session["error"] = "keyError"
            # if it's not, the user is back on the index page with an error message
            return redirect(url_for("index"))

        # get the action (encrypt or decrypt)
        action = request.form["action"]
        # get the file
        file = request.files["file"]
        # download the file in the local folder
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))

        # save the path to the new file in the global variable
        # the first part of the name of the new file is encrypted or decrypted depends on the action selected
        new_file_name = "encrypted_" if action == "encrypt" else "decrypted_"
        # the second part is the name of the original file
        new_file_name += secure_filename(file.filename)

        # create a new file containing the original file encrypted/decrypted
        crypto(action, method, key, secure_filename(file.filename), new_file_name, app.config["UPLOAD_FOLDER"] + '/')

        # delete the orignal file from the server
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))

    return redirect(url_for("index"))


@app.route("/download")
def download() -> Responce:
    """
    download the encrypted/decrypted version of the file that he uploaded before
    :return: download the file
    """
    # get access to the global variable new_file_name
    global new_file_name

    if not new_file_name:
        # if the variable file name is empty the user is redirected to the main page
        return redirect(url_for("index"))

    # variable containing the new file downloader
    download_file = send_file(app.config["UPLOAD_FOLDER"] + '/' + new_file_name, as_attachment=True)
    # delete the ew file from the server
    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], new_file_name))
    # download the new file on the user's device
    return download_file


@app.route("/add-key", methods=["POST", "GET"])
def add_key() -> Response:
    """
    called when the user press the "save" button on the popup
    :return: index page
    """
    # get the value of the input field, if it is empty, assign a default name to the key
    key_name = request.form["key-name"] if request.form["key-name"] != '' else "key " + session["last_key"]
    # call the function to save the key in the database
    save_key(session["idt"], key_name, session["last_key"])
    session["filled"] = True
    return redirect(url_for("index"))


@app.route("/dont-save", methods=["POST", "GET"])
def dont_save() -> Response:
    """
    called when the user press the "don't save" button on the popup
    :return: index page
    """
    # delete the key from the session
    session.pop("last_key")
    session["filled"] = True
    return redirect(url_for("index"))


@app.route("/stop-ask")
def stop_ask() -> Response:
    """
    called when the user press the "stop asking" button on the popup
    :return: index page
    """
    # delete the key from the session
    session.pop("last_key")
    # now the popup is no longer shown
    session["dont_ask"] = True
    session["filled"] = True
    return redirect(url_for("index"))


def key_query(username: str) -> list:
    """
    get all the key saved by a user
    :param username: name of the account of the user
    :return: a list of lists containing the description of the key and its value
    """
    # get all keys saved by the user
    data = Keys.query.filter_by(user=username).all()
    return [[element.key_name, element.key] for element in data]


def save_key(username: str, key_name: str, key: str) -> None:
    """
    save a key in the database
    :param username: name of the account of the user
    :param key_name: name of the key
    :param key: value of the key
    :return: None
    """
    # create the key object
    new_key = Keys(username, key_name, key)
    # add the object to the database
    db.session.add(new_key)
    db.session.commit()


if __name__ == "__main__":
    # creation of the variable containing the new file name
    new_file_name = ""
    # create the database
    db.create_all()
    # run the app
    app.run()
