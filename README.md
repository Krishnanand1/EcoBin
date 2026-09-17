# EcoBin

EcoBin is a Flask web application that classifies a photo of a waste item into one of six material categories: cardboard, glass, metal, paper, plastic, or trash.

Upload a clear JPG or PNG image to receive the most likely category, its confidence score, and two alternative predictions.

## Features

- Drag-and-drop or file-picker image upload
- PNG and JPEG support, with file-content validation
- 8 MB upload limit and unique upload filenames
- Classification confidence and alternative predictions
- Clear feedback for invalid files, unavailable models, and low-confidence results
- Responsive interface with an image preview

## Technology

- Python 3.10–3.12
- Flask
- TensorFlow / Keras
- Pillow and NumPy

## Model

The application uses a Keras model located at:

```text
models/waste_classification_model.keras
```

The currently installed model accepts RGB images at **224 × 224 pixels** and produces six output probabilities. The application detects the model's required input size automatically before prediction.

The output labels are mapped in this order:

```text
cardboard, glass, metal, paper, plastic, trash
```

To use a different compatible model, set `WASTE_MODEL_PATH` to its absolute path. The model must output six probabilities in the same label order.

## Project structure

```text
EcoBin/
├── app.py                         # Flask routes and upload validation
├── utils.py                       # Model loading and prediction utilities
├── requirements.txt               # Python dependencies
├── models/
│   └── waste_classification_model.keras
├── static/
│   ├── css/style.css              # Application styles
│   └── uploads/                   # Uploaded images (not committed)
├── templates/
│   ├── index.html                 # Upload page
│   └── result.html                # Prediction result page
└── WASTE_MANAGEMENT.ipynb         # Original training notebook
```

## Run locally

The project includes an isolated virtual environment at `.venv`. From the project folder, run:

```powershell
.\.venv\Scripts\python.exe app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

If you need to create the environment again, use Python 3.10–3.12 and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Use the application

1. Open the local address in a browser.
2. Upload one clear image containing a waste item.
3. Select **Classify image**.
4. Review the predicted material, confidence, and alternative possibilities.
5. Follow your local recycling rules before disposal.

## Configuration

Optional environment variables:

```text
WASTE_MODEL_PATH=C:\absolute\path\to\another-model.keras
FLASK_DEBUG=1
```

`FLASK_DEBUG` should be used only during local development.

## Notes

- Model files are intentionally excluded from Git because they are large binary assets.
- Uploaded images are stored under `static/uploads/`; do not use this default setup for sensitive images.
- The included training notebook contains historical training material and does not describe the currently installed VGG19-based model.

## Run

 - .\.venv\Scripts\python.exe app.py