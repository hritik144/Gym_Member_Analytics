import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
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
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('gym_members_exercise_tracking.csv')
    return df

# Load or create model
@st.cache_resource
def load_or_create_model(df):
    try:
        # Suppress the version warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = joblib.load('model (2).pkl')
        return model
    except:
        st.info("Creating prediction model from data...")
        
        # Prepare features for training
        X = df[['Age', 'Weight (kg)', 'Height (m)', 'Max_BPM', 'Avg_BPM', 
                'Resting_BPM', 'Session_Duration (hours)', 'Fat_Percentage', 
                'Water_Intake (liters)', 'Workout_Frequency (days/week)', 
                'Experience_Level', 'BMI']].copy()
        
        # One-hot encode Workout_Type
        workout_dummies = pd.get_dummies(df['Workout_Type'], prefix='workout')
        X = pd.concat([X, workout_dummies], axis=1)
        
        # One-hot encode Gender
        X['Gender_Male'] = (df['Gender'] == 'Male').astype(int)
        
        y = df['Calories_Burned']
        
        model = LinearRegression()
        model.fit(X, y)
        return model

# Filter data function
def filter_data(df, genders, workouts, experience, age_range):
    mask = (
        df['Gender'].isin(genders) &
        df['Workout_Type'].isin(workouts) &
        df['Experience_Level'].isin(experience) &
        (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])
    )
    return df[mask]

# Load data
df = load_data()
model = load_or_create_model(df)

# Sidebar filters
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
        format_func=lambda x: {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}[x],
        default=[1, 2, 3]
    )
    
    st.markdown("---")
    
    # Filter data
    filtered_df = filter_data(df, genders, workouts, experience, age_range)
    st.metric("Total Members", len(filtered_df))

# Main content
st.markdown('<div class="main-header">Gym Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Performance · Health · AI Predictions</div>', unsafe_allow_html=True)

# KPIs
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
            <div class="kpi-label">Avg Calories/Session</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    avg_dur = filtered_df['Session_Duration (hours)'].mean()
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_dur:.1f}h</div>
            <div class="kpi-label">Avg Duration (hrs)</div>
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
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💪 Performance", "🏃 Workouts", "🤖 Predict"])

