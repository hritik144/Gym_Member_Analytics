import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FitIQ Pro - Gym Analytics Dashboard",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #070c18 0%, #0d1b2a 100%);
    }

    .main-header {
        font-family: 'Syne', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #a855f7, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 0.8rem;
        color: #6b8cae;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, #111827 0%, #1a2740 100%);
        border: 1px solid #1e3a5f;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #e8eaf6;
        line-height: 1;
    }

    .kpi-label {
        font-size: 0.68rem;
        color: #6b8cae;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }

    .prediction-card {
        background: linear-gradient(135deg, #0f2744 0%, #1a3a5c 100%);
        border: 1px solid rgba(0,212,255,0.25);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }

    .prediction-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1a2740 100%);
        border: 1px solid #1e3a5f;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #00d4ff;
    }

    .metric-label {
        font-size: 0.7rem;
        color: #6b8cae;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('gym_members_exercise_tracking.csv')
    return df

# Prediction function
def predict_calories(
    age, weight, height, max_bpm, avg_bpm, resting_bpm,
    duration, fat_percentage, water_intake,
    workout_freq, experience, workout_type, gender, bmi
):

    workout_base = {
        'HIIT': 450,
        'Cardio': 380,
        'Strength': 350,
        'Yoga': 280
    }

    calories = workout_base.get(workout_type, 350)

    calories += duration * 350

    if age < 30:
        calories += 50
    elif age > 50:
        calories -= 50

    calories += (weight - 70) * 3

    calories += (avg_bpm - 140) * 2
    calories += (max_bpm - 170) * 1.5

    if bmi > 30:
        calories += 30
    elif bmi < 20:
        calories -= 30

    calories -= (fat_percentage - 25) * 3

    exp_factor = {
        1: -20,
        2: 0,
        3: 30
    }

    calories += exp_factor.get(experience, 0)

    if gender == "Male":
        calories += 40

    calories += (water_intake - 2.5) * 30
    calories += (workout_freq - 3) * 15

    calories = max(150, min(2000, calories))

    return int(calories)

# Filter function
def filter_data(df, genders, workouts, experience, age_range):

    mask = (
        df['Gender'].isin(genders) &
        df['Workout_Type'].isin(workouts) &
        df['Experience_Level'].isin(experience) &
        (df['Age'] >= age_range[0]) &
        (df['Age'] <= age_range[1])
    )

    return df[mask]

# Load dataset
df = load_data()

# Sidebar
with st.sidebar:

    st.markdown("## 🔥 FitIQ Pro")
    st.markdown("### Gym Intelligence")
    st.markdown("---")

    st.markdown("#### 🎯 Gender")

    genders = st.multiselect(
        "Select Gender",
        options=['Male', 'Female'],
        default=['Male', 'Female']
    )

    st.markdown("#### 💪 Workout Type")

    workouts = st.multiselect(
        "Select Workout Type",
        options=['HIIT', 'Cardio', 'Strength', 'Yoga'],
        default=['HIIT', 'Cardio', 'Strength', 'Yoga']
    )

    st.markdown("#### 🎂 Age Range")

    age_range = st.slider(
        "Age Range",
        min_value=18,
        max_value=59,
        value=(18, 59)
    )

    st.markdown("#### ⭐ Experience Level")

    experience = st.multiselect(
        "Select Experience",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: 'Beginner',
            2: 'Intermediate',
            3: 'Advanced'
        }[x],
        default=[1, 2, 3]
    )

    st.markdown("---")

    filtered_df = filter_data(
        df,
        genders,
        workouts,
        experience,
        age_range
    )

    st.metric("📊 Total Members", len(filtered_df))

