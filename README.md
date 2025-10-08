### LeafCare - Plant Disease Recognition System

LeafCare is an AI-powered application that detects and classifies 38 plant diseases from leaf images using Convolutional Neural Networks (CNNs). The app leverages image preprocessing, data augmentation, and real-time inference to provide accurate and efficient plant disease detection, helping farmers, gardeners, and researchers take early action.

#### Features
- Detect Multiple Diseases: Classifies 38 different plant diseases.
- Real-Time Predictions: Upload a leaf image and get instant results.
- Data Preprocessing: Improves model accuracy and generalization.
- Database Integration: Stores user submissions and prediction history with MongoDB.
- Dockerized Deployment: Easy setup and scalable deployment.
- User-Friendly Interface: Built with Streamlit for a simple, interactive experience.

#### Tech Stack
- ML/AI: Python, TensorFlow/Keras
- Data Handling: Pandas, NumPy
- Frontend: Streamlit
- Database & Deployment: MongoDB, Docker
  
#### Prediction Test
<img width="300" height="auto" alt="image" src="https://github.com/user-attachments/assets/e89c5cd5-6169-42f5-a373-9f03fce7cece" />

#### Quick Start
```bash
git clone https://github.com/NisharaJay/leaf-care-app.git
cd leaf-care-app
pip install -r requirements.txt
streamlit run main.py
```

#### Docker
You can run this app using Docker without setting up dependencies locally.

##### Pull the image from Docker Hub
```bash
docker pull nisharajay/leaf-care-app:latest
```

##### App Preview

<img width="400" height="auto" alt="leaff-image-upload" src="https://github.com/user-attachments/assets/05bbab23-4e5c-4c58-b221-22104a928c40" />
<img width="400" height="auto" alt="leaf-disease-analysis" src="https://github.com/user-attachments/assets/7dbf4c87-25e4-4262-b7de-9c98a3d99927" />