# Tab 1: Overview
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Age Distribution by Workout Type")
        # Create age groups with string labels instead of Interval objects
        filtered_df['Age_Group'] = pd.cut(filtered_df['Age'], bins=8)
        # Convert Interval to string labels
        filtered_df['Age_Group_Label'] = filtered_df['Age_Group'].astype(str)
        age_workout_pivot = filtered_df.groupby(['Age_Group_Label', 'Workout_Type']).size().unstack(fill_value=0)
        st.bar_chart(age_workout_pivot)
        
        st.subheader("📈 Experience Level Distribution")
        exp_counts = filtered_df['Experience_Level'].value_counts().sort_index()
        exp_counts.index = exp_counts.index.map({1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'})
        st.bar_chart(exp_counts)
    
    with col2:
        st.subheader("🏋️ Workout Type Distribution")
        workout_counts = filtered_df['Workout_Type'].value_counts()
        st.bar_chart(workout_counts)
        
        st.subheader("⚖️ BMI by Workout Type")
        bmi_by_workout = filtered_df.groupby(['Workout_Type', 'Gender'])['BMI'].mean().unstack()
        st.bar_chart(bmi_by_workout)

# Tab 2: Performance
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Average Calories by Workout Type")
        cal_by_workout = filtered_df.groupby('Workout_Type')['Calories_Burned'].mean().sort_values(ascending=False)
        st.bar_chart(cal_by_workout)
        
        st.subheader("📈 Calories vs Session Duration")
        # Create duration bins with string labels
        filtered_df['Duration_Bin'] = pd.cut(filtered_df['Session_Duration (hours)'], bins=10)
        filtered_df['Duration_Label'] = filtered_df['Duration_Bin'].astype(str)
        dur_cal = filtered_df.groupby('Duration_Label')['Calories_Burned'].mean()
        st.line_chart(dur_cal)
    
    with col2:
        st.subheader("❤️ Heart Rate Metrics by Workout")
        bpm_data = filtered_df.groupby('Workout_Type')[['Max_BPM', 'Avg_BPM', 'Resting_BPM']].mean()
        st.bar_chart(bpm_data)
        
        st.subheader("💧 Water Intake vs Calories")
        filtered_df['Water_Bin'] = pd.cut(filtered_df['Water_Intake (liters)'], bins=10)
        filtered_df['Water_Label'] = filtered_df['Water_Bin'].astype(str)
        water_cal = filtered_df.groupby('Water_Label')['Calories_Burned'].mean()
        st.line_chart(water_cal)
    
    # Correlation matrix
    st.subheader("📊 Feature Correlations")
    numeric_cols = ['Age', 'Weight (kg)', 'Max_BPM', 'Avg_BPM', 
                   'Session_Duration (hours)', 'Calories_Burned', 
                   'Fat_Percentage', 'Water_Intake (liters)', 
                   'Workout_Frequency (days/week)', 'BMI']
    
    corr_matrix = filtered_df[numeric_cols].corr()
    
    # Display correlation as a styled dataframe
    st.dataframe(
        corr_matrix.style.background_gradient(cmap='coolwarm', axis=None)
        .format(precision=2)
    )

# Tab 3: Workouts
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Workout Frequency Distribution")
        freq_counts = filtered_df['Workout_Frequency (days/week)'].value_counts().sort_index()
        st.bar_chart(freq_counts)
        
        st.subheader("🏃 Calories by Gender & Workout")
        cal_gender = filtered_df.groupby(['Workout_Type', 'Gender'])['Calories_Burned'].mean().unstack()
        st.bar_chart(cal_gender)
    
    with col2:
        st.subheader("🧈 Average Fat % by Experience Level")
        fat_exp = filtered_df.groupby(['Experience_Level', 'Gender'])['Fat_Percentage'].mean().unstack()
        fat_exp.index = fat_exp.index.map({1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'})
        st.bar_chart(fat_exp)
        
        st.subheader("📊 Workout Frequency vs Calories")
        freq_cal = filtered_df.groupby('Workout_Frequency (days/week)')['Calories_Burned'].mean()
        st.line_chart(freq_cal)

# Tab 4: Predict
with tab4:
    st.markdown("### 🤖 AI Calorie Predictor")
    st.markdown("Adjust the parameters below to estimate your calories burned per session")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👤 Personal Information")
        age = st.slider("Age", 18, 70, 30, key="age")
        weight = st.slider("Weight (kg)", 40.0, 140.0, 70.0, 0.5, key="weight")
        height = st.slider("Height (m)", 1.40, 2.10, 1.70, 0.01, key="height")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        workout_type = st.selectbox("Workout Type", ["HIIT", "Cardio", "Strength", "Yoga"], key="workout")
        experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"], key="exp")
        
    with col2:
        st.markdown("#### ❤️ Heart Rate & Duration")
        max_bpm = st.slider("Max BPM", 130, 210, 175, key="max_bpm")
        avg_bpm = st.slider("Avg BPM", 100, 200, 145, key="avg_bpm")
        resting_bpm = st.slider("Resting BPM", 40, 90, 60, key="resting_bpm")
        duration = st.slider("Session Duration (hours)", 0.5, 3.0, 1.0, 0.1, key="duration")
        
    with col3:
        st.markdown("#### 💪 Body Composition & Habits")
        fat_percentage = st.slider("Body Fat %", 5.0, 45.0, 25.0, 0.5, key="fat")
        water_intake = st.slider("Water Intake (L/day)", 1.0, 4.0, 2.5, 0.1, key="water")
        workout_freq = st.slider("Workout Frequency (days/week)", 1, 7, 3, key="freq")
    
    # Calculate BMI
    bmi = weight / (height ** 2)
    
    # Prepare features for prediction
    gender_val = 1 if gender == "Male" else 0
    exp_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    exp_val = exp_map[experience]
    
    # Create feature vector
    features = {
        'Age': age,
        'Weight (kg)': weight,
        'Height (m)': height,
        'Max_BPM': max_bpm,
        'Avg_BPM': avg_bpm,
        'Resting_BPM': resting_bpm,
        'Session_Duration (hours)': duration,
        'Fat_Percentage': fat_percentage,
        'Water_Intake (liters)': water_intake,
        'Workout_Frequency (days/week)': workout_freq,
        'Experience_Level': exp_val,
        'BMI': bmi,
        f'workout_{workout_type}': 1,
        'Gender_Male': gender_val
    }
    
    # Add zero for other workout types
    for wt in ['HIIT', 'Cardio', 'Strength', 'Yoga']:
        if f'workout_{wt}' not in features:
            features[f'workout_{wt}'] = 0
    
    # Ensure all features are in the correct order
    expected_features = ['Age', 'Weight (kg)', 'Height (m)', 'Max_BPM', 'Avg_BPM', 
                         'Resting_BPM', 'Session_Duration (hours)', 'Fat_Percentage', 
                         'Water_Intake (liters)', 'Workout_Frequency (days/week)', 
                         'Experience_Level', 'BMI', 'workout_HIIT', 'workout_Cardio', 
                         'workout_Strength', 'workout_Yoga', 'Gender_Male']
    
    feature_vector = np.array([[features[f] for f in expected_features]])
    
    # Make prediction
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            prediction = model.predict(feature_vector)[0]
    except:
        # Fallback prediction formula
        prediction = (duration * 200) + (max_bpm * 2) + (avg_bpm * 1.5) + (weight * 3)
    
    prediction = max(100, min(3000, prediction))
    
    # Calculate peer comparison
    peer_data = filtered_df[
        (filtered_df['Workout_Type'] == workout_type) & 
        (abs(filtered_df['Age'] - age) <= 5)
    ]
    peer_avg = peer_data['Calories_Burned'].mean() if len(peer_data) > 0 else prediction
    diff = prediction - peer_avg
    
    # Display predictions
    st.markdown("---")
    
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    
    with pred_col1:
        st.markdown(f"""
            <div class="prediction-card">
                <div class="kpi-label">🔥 Estimated Calories Burned</div>
                <div class="prediction-value">{prediction:.0f}</div>
                <div style="color: #6b8cae; font-size: 0.75rem;">kcal per session</div>
            </div>
        """, unsafe_allow_html=True)
    
    with pred_col2:
        diff_color = "green" if diff >= 0 else "red"
        diff_symbol = "▲" if diff >= 0 else "▼"
        st.markdown(f"""
            <div class="prediction-card">
                <div class="kpi-label">📊 vs. Similar Members</div>
                <div style="font-size: 2rem; font-weight: 800; color: {diff_color}">
                    {diff_symbol} {abs(diff):.0f}
                </div>
                <div style="color: #6b8cae; font-size: 0.75rem;">peer avg: {peer_avg:.0f} kcal</div>
            </div>
        """, unsafe_allow_html=True)
    
    with pred_col3:
        st.markdown(f"""
            <div class="prediction-card">
                <div class="kpi-label">📅 Weekly & Monthly Burn</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #a855f7">
                    {prediction * workout_freq:.0f}
                </div>
                <div style="color: #6b8cae; font-size: 0.75rem;">
                    weekly | ~{prediction * workout_freq * 4.33:.0f} monthly
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Additional metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Your BMI", f"{bmi:.1f}", 
                  delta=f"{bmi - filtered_df['BMI'].mean():.1f} vs avg",
                  delta_color="inverse")
    with metric_col2:
        st.metric("Body Fat", f"{fat_percentage:.1f}%",
                  delta=f"{fat_percentage - filtered_df['Fat_Percentage'].mean():.1f} vs avg")
    with metric_col3:
        st.metric("Weekly Workouts", f"{workout_freq} days",
                  delta=f"{workout_freq - filtered_df['Workout_Frequency (days/week)'].mean():.1f} vs avg")
    
    # Distribution chart
    st.markdown("---")
    st.subheader(f"📊 Calories Distribution for {workout_type} Members")
    
    workout_data = filtered_df[filtered_df['Workout_Type'] == workout_type]['Calories_Burned']
    if len(workout_data) > 0:
        # Create histogram bins
        hist_values, bin_edges = np.histogram(workout_data, bins=15)
        
        # Convert to DataFrame for bar chart with proper labels
        hist_df = pd.DataFrame({
            'Range': [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)],
            'Count': hist_values
        })
        
        st.bar_chart(hist_df.set_index('Range'))
        
        # Add info about where the user falls
        percentile = (workout_data < prediction).mean() * 100
        st.info(f"💡 Your predicted value of {prediction:.0f} kcal is higher than {percentile:.0f}% of {workout_type} members.")
    else:
        st.warning(f"No data available for {workout_type} workout type with current filters.")
