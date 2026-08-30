# Author: Junior
# ============================================================
# IMPORTS
# ============================================================

import os
import json
import random
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

IMG_SIZE = 128
BATCH_SIZE = 32

BASE_DIR = Path(__file__).resolve().parent

TRAIN_DIR = BASE_DIR / "dataset" / "train"
CSV_PATH = BASE_DIR / "dataset" / "labels.csv"

OUTPUT_DIR = BASE_DIR / "cnn"

MODEL_DIR = OUTPUT_DIR / "models"
REPORT_DIR = OUTPUT_DIR / "reports"
PLOT_DIR = OUTPUT_DIR / "plots"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("SMARTCART CUSTOM CNN IMAGE SEARCH")
print("=" * 70)
print("BASE_DIR :", BASE_DIR)
print("TRAIN_DIR:", TRAIN_DIR)
print("CSV_PATH :", CSV_PATH)


# ============================================================
# CELL 2 — LOAD CSV AND ALIGN IMAGES
# ============================================================

labels_df = pd.read_csv(CSV_PATH)

print("=" * 70)
print("CSV")
print("=" * 70)

print(labels_df.head())
print()
print("Rows:", len(labels_df))
print()
print(labels_df.columns.tolist())

required_columns = [
    "filename",
    "gender",
    "color",
    "category"
]

missing_columns = [
    c for c in required_columns
    if c not in labels_df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing CSV columns: {missing_columns}"
    )

labels_df["filename"] = (
    labels_df["filename"]
    .astype(str)
    .str.strip()
)

labels_df["gender"] = (
    labels_df["gender"]
    .astype(str)
    .str.strip()
    .str.lower()
)

labels_df["color"] = (
    labels_df["color"]
    .astype(str)
    .str.strip()
    .str.lower()
)

labels_df["category"] = (
    labels_df["category"]
    .astype(str)
    .str.strip()
    .str.lower()
)

labels_df["image_path"] = labels_df["filename"].apply(
    lambda x: str(TRAIN_DIR / x)
)

labels_df["exists"] = labels_df["image_path"].apply(
    os.path.exists
)

missing_images = labels_df[~labels_df["exists"]]

print()
print("Missing images:", len(missing_images))

if len(missing_images):
    print(missing_images[["filename", "image_path"]].head(20))

labels_df = labels_df[
    labels_df["exists"]
].copy()

labels_df = labels_df.reset_index(drop=True)

print()
print("Aligned images:", len(labels_df))



# ============================================================
# CELL 3 — LABEL MAPPINGS
# ============================================================

GENDERS = [
    "men",
    "women"
]

CATEGORIES = [
    "shirt",
    "pant",
    "shoe"
]

COLORS = [
    "black",
    "blue",
    "brown",
    "gray",
    "green",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow"
]

gender_to_id = {
    value: index
    for index, value in enumerate(GENDERS)
}

category_to_id = {
    value: index
    for index, value in enumerate(CATEGORIES)
}

color_to_id = {
    value: index
    for index, value in enumerate(COLORS)
}

id_to_gender = {
    index: value
    for index, value in enumerate(GENDERS)
}

id_to_category = {
    index: value
    for index, value in enumerate(CATEGORIES)
}

id_to_color = {
    index: value
    for index, value in enumerate(COLORS)
}

labels_df["gender_id"] = labels_df["gender"].map(
    gender_to_id
)

labels_df["category_id"] = labels_df["category"].map(
    category_to_id
)

labels_df["color_id"] = labels_df["color"].map(
    color_to_id
)

bad_labels = labels_df[
    labels_df[
        ["gender_id", "category_id", "color_id"]
    ].isna().any(axis=1)
]

if len(bad_labels):
    print("Invalid labels:")
    print(
        bad_labels[
            [
                "filename",
                "gender",
                "color",
                "category"
            ]
        ].to_string(index=False)
    )
    raise ValueError(
        "CSV contains labels outside the supported classes."
    )

labels_df["gender_id"] = labels_df["gender_id"].astype(int)
labels_df["category_id"] = labels_df["category_id"].astype(int)
labels_df["color_id"] = labels_df["color_id"].astype(int)

print("Gender mapping :", gender_to_id)
print("Category mapping:", category_to_id)
print("Color mapping   :", color_to_id)

# ============================================================
# CELL 4 — DATASET CHECK
# ============================================================

print("=" * 70)
print("DATASET DISTRIBUTION")
print("=" * 70)