# Header
st.markdown(
    '<div class="main-header">🏋️ Gym Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">Performance · Health · AI Predictions</div>',
    unsafe_allow_html=True
)

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{len(filtered_df):,}</div>
        <div class="kpi-label">Total Members</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_cal = filtered_df['Calories_Burned'].mean()

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_cal:.0f}</div>
        <div class="kpi-label">Avg Calories</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_dur = filtered_df['Session_Duration (hours)'].mean()

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_dur:.1f}h</div>
        <div class="kpi-label">Avg Duration</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_bmi = filtered_df['BMI'].mean()

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_bmi:.1f}</div>
        <div class="kpi-label">Avg BMI</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    avg_fat = filtered_df['Fat_Percentage'].mean()

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_fat:.1f}%</div>
        <div class="kpi-label">Avg Fat %</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "💪 Performance",
    "🏃 Workouts",
    "🤖 Predict"
])

# Overview Tab
with tab1:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Age Distribution by Workout")

        filtered_df['Age_Group'] = pd.cut(
            filtered_df['Age'],
            bins=6
        )

        filtered_df['Age_Group_Label'] = (
            filtered_df['Age_Group'].astype(str)
        )

        age_workout = filtered_df.groupby(
            ['Age_Group_Label', 'Workout_Type']
        ).size().unstack(fill_value=0)

        st.bar_chart(age_workout)

        st.subheader("📈 Experience Distribution")

        exp_counts = (
            filtered_df['Experience_Level']
            .value_counts()
            .sort_index()
        )

        exp_counts.index = exp_counts.index.map({
            1: 'Beginner',
            2: 'Intermediate',
            3: 'Advanced'
        })

        st.bar_chart(exp_counts)

    with col2:

        st.subheader("🏋️ Workout Distribution")

        workout_counts = (
            filtered_df['Workout_Type']
            .value_counts()
        )

        st.bar_chart(workout_counts)

        st.subheader("⚖️ BMI by Workout")

        bmi_workout = filtered_df.groupby(
            ['Workout_Type', 'Gender']
        )['BMI'].mean().unstack()

        st.bar_chart(bmi_workout)

# Performance Tab
with tab2:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🔥 Calories by Workout")

        cal_workout = filtered_df.groupby(
            'Workout_Type'
        )['Calories_Burned'].mean()

        st.bar_chart(cal_workout)

        st.subheader("📈 Calories vs Duration")

        filtered_df['Duration_Bin'] = pd.cut(
            filtered_df['Session_Duration (hours)'],
            bins=8
        )

        filtered_df['Duration_Label'] = (
            filtered_df['Duration_Bin'].astype(str)
        )

        duration_cal = filtered_df.groupby(
            'Duration_Label'
        )['Calories_Burned'].mean()

        st.line_chart(duration_cal)

    with col2:

        st.subheader("❤️ BPM Metrics")

        bpm_data = filtered_df.groupby(
            'Workout_Type'
        )[['Max_BPM', 'Avg_BPM', 'Resting_BPM']].mean()

        st.bar_chart(bpm_data)

        st.subheader("💧 Water Intake vs Calories")

        filtered_df['Water_Bin'] = pd.cut(
            filtered_df['Water_Intake (liters)'],
            bins=8
        )

        filtered_df['Water_Label'] = (
            filtered_df['Water_Bin'].astype(str)
        )

        water_cal = filtered_df.groupby(
            'Water_Label'
        )['Calories_Burned'].mean()

        st.line_chart(water_cal)

    st.subheader("📊 Metrics Summary")

    summary_data = []

    for workout in filtered_df['Workout_Type'].unique():

        workout_data = filtered_df[
            filtered_df['Workout_Type'] == workout
        ]

        summary_data.append({
            'Workout Type': workout,
            'Avg Calories': f"{workout_data['Calories_Burned'].mean():.0f}",
            'Avg Duration': f"{workout_data['Session_Duration (hours)'].mean():.1f}h",
            'Avg BPM': f"{workout_data['Avg_BPM'].mean():.0f}",
            'Members': len(workout_data)
        })

    summary_df = pd.DataFrame(summary_data)

    # FIXED HERE
    st.dataframe(summary_df, width="stretch")
