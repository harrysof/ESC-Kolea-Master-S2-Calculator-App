import streamlit as st

st.set_page_config(
    page_title="Master 1\nCalculator",
    page_icon= "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fe0.pxfuel.com%2Fwallpapers%2F951%2F106%2Fdesktop-wallpaper-harry-potter-hogwarts-lantern-castle-%25E2%2580%25A2-for-you-harry-potter-face.jpg&f=1&nofb=1&ipt=67dcf6b5e4bbaa6e40d5749842f331503249c2ea1075735ac84522d312eec051",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #ff812f;
        text-align: center;
        padding: 1.5rem 0;
        background: #0e1118;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .subject-header {
        color: #ff812f;
        font-size: 1.2rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #E2E8F0;
        margin-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff812f;
        color: white;
    }
    .result-box {
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        background-color: #0e1118;
        border: 1px solid #48BB78;
    }
    .semester-selector {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
    }
    .semester-button {
        background-color: #4f8bf9;
        color: white;
        padding: 10px 30px;
        border-radius: 20px;
        text-align: center;
        cursor: pointer;
        width: 150px;
    }
    .semester-button.active {
        background-color: #2662de;
        font-weight: bold;
    }
    .s2-color {
        color: #2fffe9;
    }
    
    /* Corner GIF Styles */
    .corner-gif {
        position: fixed;
        top: 85px;
        right: 10px;
        z-index: 9999;
        width: 80px;
        height: 80px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        opacity: 0.8;
        transition: opacity 0.3s ease;
    }
    .corner-gif:hover {
        opacity: 1;
        transform: scale(1.1);
        transition: all 0.3s ease;
    }
    
    /* Alternative: Bottom right corner */
    .corner-gif-bottom {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        opacity: 0.7;
    }
    </style>
    """, unsafe_allow_html=True)

# Add the corner GIF - Replace the URL with your desired GIF
st.markdown("""
    <img src="https://i.gifer.com/XOsX.gif" class="corner-gif" alt="Finance GIF">
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="main-title">
        Master <br>Grade Calculator<br>
        <span style="font-size: 1.2rem; color: #dcdcdc;">By Sofiane Belkacem Nacer</span>
    </div>
    """, unsafe_allow_html=True)

# Updated subjects and their coefficients from the screenshot
subjects_with_coef = {
    "PL": 3,
    "Analyse des Organisations": 4.5,
    "Fiscalité": 1.5,
    "Marketing Mix": 4.5,
    "Econométrie": 3,
    "English": 1.5,
    "Comptabilité Managériale": 4.5,
    "Finance d'Entreprise": 4.5,
    "Microéconomie": 3
}

# Initialize session state
for subject in subjects_with_coef.keys():
    exam_key = f"{subject}_exam"
    td_key = f"{subject}_TD"
    if exam_key not in st.session_state:
        st.session_state[exam_key] = None
    if td_key not in st.session_state:
        st.session_state[td_key] = None

def calculate_semester_average():
    subjects_data = {}
    for subject, coef in subjects_with_coef.items():
        exam_key = f"{subject}_exam"
        td_key = f"{subject}_TD"
        try:
            exam_grade = float(st.session_state.get(exam_key, 0.0) or 0.0)
            td_grade = float(st.session_state.get(td_key, 0.0) or 0.0)
            subjects_data[subject] = {"exam": exam_grade, "td": td_grade, "coef": coef}
        except (ValueError, TypeError):
            st.error(f"Invalid input for {subject}. Please enter numbers only, Sa7a!.")
            return

    total_weighted_sum = 0
    total_credits = sum(subjects_with_coef.values())
    
    for subject, data in subjects_data.items():
        average = (data["exam"] * 0.67) + (data["td"] * 0.33)
        total_weighted_sum += average * data["coef"]

    semester_average = total_weighted_sum / total_credits
    formatted_float = "{:.2f}".format(semester_average)
    better_total = "{:.2f}".format(total_weighted_sum)
    
    # Determine color based on average score
    color = "#FF0000"  # Default red for below 10
    if semester_average >= 15:
        color = "#D89CF6"  # Purple for 15 and up
    elif semester_average >= 14:
        color = "#12CAD6"  # Teal for 14-15
    elif semester_average >= 12:
        color = "#50D890"  # Green for 12-14
    elif semester_average >= 10:
        color = "#FE9801"  # Orange for 10-12
    
    st.markdown(f"""
        <div class="result-box" style="text-align: center;">
            <h3 style="color: #2F855A; margin: 0;">📊 Results</h3>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                Moyenne S2: <strong style="color: {color}">{formatted_float}</strong><br>
            </p>
        </div>
    """, unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    
    subjects_list = list(subjects_with_coef.keys())
    half = len(subjects_list) // 2
    
    for i, subject in enumerate(subjects_list):
        current_col = col1 if i < half else col2
        coef = subjects_with_coef[subject]
        with current_col:
            st.markdown(f'<div class="subject-header">{subject}</div>', unsafe_allow_html=True)
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                st.number_input(
                    "Exam",
                    key=f"{subject}_exam",
                    min_value=0.0,
                    value=None,
                    step=0.05,
                    format="%.2f"
                )
            with subcol2:
                st.number_input(
                    "TD",
                    key=f"{subject}_TD",
                    min_value=0.0,
                    value=None,
                    step=0.05,
                    format="%.2f"
                )

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Calculer Moyenne"):
        calculate_semester_average()


