import pandas as pd
from sklearn.ensemble import IsolationForest
import os

class AnomaliesDetection:
    def __init__(self):
        self.model = IsolationForest(random_state=42)
        self.feature_names = None

    def train(self, csv_path, sep=",", min_rows=300):
        """
        Train model with CSV file containing only normal data.
        Throws exception if file is missing or too small.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file '{csv_path}' not found.")

        df = pd.read_csv(csv_path, sep=sep)

        if len(df) < min_rows:
            raise ValueError(f"Not enough data to train model ({len(df)} rows, minimum = {min_rows}).")

        self.feature_names = df.columns.tolist()
        self.model.fit(df)
        print(f"Model trained on {len(df)} samples and {len(self.feature_names)} features.")

    def predict(self, row):
        """
        Predicts whether an observation is an anomaly.
        Returns True if anomaly, False otherwise.
        """
        if isinstance(row, dict):
            df = pd.DataFrame([row])
        elif isinstance(row, pd.Series):
            df = row.to_frame().T
        elif isinstance(row, pd.DataFrame):
            df = row
        else:
            raise ValueError("Data format not supported for prediction.")

        if self.feature_names:
            df = df[self.feature_names]

        prediction = self.model.predict(df)[0]
        return prediction == -1  # -1 = anomalie, 1 = normal
