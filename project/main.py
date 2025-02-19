import pandas as pd
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Define column names
column_names = [
    'id', 'diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se',
    'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
    'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
    'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

def load_and_clean_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    data = pd.read_csv(file_path, header=None, names=column_names)
    data.drop(columns=['id'], errors='ignore', inplace=True)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    
    return data

def train_model(data):
    X = data.drop(['diagnosis'], axis=1)
    y = data['diagnosis']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print('Model Accuracy:', accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    return model, scaler

def save_model(model, scaler):
    os.makedirs('model', exist_ok=True)
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('model/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

def main():
    file_path = 'data/data.csv'  # Update with correct path
    data = load_and_clean_data(file_path)
    model, scaler = train_model(data)
    save_model(model, scaler)
    print("Model and Scaler saved successfully!")

if __name__ == '__main__':
    main()

