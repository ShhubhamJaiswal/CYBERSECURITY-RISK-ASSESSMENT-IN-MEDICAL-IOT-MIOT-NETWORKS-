import unittest
import os
import joblib
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

FEATURES = ["hr", "spo2", "tempC"]

class TestAnomalyDetection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load model and initialize Firebase connection once."""
        # Load model
        model_path = os.path.join(os.path.dirname(__file__), "../streamlit_dashboard/isolation_model.joblib")
        cls.model, cls.features = joblib.load(model_path)

        # Initialize Firebase if not already
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                os.path.join(os.path.dirname(__file__), "../streamlit_dashboard/serviceAccountKey.json")
            )
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://miot--project-9560d-default-rtdb.firebaseio.com/"
            })

        cls.readings_ref = db.reference("readings/esp32-01")

    def test_model_file_exists(self):
        """Check if the trained model exists."""
        model_path = os.path.join(os.path.dirname(__file__), "../streamlit_dashboard/isolation_model.joblib")
        self.assertTrue(os.path.exists(model_path), "Model file missing!")

    def test_prediction_on_synthetic_data(self):
        """Check if model can predict anomalies on synthetic input."""
        sample = pd.DataFrame([[90, 98, 36.9]], columns=FEATURES)
        pred = self.model.predict(sample)[0]
        self.assertIn(pred, [1, -1], "Prediction must be normal (1) or anomaly (-1)")

    def test_fetch_and_predict_firebase_data(self):
        """Fetch latest IoT data from Firebase and run anomaly detection."""
        data = self.readings_ref.order_by_key().limit_to_last(5).get()
        if not data:
            self.skipTest("No IoT data found in Firebase for testing.")
        else:
            rows = []
            for ts, v in data.items():
                rows.append([v.get("hr", 0), v.get("spo2", 0), v.get("tempC", 0)])
            df = pd.DataFrame(rows, columns=FEATURES)

            preds = self.model.predict(df)
            print("🔎 Predictions:", preds.tolist())
            self.assertEqual(len(preds), len(df), "Predictions must match input size")


if __name__ == "__main__":
    unittest.main()
