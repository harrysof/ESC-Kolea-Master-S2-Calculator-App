import streamlit as st

st.set_page_config(
    page_title="Master Grade Calculator",
    page_icon="https://i.imgur.com/hKP0yw9.png",
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
        margin-bottom: 0.5rem; /* Added margin for space before inputs */
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

    /* Styling for NumberInput its label, and module average display */
    div[data-testid="stNumberInput"] > label { /* Target Streamlit's label */
        font-weight: normal; /* Adjust as needed */
        color: #dcdcdc;      /* Light gray for labels */
        margin-bottom: 0.2rem;
        display: block;
        font-size: 0.9rem; /* Slightly smaller label */
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 4px;
        border: 1px solid #4A5568; /* Darker border for inputs */
        background-color: #1A202C; /* Dark background for inputs */
        color: #E2E8F0;            /* Light text color for inputs */
        padding: 0.4rem 0.6rem;
        height: 38px; /* Explicit height */
        box-sizing: border-box; /* Ensure padding and border are included in height */
        width: 100%; /* Ensure input takes full column width */
    }
    
    .module-average-label { /* Label for "Moyenne" */
        font-weight: normal;
        color: #dcdcdc;
        margin-bottom: 0.2rem;
        display: block;
        font-size: 0.9rem; 
    }
    
    .module-average-display { /* The box displaying the "Moyenne" value */
        border-radius: 4px;
        border: 1px solid #4A5568;
        background-color: #1A202C; 
        padding: 0.4rem 0.6rem;
        font-size: 0.9rem; /* Match input text size */
        height: 38px; /* Match height of number input box */
        box-sizing: border-box;
        display: flex;
        align-items: center;
        opacity: 0.9; /* Visually similar to a disabled input */
        width: 100%;
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

# Initialize session state for S1 (exam, TD, and module_avg)
for subject in s1_subjects:
    exam_key = f"s1_{subject}_exam"
    td_key = f"s1_{subject}_TD"
    module_avg_key = f"s1_{subject}_module_avg"
    if exam_key not in st.session_state: st.session_state[exam_key] = None
    if td_key not in st.session_state: st.session_state[td_key] = None
    if module_avg_key not in st.session_state: st.session_state[module_avg_key] = 0.0

# Initialize session state for S2 (exam, TD, and module_avg)
for subject in s2_subjects_with_coef.keys():
    exam_key = f"s2_{subject}_exam"
    td_key = f"s2_{subject}_TD"
    module_avg_key = f"s2_{subject}_module_avg"
    if exam_key not in st.session_state: st.session_state[exam_key] = None
    if td_key not in st.session_state: st.session_state[td_key] = None
    if module_avg_key not in st.session_state: st.session_state[module_avg_key] = 0.0

# Callback function to calculate and store individual module average
def calculate_and_store_module_average(prefix, subject_name):
    exam_key = f"{prefix}_{subject_name}_exam"
    td_key = f"{prefix}_{subject_name}_TD"
    module_avg_storage_key = f"{prefix}_{subject_name}_module_avg"

    exam_grade_val = st.session_state.get(exam_key)
    td_grade_val = st.session_state.get(td_key)

    try:
        exam_grade_float = float(exam_grade_val) if exam_grade_val is not None else 0.0
    except (ValueError, TypeError):
        exam_grade_float = 0.0
    
    try:
        td_grade_float = float(td_grade_val) if td_grade_val is not None else 0.0
    except (ValueError, TypeError):
        td_grade_float = 0.0
    
    # Ensure grades are within bounds for calculation
    exam_grade_float = max(0.0, min(20.0, exam_grade_float))
    td_grade_float = max(0.0, min(20.0, td_grade_float))

    average = (exam_grade_float * 0.67) + (td_grade_float * 0.33)
    st.session_state[module_avg_storage_key] = average


def calculate_s1_average():
    total_weighted_sum = 0
    total_credits_s1 = 30 # S1 total credits

    for subject in s1_subjects:
        module_avg_key = f"s1_{subject}_module_avg"
        # Ensure module average is calculated if inputs were directly changed before button press
        # (Though on_change should handle it, this is a fallback)
        if st.session_state.get(f"s1_{subject}_exam") is not None or st.session_state.get(f"s1_{subject}_TD") is not None:
            calculate_and_store_module_average("s1", subject)

        module_avg = float(st.session_state.get(module_avg_key, 0.0))
        
        weight = 4.5 if subject in ["Statistiques Inférentielles", "Comptabilité Financière", "Management", "Marketing"] else 3
        total_weighted_sum += module_avg * weight

    semester_average = total_weighted_sum / total_credits_s1 if total_credits_s1 else 0
    formatted_float = "{:.2f}".format(semester_average)
    
    st.markdown(f"""
        <div class="result-box">
            <h3 style="color: #2F855A; margin: 0;">📊 S1 Results</h3>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                Moyenne S1: <strong style="color: #2fffe9">{formatted_float}</strong><br>
            </p>
        </div>
    """, unsafe_allow_html=True)

def calculate_s2_average():
    total_weighted_sum = 0
    total_credits_s2 = sum(s2_subjects_with_coef.values())
    
    for subject in s2_subjects_with_coef.keys():
        module_avg_key = f"s2_{subject}_module_avg"
        if st.session_state.get(f"s2_{subject}_exam") is not None or st.session_state.get(f"s2_{subject}_TD") is not None:
            calculate_and_store_module_average("s2", subject)
            
        module_avg = float(st.session_state.get(module_avg_key, 0.0))
        coef = s2_subjects_with_coef[subject]
        total_weighted_sum += module_avg * coef

    semester_average = total_weighted_sum / total_credits_s2 if total_credits_s2 else 0
    formatted_float = "{:.2f}".format(semester_average)
    
    color = "#FF0000" 
    if semester_average >= 15: color = "#D89CF6" 
    elif semester_average >= 14: color = "#12CAD6" 
    elif semester_average >= 12: color = "#50D890" 
    elif semester_average >= 10: color = "#FE9801" 
    
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
    st.markdown("### <span style='color: #2fffe9;'>Semestre 1</span> Calculator", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        s1_subjects_list = list(s1_subjects) # Ensure it's a list for consistent ordering
        half = len(s1_subjects_list) // 2
        
        for i, subject in enumerate(s1_subjects_list):
            current_col = col1 if i < half else col2
            coef = 4.5 if subject in ["Statistiques Inférentielles", "Comptabilité Financière", "Management", "Marketing"] else 3
            with current_col:
                st.markdown(f'<div class="subject-header s1-header">{subject} (Coef: {coef})</div>', unsafe_allow_html=True)
                
                # Keys for this subject
                exam_key_s1 = f"s1_{subject}_exam"
                td_key_s1 = f"s1_{subject}_TD"
                module_avg_key_s1 = f"s1_{subject}_module_avg"

                subcol_exam, subcol_td, subcol_avg = st.columns(3)
                with subcol_exam:
                    st.number_input(
                        "Exam",
                        key=exam_key_s1,
                        min_value=0.0, max_value=20.0,
                        value=st.session_state.get(exam_key_s1),
                        step=0.05, format="%.2f",
                        on_change=calculate_and_store_module_average, args=("s1", subject)
                    )
                with subcol_td:
                    st.number_input(
                        "TD",
                        key=td_key_s1,
                        min_value=0.0, max_value=20.0,
                        value=st.session_state.get(td_key_s1),
                        step=0.05, format="%.2f",
                        on_change=calculate_and_store_module_average, args=("s1", subject)
                    )
                with subcol_avg:
                    avg_val = float(st.session_state.get(module_avg_key_s1, 0.0))
                    avg_color = "#FF0000" # Red
                    if avg_val >= 15: avg_color = "#D89CF6" # Purple
                    elif avg_val >= 10: avg_color = "#50D890" # Green
                    elif avg_val >= 7: avg_color = "#4682B4" # SteelBlue
                    
                    # The negative margin is crucial for vertical alignment. Adjust if needed.
                    module_avg_html = f"""
                    <div style="margin-top: -0.18rem;"> 
                        <label class='module-average-label'>Moyenne</label>
                        <div class="module-average-display" style="color: {avg_color};">
                            {avg_val:.2f}
                        </div>
                    </div>
                    """
                    st.markdown(module_avg_html, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col_s1_1, btn_col_s1_2, btn_col_s1_3 = st.columns([1, 2, 1])
    with btn_col_s1_2:
        st.markdown('<div class="s1-button">', unsafe_allow_html=True)
        if st.button("Calculer Moyenne S1", key="s1_calc"):
            calculate_s1_average()
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### <span style='color: #ff812f;'>Semestre 2</span> Calculator", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        s2_subjects_list = list(s2_subjects_with_coef.keys())
        half = len(s2_subjects_list) // 2
        
        for i, subject in enumerate(s2_subjects_list):
            current_col = col1 if i < half else col2
            coef = s2_subjects_with_coef[subject]
            with current_col:
                st.markdown(f'<div class="subject-header s2-header">{subject} (Coef: {coef})</div>', unsafe_allow_html=True)
                
                exam_key_s2 = f"s2_{subject}_exam"
                td_key_s2 = f"s2_{subject}_TD"
                module_avg_key_s2 = f"s2_{subject}_module_avg"

                subcol_exam, subcol_td, subcol_avg = st.columns(3)
                with subcol_exam:
                    st.number_input(
                        "Exam",
                        key=exam_key_s2,
                        min_value=0.0, max_value=20.0,
                        value=st.session_state.get(exam_key_s2),
                        step=0.05, format="%.2f",
                        on_change=calculate_and_store_module_average, args=("s2", subject)
                    )
                with subcol_td:
                    st.number_input(
                        "TD",
                        key=td_key_s2,
                        min_value=0.0, max_value=20.0,
                        value=st.session_state.get(td_key_s2),
                        step=0.05, format="%.2f",
                        on_change=calculate_and_store_module_average, args=("s2", subject)
                    )
                with subcol_avg:
                    avg_val = float(st.session_state.get(module_avg_key_s2, 0.0))
                    avg_color = "#FF0000" # Red
                    if avg_val >= 15: avg_color = "#D89CF6" # Purple
                    elif avg_val >= 10: avg_color = "#50D890" # Green
                    elif avg_val >= 7: avg_color = "#4682B4" # SteelBlue
                    
                    module_avg_html = f"""
                    <div style="margin-top: -0.18rem;">
                        <label class='module-average-label'>Moyenne</label>
                        <div class="module-average-display" style="color: {avg_color};">
                            {avg_val:.2f}
                        </div>
                    </div>
                    """
                    st.markdown(module_avg_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col_s2_1, btn_col_s2_2, btn_col_s2_3 = st.columns([1, 2, 1])
    with btn_col_s2_2:
        st.markdown('<div class="s2-button">', unsafe_allow_html=True)
        if st.button("Calculer Moyenne S2", key="s2_calc"):
            calculate_s2_average()
        st.markdown('</div>', unsafe_allow_html=True)
