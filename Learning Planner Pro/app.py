import streamlit as st
import datetime
import time
import requests
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# Importing logic functions
from logic import *

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="Learning Planner Pro", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MAGIC START EFFECT (Har baar start hone par) ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("<h1 style='text-align: center; margin-top: 20%;'>✨ Initializing Your Magic Planner...</h1>", unsafe_allow_html=True)
        st.snow() # Sparkle effect ki jagah snow (magic feel)
        time.sleep(1.5)
    placeholder.empty()

# --- 3. LOAD ASSETS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_success = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_qc9scvqy.json")

# --- 4. MODERN GOOGLE CSS (Bigger Fonts) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Google Sans', sans-serif !important;
        font-size: 18px !important; /* Font size badha diya gaya hai */
    }

    h1 { font-size: 42px !important; }
    h2 { font-size: 32px !important; }
    h3 { font-size: 26px !important; }
    p { font-size: 19px !important; }

    /* Modern Card UI */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px;
    }

    /* Metric Font Fix */
    [data-testid="stMetricValue"] { font-size: 35px !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- 5. INITIALIZATION ---
if 'creds' not in st.session_state:
    from main import authentication
    st.session_state.creds = authentication()

# --- 6. TOP NAVIGATION ---
selected = option_menu(
    menu_title=None, 
    options=["Dashboard", "Add Task", "Assignments", "Tools", "System"],
    icons=["house-heart", "plus-circle", "book", "grid-3x3-gap", "gear"],
    orientation="horizontal",
    styles={
        "container": {"padding": "10px", "background-color": "#ffffff"},
        "nav-link": {"font-size": "18px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#4285f4", "color": "white", "border-radius": "12px"},
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# --- 7. PAGE CONTENT ---

if selected == "Dashboard":
    st.markdown("## 📈 Welcome to Your Command Center")
    events = get_upcoming_events(st.session_state.creds)
    assigns = get_assignments(st.session_state.creds, True)
    
    e_list = [e for e in events if e[0] and e[0] != "no_event_id"]
    a_list = [a for a in assigns if a[0]]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tasks Today", len(e_list))
    m2.metric("Pending Work", len(a_list))
    m3.metric("Study Goal", "92%")
    m4.metric("Focus Score", "High")

    st.divider()
    
    l_col, r_col = st.columns([2, 1])
    with l_col:
        st.markdown("### 🚀 Today's Action Plan")
        if not e_list:
            st.success("Everything is clear! ✨ Go grab a coffee.")
        else:
            for task in e_list:
                with st.container(border=True):
                    c1, c2 = st.columns([0.1, 0.9])
                    if c1.checkbox("", key=f"dash_{task[0]}"):
                        delete_task(st.session_state.creds, task[0])
                        if lottie_success: st_lottie(lottie_success, height=150, key=f"l_{task[0]}")
                        st.toast(f"Completed: {task[1]}")
                        time.sleep(1.2)
                        st.rerun()
                    c2.markdown(f"**{task[1]}**")

    with r_col:
        st.markdown("### 🚩 Deadlines")
        for a in a_list:
            with st.container(border=True):
                st.write(f"**{a[1]}**")
                if st.button("Mark Done", key=f"btn_{a[0]}", use_container_width=True):
                    delete_task(st.session_state.creds, a[0])
                    st.balloons()
                    time.sleep(1)
                    st.rerun()

elif selected == "Tools":
    st.markdown("## 🛠️ Supercharger Tools")
    t1, t2, t3 = st.tabs(["📊 CGPA Heatmap", "🧮 Smart Calculator", "⏲️ Focus Timer"])
    
    with t1:
        st.markdown("### Subject-wise Performance Heatmap")
        with st.container(border=True):
            # Input for subjects and marks
            data_input = st.text_area("Enter Subjects & Marks (Subject:Mark format, one per line)", 
                                     "Maths:85\nPhysics:92\nCS:95\nEnglish:78\nChemistry:88")
            if st.button("Generate Analytics"):
                try:
                    subjects = []
                    marks = []
                    for line in data_input.split('\n'):
                        s, m = line.split(':')
                        subjects.append(s.strip())
                        marks.append(float(m.strip()))
                    
                    # Creating Heatmap Data
                    df = pd.DataFrame({"Subject": subjects, "Score": marks})
                    df["Category"] = "Current Semester"
                    
                    fig = px.density_heatmap(df, x="Subject", y="Category", z="Score", 
                                             text_auto=True, color_continuous_scale="Viridis")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    avg = np.mean(marks)
                    st.info(f"Your Average Score: **{avg:.2f}%**")
                except:
                    st.error("Please enter in 'Subject:Mark' format.")

    with t2:
        st.markdown("### Quick Calculator")
        with st.container(border=True):
            exp = st.text_input("Enter your expression (e.g., 55 * 12 + 100)")
            if exp:
                try:
                    result = eval(exp)
                    st.markdown(f"#### Result: `{result}`")
                except:
                    st.error("Invalid expression.")

    with t3:
        st.markdown("### Pomodoro Timer")
        if st.button("Start 25-Min Focus"):
            with st.empty():
                for i in range(25*60, 0, -1):
                    mins, secs = divmod(i, 60)
                    st.header(f"⏳ {mins:02d}:{secs:02d}")
                    time.sleep(1)
                st.success("Session Over! Take a 5-min break.")

elif selected == "Add Task":
    st.markdown("## 📋 Schedule New Activity")
    with st.container(border=True):
        with st.form("task_f"):
            title = st.text_input("Activity Name")
            module = st.selectbox("Category", ["General", "Studies", "Project", "Personal"])
            c1, c2, c3 = st.columns(3)
            d = c1.date_input("Date")
            s = c2.time_input("Starts")
            e = c3.time_input("Ends")
            if st.form_submit_button("Add to Calendar", use_container_width=True):
                add_task(st.session_state.creds, title, module, str(s), str(e), str(d))
                st.success("Synchronized! ✨")

elif selected == "Assignments":
    st.markdown("## 📥 Log Assignment")
    with st.container(border=True):
        with st.form("as_f"):
            title = st.text_input("Topic Name")
            d_col, t_col = st.columns(2)
            due_d = d_col.date_input("Deadline")
            due_t = t_col.time_input("Time")
            if st.form_submit_button("Save Assignment", use_container_width=True):
                add_assignment(st.session_state.creds, title, "General", str(due_d), str(due_t))
                st.success("Logged successfully!")

elif selected == "System":
    st.markdown("## ⚙️ Control Panel")
    with st.container(border=True):
        if st.button("Hard Refresh App"):
            st.session_state.clear()
            st.rerun()
        st.write("App Version: 2.0.0 (Professional)")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #757575;'>✨ Built with focus for students ✨</p>", unsafe_allow_html=True)