import streamlit as st
import tensorflow as tf
import numpy as np
from db_connection import get_disease_info

# Configure page
st.set_page_config(
    page_title="LeafCare - Plant Disease Recognition",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clean design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app background - subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding-top: 1rem;
    }
    
    /* Sidebar styling - cleaner look */
    .stSidebar {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        border-right: 1px solid #475569;
    }
    
    .stSidebar .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    .stSidebar h3 {
        color: #60a5fa !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Navigation buttons - modern style */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:focus {
        outline: 2px solid #60a5fa;
        outline-offset: 2px;
    }
    
    /* Title container - cleaner design */
    .title-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(51, 65, 85, 0.9));
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(96, 165, 250, 0.2);
        text-align: center;
    }
    
    .title-text {
        color: #f8fafc !important;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Feature cards - modern card design */
    .feature-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
        border: 1px solid rgba(96, 165, 250, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .feature-card p {
        color: #cbd5e1 !important;
        margin: 0.5rem 0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .feature-title {
        color: #60a5fa !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    /* Prediction result - success/error states */
    .prediction-result {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white !important;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.3);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .prediction-result.diseased {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3);
        border: 1px solid rgba(248, 113, 113, 0.3);
    }
    
    .prediction-result h2, .prediction-result h3, .prediction-result p {
        color: white !important;
        margin: 0.5rem 0;
    }
    
    /* Upload section */
    .upload-section {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #60a5fa;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #3b82f6;
        background: rgba(30, 41, 59, 0.6);
    }
    
    .upload-section h3 {
        color: #60a5fa !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .upload-section p {
        color: #cbd5e1 !important;
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .stats-container h3 {
        color: #60a5fa !important;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(59, 130, 246, 0.1);
        backdrop-filter: blur(5px);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.4);
    }
    
    .metric-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #60a5fa !important;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #cbd5e1 !important;
        margin-top: 0.25rem;
    }
    
    /* File uploader styling */
    .stFileUploader label {
        color: #60a5fa !important;
        font-weight: 500;
    }
    
    .stFileUploader > div {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 8px;
        color: #e2e8f0 !important;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .stSelectbox label {
        color: #60a5fa !important;
        font-weight: 500;
    }
    
    /* Text styles */
    .welcome-text {
        color: #e2e8f0 !important;
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: center;
        margin: 2rem 0;
    }
    
    .section-header {
        color: #f8fafc !important;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .cta-section {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    .cta-section h3 {
        color: #60a5fa !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .cta-section p {
        color: #cbd5e1 !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Status indicators */
    .status-healthy {
        color: #10b981 !important;
        font-weight: 600;
    }
    
    .status-diseased {
        color: #ef4444 !important;
        font-weight: 600;
    }
    
    .success-message {
        color: #10b981 !important;
        font-weight: 500;
        text-align: center;
        margin-top: 1rem;
    }
    
    .info-message {
        color: #94a3b8 !important;
        text-align: center;
    }
    
    /* Override default text colors */
    .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f8fafc !important;
    }
    
    /* Alert styling */
    .stAlert {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(96, 165, 250, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 8px;
    }
    
    /* Spinner styling */
    .stSpinner > div > div {
        border-top-color: #60a5fa !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #60a5fa;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3b82f6;
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .title-text {
            font-size: 2rem;
        }
        
        .feature-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
        
        .title-container {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

#Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("./model/trained_model.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions) #return index of max element

#Sidebar
st.sidebar.markdown("### 🌿 Navigation")
st.sidebar.markdown("---")

# Create navigation buttons instead of dropdown
if st.sidebar.button("Home", use_container_width=True):
    st.session_state.page = "home"
if st.sidebar.button("About", use_container_width=True):
    st.session_state.page = "about"
if st.sidebar.button("Disease Recognition", use_container_width=True):
    st.session_state.page = "recognition"

# Initialize page state if not exists
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Get current page
if st.session_state.page == "home":
    app_mode = "Home"
elif st.session_state.page == "about":
    app_mode = "About"
elif st.session_state.page == "recognition":
    app_mode = "Disease Recognition"
else:
    app_mode = "Home"

# Add some sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.markdown("""
<div class="metric-card">
    <div class="metric-number">38</div>
    <div class="metric-label">Disease Classes</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="metric-card" style="margin-top: 0.5rem;">
    <div class="metric-number">87K+</div>
    <div class="metric-label">Training Images</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.info("📸 Upload clear, well-lit images of plant leaves for accurate results!")

#Main Page
if(app_mode=="Home"):
    # Title Section
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🌿 LeafCare</h1>
        <p style="color: #cbd5e1; font-size: 1.3rem; margin-top: 1rem; font-weight: 500;">
            AI-Powered Plant Disease Recognition
        </p>
        <p style="color: #94a3b8; font-size: 1rem; margin-top: 0.5rem;">
            Protecting crops with advanced machine learning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-text">
        <h2 class="section-header">Welcome to the Future of Plant Health! 🚜</h2>
        <p>
            LeafCare empowers farmers and gardeners with instant AI-driven plant disease detection. 
            Simply upload a leaf image, and our advanced neural network will provide accurate diagnosis 
            and actionable recommendations. Join thousands of users protecting their crops with smart technology! 🌾
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 How It Works</div>
            <p><strong>1. Upload:</strong> Navigate to Disease Recognition and select a plant image</p>
            <p><strong>2. Analyze:</strong> Our CNN model processes the image in seconds</p>
            <p><strong>3. Results:</strong> Get instant diagnosis with treatment recommendations</p>
            <p><strong>4. Act:</strong> Apply suggested solutions to protect your plants</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚡ Lightning Fast</div>
            <p>Advanced preprocessing and optimized model architecture deliver results in under 3 seconds, 
            enabling real-time decision making in the field.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎯 Why LeafCare?</div>
            <p><strong>✓ Proven Accuracy:</strong> CNN trained on 87,000+ diverse plant images</p>
            <p><strong>✓ Easy to Use:</strong> Clean, intuitive interface for all skill levels</p>
            <p><strong>✓ Comprehensive:</strong> Covers 38 diseases across 10+ plant species</p>
            <p><strong>✓ Expert Guidance:</strong> Detailed treatment recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🌱 Supported Plants</div>
            <p>Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, 
            Raspberry, Soybean, Squash, Strawberry, Tomato and more species supported.</p>
        </div>
        """, unsafe_allow_html=True)

    # Call to action
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="cta-section">
            <h3>Ready to Start?</h3>
            <p>Click <strong>Disease Recognition</strong> in the sidebar to upload your plant image 
            and experience the power of AI-driven plant health analysis!</p>
        </div>
        """, unsafe_allow_html=True)

#About Project
elif(app_mode=="About"):
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">📖 About LeafCare</h1>
        <p style="color: #cbd5e1; font-size: 1.2rem; margin-top: 1rem;">
            Advanced AI technology for agricultural innovation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Dataset Overview</div>
            <p>Our comprehensive dataset contains <strong>87,000 high-quality RGB images</strong> of healthy and 
            diseased crop leaves, meticulously organized into <strong>38 distinct classes</strong>. The dataset 
            maintains scientific rigor with an optimal 80/20 training-validation split.</p>
            <p>Each image undergoes careful preprocessing and augmentation to ensure robust model performance 
            across diverse real-world conditions. A dedicated test set of 33 images validates prediction accuracy.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔬 Technical Architecture</div>
            <p><strong>Model:</strong> Deep Convolutional Neural Network optimized for plant pathology</p>
            <p><strong>Input Processing:</strong> Standardized 128x128 pixel preprocessing pipeline</p>
            <p><strong>Training:</strong> Advanced data augmentation with careful validation protocols</p>
            <p><strong>Framework:</strong> TensorFlow/Keras with GPU acceleration support</p>
            <p><strong>Accuracy:</strong> Validated performance across multiple disease categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container">
            <h3 style="text-align: center; margin-bottom: 1.5rem;">📈 Dataset Statistics</h3>
            <div class="metric-card">
                <div class="metric-number">70,295</div>
                <div class="metric-label">Training Images</div>
            </div>
            <div class="metric-card">
                <div class="metric-number">17,572</div>
                <div class="metric-label">Validation Images</div>
            </div>
            <div class="metric-card">
                <div class="metric-number">33</div>
                <div class="metric-label">Test Images</div>
            </div>
            <div class="metric-card">
                <div class="metric-number">10+</div>
                <div class="metric-label">Plant Species</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

#Prediction Page
elif(app_mode=="Disease Recognition"):
    st.markdown("""
    <div class="title-container">
        <h1 class="title-text">🔍 Disease Recognition</h1>
        <p style="color: #cbd5e1; font-size: 1.2rem; margin-top: 1rem;">
            Upload a plant image for instant AI diagnosis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])  # Made first column wider (2:1 ratio)
    
    with col1:
        
        test_image = st.file_uploader(
            "Choose an Image:", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear, well-lit image of a plant leaf"
        )
        
        # Show uploaded image automatically without preview button
        if test_image is not None:
            st.image(test_image, caption="Uploaded Image", use_container_width=True)
            
            # Show success message and analyze button below the image
            st.markdown("""
            <div style="text-align: center; margin-top: 1rem;">
                <p class="success-message">Image uploaded successfully!</p>
                <p class="info-message">Ready for analysis - click predict below</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Analyze button below the success message
            if st.button("Analyze Image", use_container_width=True):
                with st.spinner('Processing image... Please wait'):
                    result_index = model_prediction(test_image)
                    
                    # Reading Labels
                    class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                                'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                                'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                                'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                                'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                                'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                                'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                                'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                                'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                                'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                                'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                                  'Tomato___healthy']
                    
                    prediction = class_name[result_index]
                    disease_info = get_disease_info(prediction)
                    
                    # Format the prediction nicely
                    plant_name = prediction.split('___')[0].replace('_', ' ')
                    condition = prediction.split('___')[1].replace('_', ' ')
                    
                    # Determine status and styling
                    if 'healthy' in condition.lower():
                        icon = "🌿"
                        status = "HEALTHY PLANT"
                        result_class = ""
                        status_class = "status-healthy"
                    else:
                        icon = "⚠️"
                        status = "DISEASE DETECTED"
                        result_class = "diseased"
                        status_class = "status-diseased"
                    
                    # Display results using full width
                    st.markdown("---")
                    st.markdown("<h2 style='text-align: center; color: #f8fafc; margin-bottom: 2rem;'>🔬 Analysis Results</h2>", unsafe_allow_html=True)
                    
                    # Use full width for results display
                    col_result1, col_result2, col_result3 = st.columns([1, 1, 1])
                    
                    with col_result1:
                        st.markdown(f"""
                        <div class="prediction-result {result_class}" style="height: 100%;">
                            <h2>{icon}</h2>
                            <h3>Detection Result</h3>
                            <p><strong>Plant:</strong> {plant_name.title()}</p>
                            <p><strong>Condition:</strong> {condition.title()}</p>
                            <p style="font-size: 1.1rem; margin-top: 1rem; font-weight: 600;">
                                Status: <span class="{status_class}">{status}</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_result2:
                        # Show disease details if available
                        if disease_info:
                            st.markdown(f"""
                            <div class="feature-card" style="height: 100%;">
                                <div class="feature-title">📋 Disease Information</div>
                                <p><strong>Description:</strong> {disease_info['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="feature-card" style="height: 100%;">
                                <div class="feature-title">📋 Plant Information</div>
                                <p><strong>Plant:</strong> {plant_name.title()}</p>
                                <p><strong>Health Status:</strong> {condition.title()}</p>
                                <p>No specific disease information available in database.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col_result3:
                        # Show recommendations based on result
                        if 'healthy' not in condition.lower():
                            st.markdown("""
                            <div class="feature-card" style="height: 100%;">
                                <div class="feature-title">🩺 Treatment Recommendations</div>
                                <p><strong>Immediate Actions:</strong></p>
                                <p>• Remove affected leaves</p>
                                <p>• Isolate plant</p>
                                <p>• Apply appropriate treatment</p>
                                <p><strong>Long-term Care:</strong></p>
                                <p>• Improve air circulation</p>
                                <p>• Adjust watering schedule</p>
                                <p>• Monitor surrounding plants</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.balloons()
                            st.markdown("""
                            <div class="feature-card" style="height: 100%;">
                                <div class="feature-title">🎉 Excellent Plant Health!</div>
                                <p><strong>Keep up the great work:</strong></p>
                                <p>• Consistent watering</p>
                                <p>• Proper nutrition</p>
                                <p>• Adequate sunlight</p>
                                <p>• Regular monitoring</p>
                                <p>• Preventive care</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Additional detailed information below the horizontal layout
                    st.markdown("---")
                    
                    if 'healthy' not in condition.lower() and disease_info:
                        col_detail1, col_detail2 = st.columns([1, 1])
                        
                        with col_detail1:
                            st.markdown(f"""
                            <div class="feature-card">
                                <div class="feature-title">🔬 Detailed Disease Analysis</div>
                                <p><strong>Full Description:</strong> {disease_info['description']}</p>
                                <p><strong>Recommended Solution:</strong> {disease_info['solution']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_detail2:
                            st.markdown("""
                            <div class="feature-card">
                                <div class="feature-title">📝 Additional Recommendations</div>
                                <p><strong>Preventive Measures:</strong></p>
                                <p>• Regular inspection of plants</p>
                                <p>• Proper spacing between plants</p>
                                <p>• Use of disease-resistant varieties</p>
                                <p>• Crop rotation practices</p>
                                <p>• Sanitation of gardening tools</p>
                            </div>
                            """, unsafe_allow_html=True)