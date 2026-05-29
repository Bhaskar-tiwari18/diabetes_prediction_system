import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DiaSense AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- CREATE USER FILE ----------------
if not os.path.exists("users.csv"):

    users_df = pd.DataFrame({
        "username": ["admin"],
        "password": ["admin123"]
    })

    users_df.to_csv("users.csv", index=False)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Title */
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 22px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Button */
.stButton>button {
    width: 100%;
    height: 3.2em;
    border-radius: 15px;
    border: none;
    background: linear-gradient(to right, #2563eb, #7c3aed);
    color: white;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(to right, #1d4ed8, #6d28d9);
    color: white;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Result Box */
.success-box {
    background: linear-gradient(to right, #065f46, #047857);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.danger-box {
    background: linear-gradient(to right, #991b1b, #dc2626);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

/* Metrics */
.metric-box {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

/* Login Box */
.login-box {
    width: 450px;
    margin: auto;
    margin-top: 80px;
    padding: 40px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🩺 DiaSense AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI-Powered Diabetes Prediction System</div>',
        unsafe_allow_html=True
    )

    menu = st.selectbox(
        "Select Option",
        ["Login", "Register"]
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    users = pd.read_csv("users.csv")

    # ---------------- LOGIN ----------------
    if menu == "Login":

        st.subheader("🔐 Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            result = users[
                (users["username"] == username) &
                (users["password"] == password)
            ]

            if not result.empty:

                st.session_state.logged_in = True

                st.success("Login Successful ✅")

                st.rerun()

            else:
                st.error("Invalid Username or Password ❌")

    # ---------------- REGISTER ----------------
    else:

        st.subheader("📝 Register")

        new_user = st.text_input("Create Username")

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Register"):

            if new_password != confirm_password:

                st.error("Passwords Do Not Match ❌")

            elif new_user in users["username"].values:

                st.warning("Username Already Exists ⚠️")

            else:

                new_data = pd.DataFrame({
                    "username": [new_user],
                    "password": [new_password]
                })

                users = pd.concat(
                    [users, new_data],
                    ignore_index=True
                )

                users.to_csv(
                    "users.csv",
                    index=False
                )

                st.success("Registration Successful ✅")
                st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    # ---------------- HEADER ----------------
    st.markdown(
        '<div class="main-title">🩺 DiaSense AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI-Powered Diabetes Prediction System</div>',
        unsafe_allow_html=True
    )

    # ---------------- LOGOUT ----------------
    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("📋 Patient Information")

    preg = st.sidebar.slider("Pregnancies", 0, 20, 1)

    glucose = st.sidebar.slider("Glucose Level", 0, 300, 120)

    bp = st.sidebar.slider("Blood Pressure", 0, 200, 70)

    skin = st.sidebar.slider("Skin Thickness", 0, 100, 20)

    insulin = st.sidebar.slider("Insulin", 0, 900, 80)

    bmi = st.sidebar.slider("BMI", 0.0, 70.0, 25.0)

    dpf = st.sidebar.slider(
        "Diabetes Pedigree Function",
        0.0,
        3.0,
        0.5
    )

    age = st.sidebar.slider("Age", 1, 120, 25)

    # ---------------- MAIN LAYOUT ----------------
    col1, col2 = st.columns(2)

    # ---------------- LEFT ----------------
    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🧾 Patient Summary")

        st.write(f"**Pregnancies:** {preg}")
        st.write(f"**Glucose:** {glucose}")
        st.write(f"**Blood Pressure:** {bp}")
        st.write(f"**Skin Thickness:** {skin}")
        st.write(f"**Insulin:** {insulin}")
        st.write(f"**BMI:** {bmi}")
        st.write(f"**DPF:** {dpf}")
        st.write(f"**Age:** {age}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- RIGHT ----------------
    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🤖 AI Prediction")

        if st.button("Predict Diabetes"):

            data = np.array([[
                preg,
                glucose,
                bp,
                skin,
                insulin,
                bmi,
                dpf,
                age
            ]])

            data = scaler.transform(data)

            prediction = model.predict(data)

            probability = model.predict_proba(data)

            diabetic_prob = probability[0][1] * 100

            if prediction[0] == 1:

                st.markdown(
                    f'''
                    <div class="danger-box">
                        ⚠️ HIGH DIABETES RISK<br><br>
                        Risk Probability: {diabetic_prob:.2f}%
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f'''
                    <div class="success-box">
                        ✅ LOW DIABETES RISK<br><br>
                        Risk Probability: {diabetic_prob:.2f}%
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- METRICS ----------------
    st.markdown("## 📊 Health Metrics")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f'''
            <div class="metric-box">
                <h3>🩸 Glucose</h3>
                <h2>{glucose}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'''
            <div class="metric-box">
                <h3>⚖️ BMI</h3>
                <h2>{bmi}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f'''
            <div class="metric-box">
                <h3>🎂 Age</h3>
                <h2>{age}</h2>
            </div>
            ''',
            unsafe_allow_html=True
        )

    # ---------------- FEEDBACK ----------------
    st.markdown("---")
    st.markdown("## ⭐ Feedback & Suggestions")

    name = st.text_input("Your Name")

    rating = st.slider(
        "Rate This Application",
        1,
        5,
        4
    )

    feedback = st.text_area("Write Feedback")

    if st.button("Submit Feedback"):

        feedback_data = pd.DataFrame({
            "Name": [name],
            "Rating": [rating],
            "Feedback": [feedback]
        })

        if os.path.exists("feedback.csv"):

            old_data = pd.read_csv("feedback.csv")

            feedback_data = pd.concat(
                [old_data, feedback_data],
                ignore_index=True
            )

        feedback_data.to_csv(
            "feedback.csv",
            index=False
        )

        st.success("Thank You For Your Feedback ❤️")

        st.balloons()

    # ---------------- FOOTER ----------------
    st.markdown("---")

    st.markdown(
        """
        <center>
            <h4 style='color:lightgray;'>
                DiaSense AI • Developed using Python, Streamlit & Machine Learning
            </h4>
        </center>
        """,
        unsafe_allow_html=True
    )
