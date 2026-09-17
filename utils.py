import numpy as np
from PIL import Image
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
configured_path = os.getenv("WASTE_MODEL_PATH")
MODEL_PATH = Path(configured_path) if configured_path else (
    MODELS_DIR / "waste_classification_model.keras"
    if (MODELS_DIR / "waste_classification_model.keras").is_file()
    else MODELS_DIR / "waste_classification_model.h5"
)
model = None

# Categories mapping
CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

class ModelUnavailableError(RuntimeError):
    pass


def get_model():
    global model
    if model is not None:
        return model
    if not MODEL_PATH.is_file():
        raise ModelUnavailableError("The trained model is missing. Put a compatible .keras or .h5 model in the models folder or set WASTE_MODEL_PATH to its location.")
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except ImportError as error:
        raise ModelUnavailableError("TensorFlow is not installed. Run: pip install -r requirements.txt") from error
    except Exception as error:
        raise ModelUnavailableError("The trained model could not be loaded. Check that it is a compatible Keras .h5 model.") from error


def preprocess_image(image_path, target_size):
    """Preprocess an RGB image to match the model's declared input size."""
    with Image.open(image_path) as image:
        img = image.convert("RGB").resize(target_size)
        img_array = np.asarray(img, dtype=np.float32)
    return np.expand_dims(img_array / 255.0, axis=0)

def predict_waste_category(image_path):
    """Predict the waste category for a given image."""
    loaded_model = get_model()
    height, width = loaded_model.input_shape[1:3]
    if not height or not width:
        raise ModelUnavailableError("The model must declare a fixed image width and height.")
    processed_image = preprocess_image(image_path, (width, height))
    predictions = loaded_model.predict(processed_image, verbose=0)
    predicted_class = np.argmax(predictions[0])
    
    top_indices = np.argsort(predictions[0])[::-1][:3]
    top_predictions = [{"category": CATEGORIES[index], "confidence": round(float(predictions[0][index]) * 100, 1)} for index in top_indices]
    return {"category": CATEGORIES[predicted_class], "confidence": top_predictions[0]["confidence"], "alternatives": top_predictions[1:]}
