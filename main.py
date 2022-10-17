from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from werkzeug.utils import secure_filename
import os
from crypto import crypto, check_key
from flask_login import current_user

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

app.secret_key = "TEST"

app.config["Session_permanent"] = False

# create the folder to save the uploaded files if it doesn't exist
if not os.path.exists(upload_path):
    os.mkdir(upload_path)


@app.route("/")
def index() -> str:
    """
    display the index page of the website
    :return: index page
    """
    error = []
    filled = False
    if "error" in session:
        error = session["error"]
        session.pop("error")

    if "filled" in session:
        filled = session["filled"]
        session.pop("filled")

    print(filled)
    return render_template("index.html", error_messages=error, is_filled=filled)


@app.route("/log_out")
def log_out() -> Response:
    """
    log out the user
    :return: index page
    """
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
        return redirect(url_for("index"))

    return render_template("sign-in.html")


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
        return redirect(url_for("index"))

    return render_template("sign-up.html")


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
        # get the key
        key = request.form["key"]
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
        # download the file on the server
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
    # download the new file on the client's device
    return download_file


if __name__ == "__main__":
    # creation of the variable containing the new file name
    new_file_name = ""
    # run the app
    app.run(debug=True)