print("\nGender:")
print(labels_df["gender"].value_counts())

print("\nCategory:")
print(labels_df["category"].value_counts())

print("\nColor:")
print(
    labels_df["color"]
    .value_counts()
    .reindex(COLORS, fill_value=0)
)

print("\nCheck img (1).jpg:")
print(
    labels_df[
        labels_df["filename"] == "img (1).jpg"
    ][
        [
            "filename",
            "gender",
            "color",
            "category",
            "gender_id",
            "category_id",
            "color_id"
        ]
    ]
)

# ============================================================
# CELL 5 — STRATIFIED SPLIT
# ============================================================
#
# We use the label for splitting so that gender,
# category and color remain reasonably represented.
#
# This also avoids the previous problem where some classes
# had only one sample in a stratified split.
# ============================================================

labels_df["label"] = (
    labels_df["gender"]
    + "_"
    + labels_df["category"]
    + "_"
    + labels_df["color"]
)

counts = (
    labels_df["label"]
    .value_counts()
)

rare = counts[
    counts < 3
]

print(
    "classes with fewer than 3 images:",
    len(rare)
)

if len(rare):
    print(rare)

# ------------------------------------------------------------
# For robust splitting, use color as the primary stratification
# because color CNN is the new model being evaluated.
# ------------------------------------------------------------

train_val_df, test_df = train_test_split(
    labels_df,
    test_size=0.15,
    random_state=SEED,
    stratify=labels_df["color_id"]
)

train_df, val_df = train_test_split(
    train_val_df,
    test_size=0.20,
    random_state=SEED,
    stratify=train_val_df["color_id"]
)

print()
print("Train      :", len(train_df))
print("Validation :", len(val_df))
print("Test       :", len(test_df))


# ============================================================
# CELL 6 — IMAGE LOADING
# ============================================================

def load_rgb_image(path):
    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(
            f"Unable to read image: {path}"
        )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    image = cv2.resize(
        image,
        (IMG_SIZE, IMG_SIZE)
    )

    image = image.astype(np.float32) / 255.0

    return image


def make_arrays(df):

    X = []
    gender_y = []
    category_y = []
    color_y = []

    errors = []

    for _, row in df.iterrows():

        try:
            image = load_rgb_image(
                row["image_path"]
            )

            X.append(image)
            gender_y.append(
                int(row["gender_id"])
            )
            category_y.append(
                int(row["category_id"])
            )
            color_y.append(
                int(row["color_id"])
            )

        except Exception as e:
            errors.append(
                {
                    "filename": row["filename"],
                    "error": str(e)
                }
            )

    return (
        np.asarray(X, dtype=np.float32),
        np.asarray(gender_y, dtype=np.int32),
        np.asarray(category_y, dtype=np.int32),
        np.asarray(color_y, dtype=np.int32),
        errors
    )


X_train, y_gender_train, y_category_train, y_color_train, train_errors = (
    make_arrays(train_df)
)

X_val, y_gender_val, y_category_val, y_color_val, val_errors = (
    make_arrays(val_df)
)

X_test, y_gender_test, y_category_test, y_color_test, test_errors = (
    make_arrays(test_df)
)

print("X_train:", X_train.shape)
print("X_val  :", X_val.shape)
print("X_test :", X_test.shape)

if train_errors or val_errors or test_errors:
    print(
        "Image loading errors:",
        len(train_errors) + len(val_errors) + len(test_errors)
    )

# ============================================================
# CELL 7 — LOAD EXISTING GENDER/CATEGORY CNN
# ============================================================

EXISTING_MODEL_PATH = (
    BASE_DIR
    / "cnn"
    / "models"
    / "smartcart_cnn.keras"
)

EXISTING_MAPPING_PATH = (
    BASE_DIR
    / "cnn"
    / "models"
    / "class_mapping.json"
)

existing_model = None
existing_feature_extractor = None

if EXISTING_MODEL_PATH.exists():

    print(
        "Loading existing SmartCart CNN:"
    )
    print(
        EXISTING_MODEL_PATH
    )

    existing_model = keras.models.load_model(
        EXISTING_MODEL_PATH
    )

    print(
        "Existing CNN loaded."
    )

    print(
        "Outputs:",
        existing_model.output_names
    )

    # --------------------------------------------------------
    # Existing model's feature layer
    # --------------------------------------------------------

    try:
        existing_feature_extractor = keras.Model(
            inputs=existing_model.input,
            outputs=existing_model.get_layer(
                "feature_layer"
            ).output
        )

        print(
            "Existing feature extractor ready."
        )

    except Exception as e:
        print(
            "Could not create feature extractor:",
            e
        )

