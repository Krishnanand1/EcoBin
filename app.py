import os
import uuid
from pathlib import Path

from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from utils import ModelUnavailableError, predict_waste_category

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config.update(UPLOAD_FOLDER=str(UPLOAD_FOLDER), MAX_CONTENT_LENGTH=8 * 1024 * 1024)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_image(file_storage):
    try:
        image = Image.open(file_storage.stream)
        image.verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False
    finally:
        file_storage.stream.seek(0)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("file")
    if not file or not file.filename:
        return render_template("index.html", error="Choose an image before classifying."), 400
    if not allowed_file(file.filename):
        return render_template("index.html", error="Use a PNG, JPG, or JPEG image."), 400
    if not valid_image(file):
        return render_template("index.html", error="That file is not a valid image."), 400

    extension = Path(secure_filename(file.filename)).suffix.lower()
    filename = f"{uuid.uuid4().hex}{extension}"
    image_path = UPLOAD_FOLDER / filename
    file.save(image_path)
    try:
        prediction = predict_waste_category(image_path)
    except ModelUnavailableError as error:
        image_path.unlink(missing_ok=True)
        return render_template("index.html", error=str(error)), 503
    except Exception:
        app.logger.exception("Prediction failed")
        image_path.unlink(missing_ok=True)
        return render_template("index.html", error="We could not classify that image. Please try another one."), 500

    return render_template("result.html", image_url=f"uploads/{filename}", prediction=prediction)


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(_error):
    return render_template("index.html", error="Image is too large. Choose a file smaller than 8 MB."), 413


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
