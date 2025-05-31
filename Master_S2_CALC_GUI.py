import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

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
        background: linear-gradient(135deg, #0e1118 0%, #1a1d2e 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        font-weight: bold;
        box-shadow: 0 8px 32px rgba(255, 129, 47, 0.3);
        border: 1px solid rgba(255, 129, 47, 0.2);
    }
    .subject-header {
        font-size: 1.2rem;
        padding: 0.8rem;
        border-radius: 10px;
        margin-top: 1rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .subject-header:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .s1-header {
        color: #2fffe9;
        border-left: 4px solid #2fffe9;
    }
    .s2-header {
        color: #ff812f;
        border-left: 4px solid #ff812f;
    }
    .stButton > button {
        width: 100%;
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    .s1-button > button {
        background: linear-gradient(135deg, #2fffe9 0%, #00d4aa 100%);
        color: #0e1118 !important;
    }
    .s2-button > button {
        background: linear-gradient(135deg, #ff812f 0%, #ff6b1a 100%);
        color: white !important;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(72, 187, 120, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(72, 187, 120, 0.3);
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 8px 32px rgba(72, 187, 120, 0.2);
    }
    
    /* Module Average Box Styles */
    .module-avg-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
    }
    .module-avg-box {
        flex: 1;
        min-width: 250px;
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 2px solid;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .module-avg-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    .module-avg-box:hover::before {
        left: 100%;
    }
    .module-avg-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    .avg-fail {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
        border-color: #ff0000;
        color: #ff6b6b;
    }
    .avg-pass {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
        border-color: #3b82f6;
        color: #60a5fa;
    }
    .avg-good {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(22, 163, 74, 0.05) 100%);
        border-color: #22c55e;
        color: #4ade80;
    }
    .avg-excellent {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(147, 51, 234, 0.05) 100%);
        border-color: #a855f7;
        color: #c084fc;
    }
    
    /* Grade Progress Bar */
    .grade-progress {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .grade-progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease, background 0.3s ease;
    }
    
    /* Achievement Badges */
    .achievement-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.25rem;
        animation: pulse 2s infinite;
    }
    .badge-excellent {
        background: linear-gradient(135deg, #a855f7, #7c3aed);
        color: white;
    }
    .badge-good {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
    }
    .badge-pass {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px currentColor; }
        50% { box-shadow: 0 0 20px currentColor; }
    }
    
    /* Corner GIF Styles */
    .corner-gif {
        position: fixed;
        top: 85px;
        right: 10px;
        z-index: 9999;
        width: 80px;
        height: 80px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        opacity: 0.8;
        transition: all 0.3s ease;
    }
    .corner-gif:hover {
        opacity: 1;
        transform: scale(1.15) rotate(5deg);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background: linear-gradient(135deg, #262730 0%, #1a1d2e 100%);
        border-radius: 15px 15px 0px 0px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff812f 0%, #ff6b1a 100%);
        box-shadow: 0 4px 15px rgba(255, 129, 47, 0.3);
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Dark mode toggle */
    .theme-toggle {
        position: fixed;
        top: 150px;
        right: 10px;
        z-index: 9999;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .theme-toggle:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: rotate(180deg);
    }
    </style>
    """, unsafe_allow_html=True)

# Add the corner GIF and theme toggle
st.markdown("""
    <img src="https://i.gifer.com/XOsX.gif" class="corner-gif" alt="Finance GIF">
    <div class="theme-toggle" onclick="toggleTheme()">
        🌓
    </div>
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

def get_grade_color_class(grade):
    """Return CSS class based on grade"""
    if grade < 7:
        return "avg-fail"
    elif 7 <= grade < 10:
        return "avg-pass"
    elif 10 <= grade < 15:
        return "avg-good"
    else:
        return "avg-excellent"

def get_achievement_badge(grade):
    """Return achievement badge based on grade"""
    if grade >= 15:
        return '<span class="achievement-badge badge-excellent">🏆 Excellence!</span>'
    elif grade >= 12:
        return '<span class="achievement-badge badge-good">⭐ Great Job!</span>'
    elif grade >= 10:
        return '<span class="achievement-badge badge-pass">✅ Well Done!</span>'
    return ""

def create_grade_progress_bar(grade, max_grade=20):
    """Create a progress bar for grade visualization"""
    percentage = min((grade / max_grade) * 100, 100)
    if grade < 7:
        color = "#ff0000"
    elif grade < 10:
        color = "#3b82f6"
    elif grade < 15:
        color = "#22c55e"
    else:
        color = "#a855f7"
    
    return f"""
    <div class="grade-progress">
        <div class="grade-progress-fill" style="width: {percentage}%; background: linear-gradient(90deg, {color}, {color}aa);"></div>
    </div>
    """

def display_module_averages(subjects_data, semester="S1"):
    """Display individual module averages with real-time color coding"""
    st.markdown('<div class="module-avg-container">', unsafe_allow_html=True)
    
    for subject, data in subjects_data.items():
        if data['exam'] is not None and data['td'] is not None and (data['exam'] > 0 or data['td'] > 0):
            module_avg = (data['exam'] * 0.67) + (data['td'] * 0.33)
            color_class = get_grade_color_class(module_avg)
            badge = get_achievement_badge(module_avg)
            progress_bar = create_grade_progress_bar(module_avg)
            
            st.markdown(f"""
            <div class="module-avg-box {color_class}">
                <h4 style="margin: 0 0 0.5rem 0; font-size: 1rem;">{subject}</h4>
                <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                    {module_avg:.2f}/20
                </div>
                {progress_bar}
                <div style="font-size: 0.8rem; opacity: 0.8;">
                    Exam: {data['exam']:.1f} | TD: {data['td']:.1f}
                </div>
                {badge}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_grade_chart(subjects_data, title):
    """Create a radar chart for grade visualization"""
    subjects = []
    grades = []
    
    for subject, data in subjects_data.items():
        if data['exam'] is not None and data['td'] is not None and (data['exam'] > 0 or data['td'] > 0):
            subjects.append(subject[:15] + "..." if len(subject) > 15 else subject)
            grades.append((data['exam'] * 0.67) + (data['td'] * 0.33))
    
    if subjects and grades:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=grades,
            theta=subjects,
            fill='toself',
            name='Grades',
            line_color='#ff812f',
            fillcolor='rgba(255, 129, 47, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 20],
                    tickfont=dict(color='white'),
                    gridcolor='rgba(255, 255, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='white', size=10)
                )
            ),
            showlegend=False,
            title=dict(text=title, font=dict(color='white', size=16)),
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

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

    # Display module averages in real-time
    st.markdown("### 📊 Module Averages")
    display_module_averages(subjects_data, "S1")

    total = 0
    valid_subjects = 0
    for subject, grades in subjects_data.items():
        if grades["exam"] > 0 or grades["td"] > 0:
            average = (grades["exam"] * 0.67) + (grades["td"] * 0.33)
            weight = 4.5 if subject in ["Statistiques Inférentielles", "Comptabilité Financière", "Management", "Marketing"] else 3
            total += average * weight
            valid_subjects += 1

    if valid_subjects > 0:
        semester_average = total / 30
        formatted_float = "{:.2f}".format(semester_average)
        badge = get_achievement_badge(semester_average)
        progress_bar = create_grade_progress_bar(semester_average)
        
        # Determine status and color
        status = "🔴 Below Passing" if semester_average < 10 else "🟢 Passing"
        if semester_average >= 15:
            status = "🟣 Excellent!"
        elif semester_average >= 12:
            status = "🟢 Very Good!"
        
        st.markdown(f"""
            <div class="result-box">
                <h3 style="color: #2F855A; margin: 0;">📊 S1 Results</h3>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">
                    Moyenne S1: <strong style="color: #2fffe9">{formatted_float}/20</strong><br>
                    Status: <strong>{status}</strong>
                </p>
                {progress_bar}
                {badge}
            </div>
        """, unsafe_allow_html=True)
        
        # Create visualization
        create_grade_chart(subjects_data, "S1 Grades Overview")

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

    # Display module averages in real-time
    st.markdown("### 📊 Module Averages")
    display_module_averages(subjects_data, "S2")

    total_weighted_sum = 0
    total_credits = sum(s2_subjects_with_coef.values())
    valid_subjects = 0
    
    for subject, data in subjects_data.items():
        if data["exam"] > 0 or data["td"] > 0:
            average = (data["exam"] * 0.67) + (data["td"] * 0.33)
            total_weighted_sum += average * data["coef"]
            valid_subjects += 1

    if valid_subjects > 0:
        semester_average = total_weighted_sum / total_credits
        formatted_float = "{:.2f}".format(semester_average)
        badge = get_achievement_badge(semester_average)
        progress_bar = create_grade_progress_bar(semester_average)
        
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
        
        # Determine status
        status = "🔴 Below Passing" if semester_average < 10 else "🟢 Passing"
        if semester_average >= 15:
            status = "🟣 Excellent!"
        elif semester_average >= 12:
            status = "🟢 Very Good!"
        
        st.markdown(f"""
            <div class="result-box">
                <h3 style="color: #2F855A; margin: 0;">📊 S2 Results</h3>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">
                    Moyenne S2: <strong style="color: {color}">{formatted_float}/20</strong><br>
                    Status: <strong>{status}</strong>
                </p>
                {progress_bar}
                {badge}
            </div>
        """, unsafe_allow_html=True)
        
        # Create visualization
        create_grade_chart(subjects_data, "S2 Grades Overview")

# Add real-time calculation functionality
def update_module_averages_realtime(semester):
    """Update module averages in real-time as user types"""
    if semester == "S1":
        subjects_data = {}
        for subject in s1_subjects:
            exam_key = f"s1_{subject}_exam"
            td_key = f"s1_{subject}_TD"
            exam_grade = st.session_state.get(exam_key, 0.0) or 0.0
            td_grade = st.session_state.get(td_key, 0.0) or 0.0
            if exam_grade > 0 or td_grade > 0:
                subjects_data[subject] = {"exam": exam_grade, "td": td_grade}
        
        if subjects_data:
            st.markdown("### 📊 Real-time Module Averages")
            display_module_averages(subjects_data, "S1")
    
    elif semester == "S2":
        subjects_data = {}
        for subject, coef in s2_subjects_with_coef.items():
            exam_key = f"s2_{subject}_exam"
            td_key = f"s2_{subject}_TD"
            exam_grade = st.session_state.get(exam_key, 0.0) or 0.0
            td_grade = st.session_state.get(td_key, 0.0) or 0.0
            if exam_grade > 0 or td_grade > 0:
                subjects_data[subject] = {"exam": exam_grade, "td": td_grade, "coef": coef}
        
        if subjects_data:
            st.markdown("### 📊 Real-time Module Averages")
            display_module_averages(subjects_data, "S2")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📚 Semestre 1", "📖 Semestre 2", "📈 Analytics"])

with tab1:
    st.markdown("### Semester 1 Calculator")
    
    # Real-time updates
    update_module_averages_realtime("S1")
    
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
                        max_value=20.0,
                        value=None,
                        step=0.05,
                        format="%.2f",
                        help="Enter your exam grade (0-20)"
                    )
                with subcol2:
                    st.number_input(
                        "TD",
                        key=f"s1_{subject}_TD",
                        min_value=0.0,
                        max_value=20.0,
                        value=None,
                        step=0.05,
                        format="%.2f",
                        help="Enter your TD grade (0-20)"
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="s1-button">', unsafe_allow_html=True)
        if st.button("🧮 Calculer Moyenne S1", key="s1_calc"):
            calculate_s1_average()
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### Semester 2 Calculator")
    
    # Real-time updates
    update_module_averages_realtime("S2")
    
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
                        max_value=20.0,
                        value=None,
                        step=0.05,
                        format="%.2f",
                        help="Enter your exam grade (0-20)"
                    )
                with subcol2:
                    st.number_input(
                        "TD",
                        key=f"s2_{subject}_TD",
                        min_value=0.0,
                        max_value=20.0,
                        value=None,
                        step=0.05,
                        format="%.2f",
                        help="Enter your TD grade (0-20)"
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="s2-button">', unsafe_allow_html=True)
        if st.button("🧮 Calculer Moyenne S2", key="s2_calc"):
            calculate_s2_average()
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 📈 Grade Analytics & Insights")
    
    # Statistics overview
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate some basic stats
    s1_grades = []
    s2_grades = []
    
    for subject in s1_subjects:
        exam = st.session_state.get(f"s1_{subject}_exam", 0) or 0
        td = st.session_state.get(f"s1_{subject}_TD", 0) or 0
        if exam > 0 or td > 0:
            s1_grades.append((exam * 0.67) + (td * 0.33))
    
    for subject in s2_subjects_with_coef.keys():
        exam = st.session_state.get(f"s2_{subject}_exam", 0) or 0
        td = st.session_state.get(f"s2_{subject}_TD", 0) or 0
        if exam > 0 or td > 0:
            s2_grades.append((exam * 0.67) + (td * 0.33))
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h4 style="margin: 0; color: #2fffe9;">📚 S1 Modules</h4>
            <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                {}/8
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Completed</div>
        </div>
        """.format(len(s1_grades)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h4 style="margin: 0; color: #ff812f;">📖 S2 Modules</h4>
            <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                {}/9
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Completed</div>
        </div>
        """.format(len(s2_grades)), unsafe_allow_html=True)
    
    with col3:
        avg_s1 = sum(s1_grades) / len(s1_grades) if s1_grades else 0
        st.markdown("""
        <div class="stats-card">
            <h4 style="margin: 0; color: #22c55e;">📊 S1 Average</h4>
            <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                {:.1f}/20
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Current</div>
        </div>
        """.format(avg_s1), unsafe_allow_html=True)
    
    with col4:
        avg_s2 = sum(s2_grades) / len(s2_grades) if s2_grades else 0
        st.markdown("""
        <div class="stats-card">
            <h4 style="margin: 0; color: #a855f7;">📊 S2 Average</h4>
            <div style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0;">
                {:.1f}/20
            </div>
            <div style="font-size: 0.8rem; opacity: 0.8;">Current</div>
        </div>
        """.format(avg_s2), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grade distribution charts
    if s1_grades or s2_grades:
        col1, col2 = st.columns(2)
        
        with col1:
            if s1_grades:
                st.markdown("#### 📊 S1 Grade Distribution")
                fig = px.histogram(
                    x=s1_grades, 
                    nbins=10, 
                    title="S1 Grades Distribution",
                    color_discrete_sequence=['#2fffe9']
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Grade",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if s2_grades:
                st.markdown("#### 📊 S2 Grade Distribution")
                fig = px.histogram(
                    x=s2_grades, 
                    nbins=10, 
                    title="S2 Grades Distribution",
                    color_discrete_sequence=['#ff812f']
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title="Grade",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Performance insights
    st.markdown("#### 🎯 Performance Insights")
    
    insights = []
    if s1_grades:
        excellent_s1 = len([g for g in s1_grades if g >= 15])
        good_s1 = len([g for g in s1_grades if 12 <= g < 15])
        pass_s1 = len([g for g in s1_grades if 10 <= g < 12])
        fail_s1 = len([g for g in s1_grades if g < 10])
        
        if excellent_s1 > 0:
            insights.append(f"🏆 You have {excellent_s1} excellent grade(s) in S1! Keep up the amazing work!")
        if fail_s1 > 0:
            insights.append(f"⚠️ {fail_s1} module(s) in S1 need attention. Consider extra study sessions.")
        if avg_s1 >= 15:
            insights.append("✨ S1 performance is outstanding! You're on track for honors!")
    
    if s2_grades:
        excellent_s2 = len([g for g in s2_grades if g >= 15])
        good_s2 = len([g for g in s2_grades if 12 <= g < 15])
        pass_s2 = len([g for g in s2_grades if 10 <= g < 12])
        fail_s2 = len([g for g in s2_grades if g < 10])
        
        if excellent_s2 > 0:
            insights.append(f"🌟 {excellent_s2} excellent grade(s) in S2! Outstanding performance!")
        if fail_s2 > 0:
            insights.append(f"📚 Focus needed on {fail_s2} S2 module(s). You can do this!")
        if avg_s2 >= 15:
            insights.append("🎉 S2 performance is exceptional! Academic excellence achieved!")
    
    if s1_grades and s2_grades:
        improvement = avg_s2 - avg_s1
        if improvement > 1:
            insights.append(f"📈 Great improvement from S1 to S2 (+{improvement:.1f} points)!")
        elif improvement < -1:
            insights.append(f"📉 S2 needs attention (S1→S2: {improvement:.1f} points). Let's bounce back!")
    
    if not insights:
        insights.append("📝 Enter more grades to see personalized insights!")
    
    for insight in insights:
        st.info(insight)
    
    # Grade prediction tool
    st.markdown("#### 🔮 Grade Prediction Tool")
    st.info("💡 **Coming Soon**: AI-powered grade prediction based on your current performance patterns!")
    
    # Study recommendations
    st.markdown("#### 📖 Study Recommendations")
    
    weak_subjects_s1 = [subject for subject in s1_subjects if st.session_state.get(f"s1_{subject}_exam", 0) and 
                       ((st.session_state.get(f"s1_{subject}_exam", 0) * 0.67) + 
                        (st.session_state.get(f"s1_{subject}_TD", 0) or 0) * 0.33) < 10]
    
    weak_subjects_s2 = [subject for subject in s2_subjects_with_coef.keys() if st.session_state.get(f"s2_{subject}_exam", 0) and 
                       ((st.session_state.get(f"s2_{subject}_exam", 0) * 0.67) + 
                        (st.session_state.get(f"s2_{subject}_TD", 0) or 0) * 0.33) < 10]
    
    if weak_subjects_s1 or weak_subjects_s2:
        st.warning("⚠️ **Priority Study Areas:**")
        for subject in weak_subjects_s1:
            st.write(f"• **S1 - {subject}**: Focus on understanding core concepts")
        for subject in weak_subjects_s2:
            st.write(f"• **S2 - {subject}**: Review material and practice exercises")
    else:
        st.success("✅ All entered grades are above passing threshold! Keep up the excellent work!")

# Add JavaScript for theme toggle (optional enhancement)
st.markdown("""
<script>
function toggleTheme() {
    // This would toggle between light and dark themes
    // Implementation would require additional CSS variables
    console.log('Theme toggle clicked!');
}

// Add some sparkle effects for excellent grades
function addSparkles() {
    // Create sparkle animation for grades above 15
    const excellentBoxes = document.querySelectorAll('.avg-excellent');
    excellentBoxes.forEach(box => {
        box.style.animation = 'glow 2s infinite alternate';
    });
}

// Run sparkles when page loads
setTimeout(addSparkles, 1000);
</script>
""", unsafe_allow_html=True)
