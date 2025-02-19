import pickle
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Predefined Doctor Responses
doctor_responses = [
    "Thank you for your query. Please provide more details about the symptoms.",
    "It's important to consider the size and shape of the lump. Can you describe it?",
    "Have you noticed any changes in the skin over the lump, such as dimpling or redness?",
    "Are there any other symptoms, like pain or nipple discharge?",
    "It's good that you're getting this checked. Early detection is crucial.",
    "Based on the data provided, it seems like the results are benign. Please consult a specialist for confirmation.",
    "The measurements indicate a higher risk. Further tests are recommended.",
    "Please ensure you get a mammogram done if not already.",
    "How long have you noticed the lump?",
    "Is there any family history of breast cancer?",
    "Regular check-ups are very important. Make sure to follow up with your healthcare provider.",
    "It's natural to feel anxious. Try to stay calm and follow the recommended procedures.",
    "Maintaining a healthy lifestyle can help reduce risks. Consider a balanced diet and regular exercise.",
    "It's good that you're proactive about your health. Stay informed and aware.",
    "Have you experienced any weight loss or gain recently?",
    "Hormonal changes can sometimes cause lumps. Have you noticed any changes in your menstrual cycle?",
    "It's important to stay positive and hopeful.",
    "If you have any medical reports, please share them with your doctor.",
    "Have you been experiencing fatigue or lack of energy?",
    "Do you have any pain or discomfort in the breast area?",
    "It’s essential to follow the treatment plan provided by your doctor.",
    "Are you currently taking any medications?",
    "Remember, not all lumps are cancerous. Many are benign.",
    "Regular self-exams can help in early detection. Make it a habit.",
    "If you have dense breast tissue, it might be harder to detect abnormalities.",
    "Do you have any questions about the procedures involved?",
    "Make sure to get enough rest and sleep.",
    "Are you facing any issues with your insurance or healthcare provider?",
    "Stay hydrated and maintain a healthy diet.",
    "Are there any other health concerns you have?",
    "Make sure to keep all follow-up appointments.",
    "Have you experienced any changes in your appetite?",
    "Avoid stress and practice relaxation techniques.",
    "Do you have any known allergies?",
    "It's important to stay in touch with your healthcare provider.",
    "Have you undergone any surgeries in the past?",
    "Make sure to keep a record of all your medical reports.",
    "It’s essential to have a support system. Talk to your family and friends.",
    "Are you currently pregnant or planning to be?",
    "Ensure that you follow all the instructions provided by your doctor.",
    "Keep monitoring any changes and report them to your healthcare provider.",
    "Stay informed about the latest research and treatments.",
    "Do you need assistance in understanding your medical reports?",
    "Are you experiencing any side effects from the medication?",
    "Consider joining a support group for breast cancer patients.",
    "Make sure to follow a regular screening schedule.",
    "If you have any doubts, don’t hesitate to seek a second opinion.",
    "Stay connected with your doctor for any updates.",
    "If you need emotional support, consider talking to a counselor.",
    "Stay hopeful and trust the medical process."
]

# Current message index
current_message_index = 0

def get_doctor_response():
    global current_message_index
    response = doctor_responses[current_message_index % len(doctor_responses)]
    current_message_index += 1
    return response

def send_message():
    st.session_state.chat_history.append({
        "user": st.session_state.user_message,
        "doctor": get_doctor_response()
    })
    st.session_state.user_message = ""

def chat_interface():
    st.write("## Chat with Cancer Doctor")
    st.write("Feel free to ask any questions related to your condition.")
    
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Doctor:** {chat['doctor']}")
    
    st.session_state.user_message = st.text_input("Enter your message:", key="user_message_input")
    
    if st.button("Send", key="send_button"):
        if st.session_state.user_message:
            send_message()

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_message' not in st.session_state:
    st.session_state.user_message = ""
def add_sidebar():
    st.sidebar.title("Cell Nuclei Measurement")
    
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave_points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave_points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave_points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(label, 0.0, 100.0, 50.0)
    
    input_df = pd.DataFrame(input_dict, index=[0])
    return input_df

def get_radar_chart(input_data):
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 
                'Smoothness', 'Compactness', 
                'Concavity', 'Concave Points',
                'Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
          input_data['radius_mean'].values[0], input_data['texture_mean'].values[0], input_data['perimeter_mean'].values[0],
          input_data['area_mean'].values[0], input_data['smoothness_mean'].values[0], input_data['compactness_mean'].values[0],
          input_data['concavity_mean'].values[0], input_data['concave_points_mean'].values[0], input_data['symmetry_mean'].values[0],
          input_data['fractal_dimension_mean'].values[0]
        ],
        theta=categories,
        fill='toself',
        name='Mean Value',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
          input_data['radius_se'].values[0], input_data['texture_se'].values[0], input_data['perimeter_se'].values[0], input_data['area_se'].values[0],
          input_data['smoothness_se'].values[0], input_data['compactness_se'].values[0], input_data['concavity_se'].values[0],
          input_data['concave_points_se'].values[0], input_data['symmetry_se'].values[0], input_data['fractal_dimension_se'].values[0]
        ],
        theta=categories,
        fill='toself',
        name='Standard Error',
        line=dict(color='green')
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
          input_data['radius_worst'].values[0], input_data['texture_worst'].values[0], input_data['perimeter_worst'].values[0],
          input_data['area_worst'].values[0], input_data['smoothness_worst'].values[0], input_data['compactness_worst'].values[0],
          input_data['concavity_worst'].values[0], input_data['concave_points_worst'].values[0], input_data['symmetry_worst'].values[0],
          input_data['fractal_dimension_worst'].values[0]
        ],
        theta=categories,
        fill='toself',
        name='Worst Value',
        line=dict(color='red')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Adjust range to match the input slider values
            )),
        showlegend=True,
        hovermode='closest',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def add_predictions(input_data):
    model = pickle.load(open("model/model.pkl", "rb"))
    scaler = pickle.load(open("model/scaler.pkl", "rb"))
    input_array = input_data.values.flatten().reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    prediction = model.predict(input_array_scaled)
    prediction_proba = model.predict_proba(input_array_scaled)

    st.write("Prediction: ", "Benign" if prediction[0] == 0 else "Malignant")
    st.write("Probability of it being benign:", prediction_proba[0][0])
    st.write("Probability of it being malignant:", prediction_proba[0][1])
    st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")

def main():
    st.set_page_config(
        page_title="Breast Cancer Prediction",
        page_icon=":female-doctor:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    input_df = add_sidebar()

    with st.container():
        st.title("Breast Cancer Predictor")
        st.write("Please connect this app to your cytology lab to help diagnose breast cancer from your tissue sample. This app predicts using a machine learning model whether a breast mass is benign or malignant based on the measurements it receives from your cytosis lab. You can also update the measurements by hand using the sliders in the sidebar.")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            radar_chart = get_radar_chart(input_df)
            st.plotly_chart(radar_chart)
        with col2:
            add_predictions(input_df)

if __name__ == '__main__':
    main()

