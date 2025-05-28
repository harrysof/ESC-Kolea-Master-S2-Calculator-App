import streamlit as st

st.set_page_config(
    page_title="Master Grade Calculator",
    page_icon="📊",
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
        font-size: 1.2rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #E2E8F0;
        margin-top: 1rem;
    }
    .s1-header {
        color: #2fffe9;
    }
    .s2-header {
        color: #ff812f;
    }
    .stButton > button {
        width: 100%;
        color: white;
    }
    .s1-button > button {
        background-color: #2fffe9 !important;
        color: #0e1118 !important;
    }
    .s2-button > button {
        background-color: #ff812f !important;
        color: white !important;
    }
    .result-box {
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        background-color: #0e1118;
        border: 1px solid #48BB78;
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
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #262730;
        border-radius: 10px 10px 0px 0px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff812f;
    }
    </style>
    """, unsafe_allow_html=True)

# Add the corner GIF
st.markdown("""
    <img src="https://i.gifer.com/XOsX.gif" class="corner-gif" alt="Finance GIF">
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="main-title">
        Master Grade Calculator<br>
        <span style="font-size: 1.2rem; color: #dcdcdc;">By Sofiane Belkacem Nacer</span>
    </div>
    """, unsafe_allow_html=True)

# S1 subjects and data
s1_subjects = [
    "Statistiques Inférentielles", "Comptabilité Financière", "Management",
    "Marketing", "Macroéconomie", "Informatique", "Droit", "Anglais"
]

# S2 subjects with coefficients
s2_subjects_with_coef = {
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

# Initialize session state for S1
for subject in s1_subjects:
    exam_key = f"s1_{subject}_exam"
    td_key = f"s1_{subject}_TD"
    if exam_key not in st.session_state:
        st.session_state[exam_key] = None
    if td_key not in st.session_state:
        st.session_state[td_key] = None

# Initialize session state for S2
for subject in s2_subjects_with_coef.keys():
    exam_key = f"s2_{subject}_exam"
    td_key = f"s2_{subject}_TD"
    if exam_key not in st.session_state:
        st.session_state[exam_key] = None
    if td_key not in st.session_state:
        st.session_state[td_key] = None

def calculate_s1_average():
    subjects_data = {}
    for subject in s1_subjects:
        exam_key = f"s1_{subject}_exam"
        td_key = f"s1_{subject}_TD"
        try:
            exam_grade = float(st.session_state.get(exam_key, 0.0) or 0.0)
            td_grade = float(st.session_state.get(td_key, 0.0) or 0.0)
            subjects_data[subject] = {"exam": exam_grade, "td": td_grade}
        except (ValueError, TypeError):
            st.error(f"Invalid input for {subject}. Please enter numbers only.")
            return

    total = 0
    for subject, grades in subjects_data.items():
        average = (grades["exam"] * 0.67) + (grades["td"] * 0.33)
        weight = 4.5 if subject in ["Statistiques Inférentielles", "Comptabilité Financière", "Management", "Marketing"] else 3
        total += average * weight

    semester_average = total / 30
    formatted_float = "{:.2f}".format(semester_average)
    better_total = "{:.2f}".format(total)
    
    st.markdown(f"""
        <div class="result-box">
            <h3 style="color: #2F855A; margin: 0;">📊 S1 Results</h3>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                Semester Grade: <strong style="color: #2fffe9">{formatted_float}</strong><br>
                Total: <strong>{better_total}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

def calculate_s2_average():
    subjects_data = {}
    for subject, coef in s2_subjects_with_coef.items():
        exam_key = f"s2_{subject}_exam"
        td_key = f"s2_{subject}_TD"
        try:
            exam_grade = float(st.session_state.get(exam_key, 0.0) or 0.0)
            td_grade = float(st.session_state.get(td_key, 0.0) or 0.0)
            subjects_data[subject] = {"exam": exam_grade, "td": td_grade, "coef": coef}
        except (ValueError, TypeError):
            st.error(f"Invalid input for {subject}. Please enter numbers only, Sa7a!.")
            return

    total_weighted_sum = 0
    total_credits = sum(s2_subjects_with_coef.values())
    
    for subject, data in subjects_data.items():
        average = (data["exam"] * 0.67) + (data["td"] * 0.33)
        total_weighted_sum += average * data["coef"]

    semester_average = total_weighted_sum / total_credits
    formatted_float = "{:.2f}".format(semester_average)
    
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
        <div class="result-box">
            <h3 style="color: #2F855A; margin: 0;">📊 S2 Results</h3>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                Moyenne S2: <strong style="color: {color}">{formatted_float}</strong><br>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["Semestre 1", "Semestre 2"])

with tab1:
    st.markdown("### Semester 1 Calculator")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        half = len(s1_subjects) // 2
        
        for i, subject in enumerate(s1_subjects):
            current_col = col1 if i < half else col2
            coef = 4.5 if subject in ["Statistiques Inférentielles", "Comptabilité Financière", "Management", "Marketing"] else 3
            with current_col:
                st.markdown(f'<div class="subject-header s1-header">{subject} (Coef: {coef})</div>', unsafe_allow_html=True)
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.number_input(
                        "Exam",
                        key=f"s1_{subject}_exam",
                        min_value=0.0,
                        value=None,
                        step=0.05,
                        format="%.2f"
                    )
                with subcol2:
                    st.number_input(
                        "TD",
                        key=f"s1_{subject}_TD",
                        min_value=0.0,
                        value=None,
                        step=0.05,
                        format="%.2f"
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="s1-button">', unsafe_allow_html=True)
        if st.button("Calculer Moyenne S1", key="s1_calc"):
            calculate_s1_average()
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### Semester 2 Calculator")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        subjects_list = list(s2_subjects_with_coef.keys())
        half = len(subjects_list) // 2
        
        for i, subject in enumerate(subjects_list):
            current_col = col1 if i < half else col2
            coef = s2_subjects_with_coef[subject]
            with current_col:
                st.markdown(f'<div class="subject-header s2-header">{subject} (Coef: {coef})</div>', unsafe_allow_html=True)
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.number_input(
                        "Exam",
                        key=f"s2_{subject}_exam",
                        min_value=0.0,
                        value=None,
                        step=0.05,
                        format="%.2f"
                    )
                with subcol2:
                    st.number_input(
                        "TD",
                        key=f"s2_{subject}_TD",
                        min_value=0.0,
                        value=None,
                        step=0.05,
                        format="%.2f"
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="s2-button">', unsafe_allow_html=True)
        if st.button("Calculer Moyenne S2", key="s2_calc"):
            calculate_s2_average()
        st.markdown('</div>', unsafe_allow_html=True)
