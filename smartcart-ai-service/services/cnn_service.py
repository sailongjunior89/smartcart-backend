#
# SmartCart CNN Image Search Service
# Author: Junior
#
# Production inference service.
#
# Uses:
#   1. smartcart_cnn.keras
#      - Gender
#      - Category
#
#   2. color_cnn.keras
#      - 11 clothing colors
#
# Does NOT train the models.
#

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from tensorflow import keras


class CNNService:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):

        self.image_size = 128

        self.base_path = (
            Path(__file__).resolve().parent.parent / "cnn"
        )

        self.model_path = (
            self.base_path
            / "models"
            / "smartcart_cnn.keras"
        )

        self.best_model_path = (
            self.base_path
            / "models"
            / "smartcart_cnn_best.keras"
        )

        self.color_model_path = (
            self.base_path
            / "models"
            / "color_cnn.keras"
        )

        self.mapping_path = (
            self.base_path
            / "models"
            / "class_mapping.json"
        )

        self.model = None
        self.color_model = None
        self.feature_extractor = None

        self.gender_mapping = {}
        self.category_mapping = {}
        self.color_mapping = {}

        self.loaded = False

    # =========================================================
    # LOAD MODELS
    # =========================================================

    def load(self):

        print("=" * 70)
        print("SMARTCART CNN SERVICE")
        print("=" * 70)

        print("CNN directory:")
        print(self.base_path)

        print()

        # -----------------------------------------------------
        # Check model files
        # -----------------------------------------------------

        model_path = self.model_path

        if not model_path.exists():

            if self.best_model_path.exists():

                model_path = self.best_model_path

            else:

                raise FileNotFoundError(
                    "SmartCart gender/category CNN not found.\n"
                    f"Expected:\n"
                    f"  {self.model_path}\n"
                    f"or\n"
                    f"  {self.best_model_path}"
                )

        if not self.color_model_path.exists():

            raise FileNotFoundError(
                "Color CNN not found:\n"
                f"{self.color_model_path}"
            )

        if not self.mapping_path.exists():

            raise FileNotFoundError(
                "CNN class mapping not found:\n"
                f"{self.mapping_path}"
            )

        # -----------------------------------------------------
        # Load class mapping
        # -----------------------------------------------------

        print("Loading class mapping...")

        with open(
            self.mapping_path,
            "r",
            encoding="utf-8"
        ) as file:

            mapping = json.load(file)

        self.gender_mapping = {
            int(key): value.upper()
            for key, value
            in mapping["gender"].items()
        }

        self.category_mapping = {
            int(key): value.upper()
            for key, value
            in mapping["category"].items()
        }

        self.color_mapping = {
            int(key): value.upper()
            for key, value
            in mapping["color"].items()
        }

        self.image_size = int(
            mapping.get(
                "image_size",
                128
            )
        )

        print(
            "Gender mapping:",
            self.gender_mapping
        )

        print(
            "Category mapping:",
            self.category_mapping
        )

        print(
            "Color mapping:",
            self.color_mapping
        )

        # -----------------------------------------------------
        # Load gender/category CNN
        # -----------------------------------------------------

        print()
        print("Loading gender/category CNN...")
        print(model_path)

        self.model = keras.models.load_model(
            model_path
        )

        print("Gender/category CNN loaded.")

        print(
            "Model outputs:",
            self.model.output_names
        )

        # -----------------------------------------------------
        # Load color CNN
        # -----------------------------------------------------

        print()
        print("Loading color CNN...")
        print(self.color_model_path)

        self.color_model = keras.models.load_model(
            self.color_model_path
        )

        print("Color CNN loaded.")

        # -----------------------------------------------------
        # Feature extractor
        #
        # Optional.
        # We don't need embeddings for the current
        # Spring Boot attribute search.
        # -----------------------------------------------------

        try:

            self.feature_extractor = keras.Model(
                inputs=self.model.input,
                outputs=self.model.get_layer(
                    "feature_layer"
                ).output
            )

            print(
                "Feature extractor loaded."
            )

        except Exception as error:

            self.feature_extractor = None

            print(
                "Feature extractor unavailable."
            )

            print(
                f"Reason: {error}"
            )

        self.loaded = True

        print()
        print("SMARTCART CNN READY")
        print("=" * 70)

    # =========================================================
    # PREPARE IMAGE
    # =========================================================

    def _prepare_image(
        self,
        image: np.ndarray
    ) -> np.ndarray:

        if image is None:

            raise ValueError(
                "Image is empty."
            )

        # OpenCV BGR → RGB

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        # Resize

        image = cv2.resize(
            image,
            (
                self.image_size,
                self.image_size
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
    # PREDICT GENDER + CATEGORY
    # =========================================================

    def predict_gender_category(
        self,
        image: np.ndarray
    ) -> dict[str, Any]:

        if self.model is None:

            raise RuntimeError(
                "Gender/category CNN has not been loaded."
            )

        processed = self._prepare_image(
            image
        )

        predictions = self.model.predict(
            processed,
            verbose=0
        )

        # -----------------------------------------------------
        # Model output:
        #
        # output 0 = gender
        # output 1 = category
        # -----------------------------------------------------

        if len(predictions) < 2:

            raise RuntimeError(
                "SmartCart CNN must return "
                "gender and category outputs."
            )

        gender_prediction = np.asarray(
            predictions[0][0]
        )

        category_prediction = np.asarray(
            predictions[1][0]
        )

        # -----------------------------------------------------
        # Gender
        # -----------------------------------------------------

        gender_id = int(
            np.argmax(
                gender_prediction
            )
        )

        gender = self.gender_mapping.get(
            gender_id,
            f"UNKNOWN_{gender_id}"
        )

        gender_confidence = float(
            gender_prediction[gender_id]
        )

        # -----------------------------------------------------
        # Category
        # -----------------------------------------------------

        category_id = int(
            np.argmax(
                category_prediction
            )
        )

        category = self.category_mapping.get(
            category_id,
            f"UNKNOWN_{category_id}"
        )

        category_confidence = float(
            category_prediction[category_id]
        )

        return {

            "gender": gender,

            "gender_confidence":
                gender_confidence,

            "category": category,

            "category_confidence":
                category_confidence
        }

    # =========================================================
    # PREDICT COLOR
    # =========================================================

    def predict_color(
        self,
        image: np.ndarray
    ) -> dict[str, Any]:

        if self.color_model is None:

            raise RuntimeError(
                "Color CNN has not been loaded."
            )

        processed = self._prepare_image(
            image
        )

        probabilities = (
            self.color_model.predict(
                processed,
                verbose=0
            )[0]
        )

        color_id = int(
            np.argmax(
                probabilities
            )
        )

        color = self.color_mapping.get(
            color_id,
            f"UNKNOWN_{color_id}"
        )

        confidence = float(
            probabilities[color_id]
        )

        scores = {

            self.color_mapping.get(
                index,
                f"UNKNOWN_{index}"
            ):
                float(probabilities[index])

            for index in range(
                len(probabilities)
            )
        }

        return {

            "color": color,

            "confidence": confidence,

            "scores": scores
        }

    # =========================================================
    # ANALYZE IMAGE
    # =========================================================

    def analyze_image(
        self,
        image: np.ndarray
    ) -> dict[str, Any]:

        gender_category = (
            self.predict_gender_category(
                image
            )
        )

        color_result = (
            self.predict_color(
                image
            )
        )

        prediction = (
            f"{gender_category['gender']} "
            f"{gender_category['category']} "
            f"{color_result['color']}"
        )

        return {

            "prediction": prediction,

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

            "products": []
        }

    # =========================================================
    # SEARCH FROM UPLOADED BYTES
    # =========================================================

    def search(
        self,
        image_bytes: bytes
    ) -> dict[str, Any]:

        if not self.loaded:

            raise RuntimeError(
                "CNN service has not been loaded."
            )

        if not image_bytes:

            raise ValueError(
                "Image data is empty."
            )

        # -----------------------------------------------------
        # Convert bytes → OpenCV image
        # -----------------------------------------------------

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:

            raise ValueError(
                "Cannot decode uploaded image."
            )

        # -----------------------------------------------------
        # Analyze
        # -----------------------------------------------------

        result = self.analyze_image(
            image
        )

        print()
        print("=" * 60)
        print("CNN IMAGE SEARCH")
        print("=" * 60)

        print(
            "Prediction:",
            result["prediction"]
        )

        print(
            "Gender:",
            result["gender"],
            f"({result['gender_confidence']:.4f})"
        )

        print(
            "Category:",
            result["category"],
            f"({result['category_confidence']:.4f})"
        )

        print(
            "Color:",
            result["color"],
            f"({result['color_confidence']:.4f})"
        )

        print("=" * 60)

        return result