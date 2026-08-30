# Author: Junior

import json
from pathlib import Path

import cv2
import numpy as np
import pytest
from tensorflow import keras
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# =========================================================
# TEST DATASET
# =========================================================

TEST_DIR = (
    PROJECT_ROOT
    / "tests"
    / "dataset"
)


# =========================================================
# MODEL
# =========================================================

MODEL_PATH = (
    PROJECT_ROOT
    / "cnn"
    / "models"
    / "color_cnn.keras"
)


# =========================================================
# CLASS MAPPING
# =========================================================

MAPPING_PATH = (
    PROJECT_ROOT
    / "cnn"
    / "models"
    / "class_mapping.json"
)


# =========================================================
# ACTUAL LABELS
# =========================================================

LABELS_PATH = (
    TEST_DIR
    / "test_labels.json"
)


# =========================================================
# IMAGE SETTINGS
# =========================================================

IMAGE_SIZE = 128

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# =========================================================
# LOAD COLOR MAPPING
# =========================================================

def load_color_mapping():

    assert MAPPING_PATH.exists(), (
        f"\nColor mapping not found:\n"
        f"{MAPPING_PATH}"
    )

    with open(
        MAPPING_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    assert "color" in mapping, (
        "\nclass_mapping.json does not contain "
        "'color' mapping."
    )

    color_mapping = {
        int(key): value.upper()
        for key, value
        in mapping["color"].items()
    }

    return color_mapping


# =========================================================
# LOAD ACTUAL LABELS
# =========================================================

def load_actual_labels():

    assert LABELS_PATH.exists(), (
        f"\nTest labels not found:\n"
        f"{LABELS_PATH}\n\n"
        f"Please create this file."
    )

    with open(
        LABELS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        labels = json.load(file)

    return {
        filename: color.upper()
        for filename, color
        in labels.items()
    }


# =========================================================
# PREPARE IMAGE
# =========================================================

def prepare_image(image):

    if image is None:
        raise ValueError(
            "Image is empty."
        )

    # OpenCV BGR -> RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Resize
    image = cv2.resize(
        image,
        (
            IMAGE_SIZE,
            IMAGE_SIZE
        )
    )

    # float32
    image = image.astype(
        np.float32
    )

    # Normalize
    image /= 255.0

    # Add batch dimension
    image = np.expand_dims(
        image,
        axis=0
    )

    return image


# =========================================================
# PREDICT COLOR
# =========================================================

def predict_color(
    model,
    color_mapping,
    image_path
):

    # Read image
    image = cv2.imread(
        str(image_path)
    )

    if image is None:
        raise ValueError(
            f"Cannot read image:\n"
            f"{image_path}"
        )

    # Prepare image
    processed = prepare_image(
        image
    )

    # Predict
    probabilities = model.predict(
        processed,
        verbose=0
    )[0]

    # Get highest probability
    color_id = int(
        np.argmax(
            probabilities
        )
    )

    # Convert class ID to color
    predicted_color = color_mapping.get(
        color_id,
        f"UNKNOWN_{color_id}"
    )

    # Highest probability = confidence
    confidence_score = float(
        probabilities[color_id]
    )

    return (
        predicted_color,
        confidence_score
    )


# =========================================================
# PYTEST FIXTURE - MODEL
# =========================================================

@pytest.fixture(
    scope="module"
)
def color_model():

    assert MODEL_PATH.exists(), (
        f"\nColor CNN model not found:\n"
        f"{MODEL_PATH}"
    )

    print()
    print("Loading Color CNN...")

    model = keras.models.load_model(
        MODEL_PATH
    )

    print("Color CNN loaded successfully.")

    return model


# =========================================================
# PYTEST FIXTURE - COLOR MAPPING
# =========================================================

@pytest.fixture(
    scope="module"
)
def color_mapping():

    return load_color_mapping()


# =========================================================
# PYTEST FIXTURE - ACTUAL LABELS
# =========================================================

@pytest.fixture(
    scope="module"
)
def actual_labels():

    return load_actual_labels()


# =========================================================
# PYTEST FIXTURE - TEST IMAGES
# =========================================================

@pytest.fixture(
    scope="module"
)
def test_images():

    assert TEST_DIR.exists(), (
        f"\nTest dataset directory not found:\n"
        f"{TEST_DIR}"
    )

    images = sorted(
        [
            file
            for file in TEST_DIR.iterdir()
            if file.is_file()
            and file.suffix.lower()
            in IMAGE_EXTENSIONS
        ],
        key=lambda path: path.name
    )

    assert images, (
        f"\nNo test images found in:\n"
        f"{TEST_DIR}"
    )

    return images


# =========================================================
# COLOR CNN TEST
# =========================================================

def test_color_predictions(
    color_model,
    color_mapping,
    actual_labels,
    test_images
):

    # Actual values
    y_true = []

    # Predicted values
    y_pred = []

    # =====================================================
    # HEADER
    # =====================================================

    print()
    print()
    print("=" * 100)
    print(
        "                    COLOR CNN TEST RESULTS"
    )
    print("=" * 100)

    print()

    print(
        f"Test Directory : {TEST_DIR}"
    )

    print(
        f"Model          : {MODEL_PATH}"
    )

    print(
        f"Test Images    : {len(test_images)}"
    )

    print()

    # =====================================================
    # TEST EACH IMAGE
    # =====================================================

    for image_path in test_images:

        # -------------------------------------------------
        # Predict color
        # -------------------------------------------------

        predicted_color, confidence_score = (
            predict_color(
                color_model,
                color_mapping,
                image_path
            )
        )

        # -------------------------------------------------
        # Get actual color
        # -------------------------------------------------

        actual_color = actual_labels.get(
            image_path.name
        )

        if actual_color is None:

            pytest.fail(
                f"\nMissing actual color label for:\n"
                f"{image_path.name}\n\n"
                f"Add this filename to:\n"
                f"{LABELS_PATH}"
            )

        actual_color = actual_color.upper()

        # -------------------------------------------------
        # Store values
        # -------------------------------------------------

        y_true.append(
            actual_color
        )

        y_pred.append(
            predicted_color
        )

        # -------------------------------------------------
        # Per-image accuracy
        # -------------------------------------------------

        if predicted_color == actual_color:

            image_accuracy = 1.0

            result = "PASS"

        else:

            image_accuracy = 0.0

            result = "FAIL"

        # =================================================
        # IMAGE RESULT
        # =================================================

        print(
            f"Test:              {image_path.name}"
        )

        print(
            f"Actual Color:      {actual_color}"
        )

        print(
            f"Predicted Color:   {predicted_color}"
        )

        print(
            f"Accuracy Score:    "
            f"{image_accuracy:.4f}"
        )

        print(
            f"Confidence Score:  "
            f"{confidence_score:.4f} "
            f"({confidence_score * 100:.2f}%)"
        )

        print(
            f"Result:             {result}"
        )

        print(
            "-" * 100
        )

    # =====================================================
    # CALCULATE METRICS
    # =====================================================

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    labels = sorted(
        set(y_true) | set(y_pred)
    )

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=labels
    )

    # =====================================================
    # CORRECT / INCORRECT
    # =====================================================

    correct_predictions = sum(
        actual == predicted
        for actual, predicted
        in zip(
            y_true,
            y_pred
        )
    )

    incorrect_predictions = sum(
        actual != predicted
        for actual, predicted
        in zip(
            y_true,
            y_pred
        )
    )

    # =====================================================
    # OVERALL METRICS
    # =====================================================

    print()
    print()
    print("=" * 100)
    print(
        "                         MODEL EVALUATION"
    )
    print("=" * 100)

    print()

    print(
        f"Accuracy:    {accuracy:.4f} "
        f"({accuracy * 100:.2f}%)"
    )

    print(
        f"Precision:   {precision:.4f} "
        f"({precision * 100:.2f}%)"
    )

    print(
        f"Recall:      {recall:.4f} "
        f"({recall * 100:.2f}%)"
    )

    print(
        f"F1-score:    {f1:.4f} "
        f"({f1 * 100:.2f}%)"
    )

    print()

    print(
        f"Total Images:           {len(y_true)}"
    )

    print(
        f"Correct Predictions:    "
        f"{correct_predictions}"
    )

    print(
        f"Incorrect Predictions:  "
        f"{incorrect_predictions}"
    )

    # =====================================================
    # CLASSIFICATION REPORT
    # =====================================================

    print()
    print("=" * 100)
    print(
        "                    CLASSIFICATION REPORT"
    )
    print("=" * 100)

    print()

    report = classification_report(
        y_true,
        y_pred,
        labels=labels,
        zero_division=0
    )

    print(report)

    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    print("=" * 100)
    print(
        "                       CONFUSION MATRIX"
    )
    print("=" * 100)

    print()

    # -----------------------------------------------------
    # Matrix header
    # -----------------------------------------------------

    print(
        f"{'Actual / Predicted':<20}",
        end=""
    )

    for label in labels:

        print(
            f"{label[:10]:>12}",
            end=""
        )

    print()

    print(
        "-" * (
            20 +
            (12 * len(labels))
        )
    )

    # -----------------------------------------------------
    # Matrix rows
    # -----------------------------------------------------

    for row_index, actual_label in enumerate(labels):

        print(
            f"{actual_label:<20}",
            end=""
        )

        for column_index in range(
            len(labels)
        ):

            print(
                f"{cm[row_index][column_index]:>12}",
                end=""
            )

        print()

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    print()
    print("=" * 100)
    print(
        "                         FINAL SUMMARY"
    )
    print("=" * 100)

    print()

    print(
        f"Accuracy:    {accuracy:.4f}"
        f"  ({accuracy * 100:.2f}%)"
    )

    print(
        f"Precision:   {precision:.4f}"
        f"  ({precision * 100:.2f}%)"
    )

    print(
        f"Recall:      {recall:.4f}"
        f"  ({recall * 100:.2f}%)"
    )

    print(
        f"F1-score:    {f1:.4f}"
        f"  ({f1 * 100:.2f}%)"
    )

    print()

    print(
        f"Correct:     "
        f"{correct_predictions}/{len(y_true)}"
    )

    print(
        f"Incorrect:   "
        f"{incorrect_predictions}/{len(y_true)}"
    )

    print()

    print("=" * 100)
    print(
        "                         TEST COMPLETE"
    )
    print("=" * 100)

    print()

    # The test succeeds when all images were evaluated.
    # The metrics themselves are reported above.
    assert len(y_true) == len(test_images)


# =========================================================
# BASIC MODEL TEST
# =========================================================

def test_color_model_output(
    color_model,
    color_mapping,
    test_images
):

    predicted_color, confidence_score = (
        predict_color(
            color_model,
            color_mapping,
            test_images[0]
        )
    )

    # Prediction must be a valid color
    assert predicted_color in (
        color_mapping.values()
    )

    # Confidence must be between 0 and 1
    assert (
        0.0 <= confidence_score <= 1.0
    )