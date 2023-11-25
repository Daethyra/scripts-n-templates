from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import pandas as pd
import os
from dotenv import load_dotenv

class ModelTrainer:
    def __init__(self):
        load_dotenv()
        self.data_path = os.getenv('TRAINING_DATA_PATH')
        if not self.data_path or not os.path.exists(self.data_path):
            raise ValueError("TRAINING_DATA_PATH environment variable is missing or the file does not exist.")
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(None,))) # Adjust input shape as needed
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"The data file {self.data_path} does not exist.")
    
        try:
            data = pd.read_csv(self.data_path)
        except Exception as e:
            raise IOError(f"Error reading the data file: {e}")
    
        if 'text' not in data.columns or 'label' not in data.columns:
            raise ValueError("Data file must contain 'text' and 'label' columns.")
    
        X = data['text']
        y = data['label']
        return X, y
        data = pd.read_csv(self.data_path)
        X = data['text']
        y = data['label']
        return X, y

    def train_model(self):
        X, y = self.load_data()
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        # Preprocess X_train, X_val, X_test as needed


        try:
            self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32)
            evaluation = self.model.evaluate(X_test, y_test)
            print("Evaluation Results:", evaluation)
        except Exception as e:
            raise RuntimeError(f"Error during model training or evaluation: {e}")

        # Evaluate the model
        evaluation = self.model.evaluate(X_test, y_test)
        print("Evaluation Results:", evaluation)

        # Save the model
        self.model.save(f'MyBinaryClassificationModel_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.h5')

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_model()