else:
    print()
    print(
        "WARNING:"
    )
    print(
        "Existing gender/category CNN was not found."
    )
    print(
        "Expected:"
    )
    print(
        EXISTING_MODEL_PATH
    )



# ============================================================
# CELL 8 — LOAD EXISTING CLASS MAPPING
# ============================================================

if EXISTING_MAPPING_PATH.exists():

    with open(
        EXISTING_MAPPING_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        existing_mapping = json.load(f)

    existing_gender_mapping = {
        int(k): v.upper()
        for k, v in existing_mapping["gender"].items()
    }

    existing_category_mapping = {
        int(k): v.upper()
        for k, v in existing_mapping["category"].items()
    }

    print(
        "Existing gender mapping:",
        existing_gender_mapping
    )

    print(
        "Existing category mapping:",
        existing_category_mapping
    )

else:

    existing_gender_mapping = {
        k: v.upper()
        for k, v in id_to_gender.items()
    }

    existing_category_mapping = {
        k: v.upper()
        for k, v in id_to_category.items()
    }



# ============================================================
# CELL 9 — NEW COLOR CNN
# ============================================================

color_augmentation = keras.Sequential(
    [
        layers.RandomFlip(
            "horizontal"
        ),
        layers.RandomRotation(
            0.05
        ),
        layers.RandomZoom(
            0.10
        ),
        layers.RandomContrast(
            0.10
        )
    ],
    name="color_augmentation"
)

color_inputs = keras.Input(
    shape=(
        IMG_SIZE,
        IMG_SIZE,
        3
    ),
    name="color_image"
)

x = color_augmentation(
    color_inputs
)

x = layers.Conv2D(
    32,
    (3, 3),
    padding="same",
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D((2, 2))(x)

x = layers.Conv2D(
    64,
    (3, 3),
    padding="same",
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D((2, 2))(x)

x = layers.Conv2D(
    128,
    (3, 3),
    padding="same",
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D((2, 2))(x)

x = layers.Conv2D(
    256,
    (3, 3),
    padding="same",
    activation="relu"
)(x)

x = layers.BatchNormalization()(x)
x = layers.MaxPooling2D((2, 2))(x)

x = layers.GlobalAveragePooling2D(
    name="color_feature_layer"
)(x)

x = layers.Dense(
    256,
    activation="relu"
)(x)

x = layers.Dropout(
    0.40
)(x)

color_outputs = layers.Dense(
    len(COLORS),
    activation="softmax",
    name="color_output"
)(x)

color_model = keras.Model(
    color_inputs,
    color_outputs,
    name="SmartCartColorCNN"
)

color_model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

color_model.summary()

# ============================================================
# CELL 10 — COLOR CLASS WEIGHTS
# ============================================================

class_weights_array = compute_class_weight(
    class_weight="balanced",
    classes=np.arange(len(COLORS)),
    y=y_color_train
)

color_class_weights = {
    int(i): float(weight)
    for i, weight in enumerate(
        class_weights_array
    )
}

print(
    "COLOR CLASS WEIGHTS"
)

for i, weight in color_class_weights.items():

    print(
        f"{COLORS[i].upper():10s}: "
        f"{weight:.4f}"
    )

# ============================================================
# CELL 11 — TRAIN COLOR CNN
# ============================================================

COLOR_MODEL_PATH = (
    MODEL_DIR
    / "color_cnn.keras"
)

callbacks = [

    keras.callbacks.ModelCheckpoint(
        filepath=str(
            COLOR_MODEL_PATH
        ),
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1
    ),

    keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        mode="max",
        patience=8,
        restore_best_weights=True,
        verbose=1
    ),

    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )
]

history = color_model.fit(
    X_train,
    y_color_train,
    validation_data=(
        X_val,
        y_color_val
    ),
    epochs=40,
    batch_size=BATCH_SIZE,
    class_weight=color_class_weights,
    callbacks=callbacks,
    verbose=1
)

# ============================================================
# CELL 12 — TRAINING GRAPHS
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("SmartCart Color CNN Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    PLOT_DIR / "color_accuracy.png",
    dpi=150
)

plt.show()


plt.figure(figsize=(10, 6))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("SmartCart Color CNN Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    PLOT_DIR / "color_loss.png",
    dpi=150
)

plt.show()

# ============================================================
# CELL 13 — COLOR CNN TEST
# ============================================================

best_color_model = keras.models.load_model(
    COLOR_MODEL_PATH
)

test_loss, test_accuracy = (
    best_color_model.evaluate(
        X_test,
        y_color_test,
        verbose=1
    )
)

print()
print("=" * 70)
print("COLOR CNN TEST RESULT")
print("=" * 70)

print(
    f"Test accuracy: "
    f"{test_accuracy * 100:.2f}%"
)

# ============================================================
# CELL 14 — COLOR CLASSIFICATION REPORT
# ============================================================

color_probabilities = (
    best_color_model.predict(
        X_test,
        verbose=1
    )
)

color_predictions = np.argmax(
    color_probabilities,
    axis=1
)

color_accuracy = accuracy_score(
    y_color_test,
    color_predictions
)

print()
print("=" * 70)
print("COLOR CLASSIFICATION REPORT")
print("=" * 70)

print(
    classification_report(
        y_color_test,
        color_predictions,
        labels=np.arange(len(COLORS)),
        target_names=[
            c.upper()
            for c in COLORS
        ],
        zero_division=0
    )
)

cm = confusion_matrix(
    y_color_test,
    color_predictions,
    labels=np.arange(len(COLORS))
)

cm_df = pd.DataFrame(
    cm,
    index=[
        c.upper()
        for c in COLORS
    ],
    columns=[
        c.upper()
        for c in COLORS
    ]
)

print()
print("=" * 70)
print("COLOR CONFUSION MATRIX")
print("=" * 70)

print(
    cm_df.to_string()
)

cm_df.to_csv(
    REPORT_DIR / "color_confusion_matrix.csv"
)

# ============================================================
# CELL 15 — PER-COLOR ACCURACY
# ============================================================

print()
print("=" * 70)
print("PER-COLOR ACCURACY")
print("=" * 70)

for color_id, color_name in enumerate(COLORS):

    mask = (
        y_color_test
        ==
        color_id
    )

    total = int(
        np.sum(mask)
    )

    correct = int(
        np.sum(
            color_predictions[mask]
            ==
            color_id
        )
    )

    accuracy = (
        correct / total
        if total > 0
        else 0.0
    )

    print(
        f"{color_name.upper():10s} "
        f"{correct:3d}/{total:<3d} "
        f"{accuracy * 100:6.2f}%"
    )

# ============================================================
# CELL 16 — SAVE COLOR PREDICTIONS
# ============================================================

test_prediction_df = test_df.iloc[
    :len(color_predictions)
].copy()

test_prediction_df["predicted_color"] = [
    id_to_color[int(x)]
    for x in color_predictions
]

test_prediction_df["color_confidence"] = (
    np.max(
        color_probabilities,
        axis=1
    )
)

test_prediction_df["color_correct"] = (
    test_prediction_df["color"]
    ==
    test_prediction_df["predicted_color"]
)

test_prediction_df[
    [
        "filename",
        "color",
        "predicted_color",
        "color_confidence",
        "color_correct"
    ]
].to_csv(
    REPORT_DIR / "color_test_predictions.csv",
    index=False
)

print(
    "Saved:",
    REPORT_DIR / "color_test_predictions.csv"
)

# ============================================================
# CELL 17 — PREPARE IMAGE FOR EXISTING CNN
# ============================================================

def prepare_image(path):

    image = cv2.imread(
        str(path)
    )

    if image is None:
        raise ValueError(
            f"Unable to read image: {path}"
        )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    image = cv2.resize(
        image,
        (IMG_SIZE, IMG_SIZE)
    )

    image = image.astype(
        np.float32
    ) / 255.0

    return np.expand_dims(
        image,
        axis=0
    )

# ============================================================
# CELL 18 — PREDICT COLOR
# ============================================================

def predict_color(image_path):

    image = prepare_image(
        image_path
    )

    probabilities = (
        best_color_model.predict(
            image,
            verbose=0
        )[0]
    )

    color_id = int(
        np.argmax(probabilities)
    )

    return {
        "color":
            id_to_color[color_id].upper(),

        "confidence":
            float(
                probabilities[color_id]
            ),

        "scores": {
            id_to_color[i]:
                float(probabilities[i])
            for i in range(len(COLORS))
        }
    }

# ============================================================
# CELL 19 — PREDICT GENDER + CATEGORY
# ============================================================

def predict_gender_category(
    image_path
):

    if existing_model is None:
        raise RuntimeError(
            "Existing gender/category CNN "
            "is not loaded."
        )

    image = prepare_image(
        image_path
    )

    predictions = (
        existing_model.predict(
            image,
            verbose=0
        )
    )

    # --------------------------------------------------------
    # Existing SmartCart model has:
    #
    # output 0 = gender
    # output 1 = category
    # --------------------------------------------------------

    gender_prediction = (
        predictions[0][0]
    )

    category_prediction = (
        predictions[1][0]
    )

    gender_id = int(
        np.argmax(
            gender_prediction
        )
    )

    category_id = int(
        np.argmax(
            category_prediction
        )
    )

    return {

        "gender":
            existing_gender_mapping[
                gender_id
            ],

        "gender_confidence":
            float(
                gender_prediction[
                    gender_id
                ]
            ),

        "category":
            existing_category_mapping[
                category_id
            ],

        "category_confidence":
            float(
                category_prediction[
                    category_id
                ]
            )
    }

# ============================================================
# CELL 20 — EXTRACT EXISTING CNN EMBEDDING
# ============================================================

def extract_embedding(
    image_path
):

    if existing_feature_extractor is None:

        raise RuntimeError(
            "Existing feature extractor "
            "is not available."
        )

    image = prepare_image(
        image_path
    )

    features = (
        existing_feature_extractor
        .predict(
            image,
            verbose=0
        )[0]
    )

    norm = np.linalg.norm(
        features
    )

    if norm > 0:
        features = (
            features / norm
        )

    return features

# ============================================================
# CELL 21 — COMPLETE IMAGE ANALYSIS
# ============================================================

def analyze_image(
    image_path
):

    gender_category = (
        predict_gender_category(
            image_path
        )
    )

    color_result = (
        predict_color(
            image_path
        )
    )

    embedding = (
        extract_embedding(
            image_path
        )
    )

    prediction = (
        f"{gender_category['gender']} "
        f"{gender_category['category']} "
        f"{color_result['color']}"
    )

    return {

        "prediction":
            prediction,

        "gender":
            gender_category["gender"],

        "gender_confidence":
            gender_category[
                "gender_confidence"
            ],

        "category":
            gender_category["category"],

        "category_confidence":
            gender_category[
                "category_confidence"
            ],

        "color":
            color_result["color"],

        "color_confidence":
            color_result["confidence"],

        "color_scores":
            color_result["scores"],

        "embedding":
            embedding.tolist()
    }



# ============================================================
# CELL 22 — TEST img (1).jpg
# ============================================================

QUERY_IMAGE = (
    TRAIN_DIR
    / "img (1).jpg"
)

print(
    "=" * 70
)

print(
    "QUERY IMAGE VERIFICATION"
)

print(
    "=" * 70
)

print(
    "Image:",
    QUERY_IMAGE
)

print()

csv_row = labels_df[
    labels_df["filename"]
    ==
    "img (1).jpg"
]

print(
    "CSV label:"
)

print(
    csv_row[
        [
            "filename",
            "gender",
            "color",
            "category"
        ]
    ].to_string(index=False)
)

print()

result = analyze_image(
    QUERY_IMAGE
)

print(
    json.dumps(
        result,
        indent=4
    )
)

# ============================================================
# CELL 23 — SAVE COMBINED CLASS MAPPING
# ============================================================

mapping = {

    "gender": {
        str(k): v
        for k, v in existing_gender_mapping.items()
    },

    "category": {
        str(k): v
        for k, v in existing_category_mapping.items()
    },

    "color": {
        str(k): v.upper()
        for k, v in id_to_color.items()
    },

    "image_size": IMG_SIZE
}

mapping_path = (
    MODEL_DIR
    / "class_mapping.json"
)

with open(
    mapping_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        mapping,
        f,
        indent=4
    )

print(
    "Saved:",
    mapping_path
)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("STARTING CNN PIPELINE")
    print("=" * 70)

    # The cells above intentionally execute sequentially when this
    # script is launched. This final block only marks successful completion.

    print()
    print("=" * 70)
    print("SMARTCART CNN COMPLETED")
    print("=" * 70)
    print()
    print("Color model:")
    print(MODEL_DIR / "color_cnn.keras")
    print()
    print("Reports:")
    print(REPORT_DIR)
