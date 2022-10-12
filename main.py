from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
from crypto import crypto, check_key
from flask_login import current_user

app = Flask(__name__)

upload_path = "./files"
max_size = 2 * 1024 * 1024

# set the upload path
app.config["UPLOAD_FOLDER"] = upload_path
# set the maximum size for uploaded files
app.config["MAX_CONTENT_LENGTH"] = max_size

if not os.path.exists(upload_path):
    os.mkdir(upload_path)


@app.route("/", methods=["POST", "GET"])
def index(signin=False, encrypted_file=None, error=None):
    if request.method == "POST":
        return render_template("index.html", signin=signin, file="ok", error_message=error)
    return render_template("index.html", signin=signin, file=encrypted_file, error_message=error)


@app.route("/log_out")
def log_out():
    return redirect(url_for("index", signin=False))


@app.route("/sign_in", methods=["POST", "GET"])
def sign_in_page():
    if request.method == "POST":
        idt = request.form["id"]
        pw = request.form["pw"]
        print(True)
        return redirect(url_for("index", signin=True))

    return render_template("sign-in.html")


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        idt = request.form["id"]
        pw = request.form["pw"]
        print(idt, pw)
        return redirect(url_for("index", signin=True))

    return render_template("sign-up.html")


@app.route("/information_page")
def info_page():
    return render_template("information-page.html")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    global encrypted_file_name
    if request.method == "POST":
        key = request.form["key"]
        method = request.form["method"]

        if not check_key(method, key):
            return redirect(url_for("index", error="keyError"))

        action = request.form["action"]
        file = request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))

        encrypted_file_name = "encrypted_" if action == "encrypt" else "decrypted"
        encrypted_file_name += file.filename

        crypto(action, method, key, file.filename, app.config["UPLOAD_FOLDER"] + '/')

        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))

    return redirect(url_for("index"))


@app.route("/download")
def download():
    global encrypted_file_name
    return send_file(app.config["UPLOAD_FOLDER"]+'/'+encrypted_file_name, as_attachment=True)


if __name__ == "__main__":
    encrypted_file_name = ""
    app.run(debug=True)
