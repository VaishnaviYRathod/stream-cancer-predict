import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle  # Use the standard pickle module
import plotly.graph_objects as go

# Define the column names based on the typical structure of the breast cancer dataset
column_names = [
    'id', 'diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se', 'compactness_se', 'concavity_se', 
    'concave points_se', 'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst', 
    'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 
    'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

def create_model(data):
    # Ensure 'diagnosis' column exists
    if 'diagnosis' not in data.columns:
        print("Error: 'diagnosis' column not found in data")
        return None, None
    
    X = data.drop(['diagnosis'], axis=1)
    y = data['diagnosis']
    
    # Scale the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Test model
    y_pred = model.predict(X_test)
    print('Accuracy of our model: ', accuracy_score(y_test, y_pred))
    print("Classification report: \n", classification_report(y_test, y_pred))
    
    return model, scaler

def get_clean_data():
    file_path = "data/data.csv"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    try:
        data = pd.read_csv(file_path, header=None, names=column_names)  # Read the CSV file with specified column names
        
        # Print column names for debugging
        print("Columns in the CSV file:", data.columns)
        
        # Check if columns to be dropped exist
        columns_to_drop = ['Unnamed: 32', 'id']
        existing_columns = [col for col in columns_to_drop if col in data.columns]
        data = data.drop(existing_columns, axis=1)

        # Check if the 'diagnosis' column exists and map its values
        if 'diagnosis' in data.columns:
            data["diagnosis"] = data["diagnosis"].map({"M": 1, 'B': 0})
        else:
            print("Error: 'diagnosis' column not found in the CSV file")
            return None
        
        print(data.head())  # Print the first few rows of the DataFrame
        return data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    data = get_clean_data()
    if data is not None:
        model, scaler = create_model(data)
        if model is not None and scaler is not None:
            # Ensure the model directory exists
            os.makedirs('model', exist_ok=True)
            
            # Save the model
            with open('model/model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            # Save the scaler
            with open('model/scaler.pkl', 'wb') as f:
                pickle.dump(scaler, f)

if __name__ == '__main__':
    main()
