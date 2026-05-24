import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import os
from sklearn.linear_model import LinearRegression

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
    .main-header {
        font-family: 'Syne', sans-serif;
        font-size: 2.8rem;
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
        position: relative;
        overflow: hidden;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
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
        font-family: 'Syne', sans-serif;
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

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model (2).pkl')
        return model
    except:
        # Fallback to a simple linear regression if model file not found
        st.warning("Model file not found. Using default coefficients.")
        class DummyModel:
            def __init__(self):
                self.coef_ = np.array([-40.294, -41.213, -21.215, 13.952, 1.256, 88.655, 
                                        4.455, 240.020, -4.020, -2.127, 3.558, -2.695, 
                                        22.053, 1.701, -0.164, 0.255, -1.898])
                self.intercept_ = 904.024
            def predict(self, X):
                return np.dot(X, self.coef_) + self.intercept_
        return DummyModel()

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
model = load_model()

# Sidebar filters
with st.sidebar:
    st.markdown("## 🔥 FitIQ Pro")
    st.markdown("### Gym Intelligence")
    st.markdown("---")
    
    st.markdown("#### 🎯 Gender")
    genders = st.multiselect(
        "Select Gender",
        options=['Male', 'Female'],
        default=['Male', 'Female'],
        label_visibility="collapsed"
    )
    
    st.markdown("#### 💪 Workout Type")
    workouts = st.multiselect(
        "Select Workout Type",
        options=['HIIT', 'Cardio', 'Strength', 'Yoga'],
        default=['HIIT', 'Cardio', 'Strength', 'Yoga'],
        label_visibility="collapsed"
    )
    
    st.markdown("#### 🎂 Age Range")
    age_range = st.slider(
        "Age Range",
        min_value=18,
        max_value=59,
        value=(18, 59),
        label_visibility="collapsed"
    )
    
    st.markdown("#### ⭐ Experience Level")
    experience = st.multiselect(
        "Select Experience",
        options=[1, 2, 3],
        format_func=lambda x: {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}[x],
        default=[1, 2, 3],
        label_visibility="collapsed"
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
        # Age distribution by workout type
        fig_age = px.histogram(
            filtered_df, x='Age', color='Workout_Type',
            nbins=15, title='Age Distribution by Workout Type',
            color_discrete_map={'HIIT': '#f97316', 'Cardio': '#00d4ff', 
                               'Strength': '#a855f7', 'Yoga': '#22d3ee'}
        )
        fig_age.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Experience level distribution
        exp_counts = filtered_df['Experience_Level'].value_counts().sort_index()
        exp_labels = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}
        fig_exp = px.bar(
            x=[exp_labels[k] for k in exp_counts.index],
            y=exp_counts.values,
            title='Experience Level Distribution',
            color=exp_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_exp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    
    with col2:
        # Workout type pie chart
        workout_counts = filtered_df['Workout_Type'].value_counts()
        fig_pie = go.Figure(data=[go.Pie(
            labels=workout_counts.index,
            values=workout_counts.values,
            marker_colors=['#f97316', '#00d4ff', '#a855f7', '#22d3ee'],
            hole=0.6
        )])
        fig_pie.update_layout(
            title='Workout Type Distribution',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # BMI by gender and workout
        bmi_data = filtered_df.groupby(['Workout_Type', 'Gender'])['BMI'].mean().reset_index()
        fig_bmi = px.bar(
            bmi_data, x='Workout_Type', y='BMI', color='Gender',
            barmode='group', title='BMI by Gender & Workout Type',
            color_discrete_map={'Male': '#00d4ff', 'Female': '#f97316'}
        )
        fig_bmi.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_bmi, use_container_width=True)

# Tab 2: Performance
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Calories by workout type
        cal_by_workout = filtered_df.groupby('Workout_Type')['Calories_Burned'].mean().reset_index()
        fig_cal = px.bar(
            cal_by_workout, x='Workout_Type', y='Calories_Burned',
            title='Average Calories by Workout Type',
            color='Workout_Type',
            color_discrete_map={'HIIT': '#f97316', 'Cardio': '#00d4ff', 
                               'Strength': '#a855f7', 'Yoga': '#22d3ee'}
        )
        fig_cal.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_cal, use_container_width=True)
        
        # Duration vs Calories scatter
        fig_scatter = px.scatter(
            filtered_df, x='Session_Duration (hours)', y='Calories_Burned',
            color='Experience_Level', title='Duration vs Calories by Experience Level',
            color_continuous_scale='Viridis',
            labels={'Experience_Level': 'Experience'}
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # BPM metrics
        bpm_data = filtered_df.groupby('Workout_Type')[['Max_BPM', 'Avg_BPM', 'Resting_BPM']].mean().reset_index()
        fig_bpm = go.Figure()
        for metric, color in [('Max_BPM', '#f43f5e'), ('Avg_BPM', '#f97316'), ('Resting_BPM', '#22d3ee')]:
            fig_bpm.add_trace(go.Bar(
                name=metric.replace('_', ' '),
                x=bpm_data['Workout_Type'],
                y=bpm_data[metric],
                marker_color=color
            ))
        fig_bpm.update_layout(
            barmode='group', title='Heart Rate Metrics by Workout Type',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_bpm, use_container_width=True)
        
        # Water intake vs Calories
        fig_water = px.scatter(
            filtered_df, x='Water_Intake (liters)', y='Calories_Burned',
            color='Workout_Type', title='Water Intake vs Calories Burned',
            color_discrete_map={'HIIT': '#f97316', 'Cardio': '#00d4ff', 
                               'Strength': '#a855f7', 'Yoga': '#22d3ee'}
        )
        fig_water.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_water, use_container_width=True)
    
    # Radar chart for average stats
    st.markdown("---")
    radar_metrics = ['Avg_BPM', 'Session_Duration (hours)', 'Fat_Percentage', 
                    'Water_Intake (liters)', 'Calories_Burned', 'Workout_Frequency (days/week)']
    
    radar_data = []
    for workout in filtered_df['Workout_Type'].unique():
        workout_data = filtered_df[filtered_df['Workout_Type'] == workout]
        values = [workout_data[m].mean() for m in radar_metrics]
        # Normalize to 0-100 scale
        min_vals = [filtered_df[m].min() for m in radar_metrics]
        max_vals = [filtered_df[m].max() for m in radar_metrics]
        normalized = [(v - min_val) / (max_val - min_val) * 100 if max_val > min_val else 50 
                     for v, min_val, max_val in zip(values, min_vals, max_vals)]
        radar_data.append(normalized)
    
    fig_radar = go.Figure()
    colors = {'HIIT': '#f97316', 'Cardio': '#00d4ff', 'Strength': '#a855f7', 'Yoga': '#22d3ee'}
    for i, workout in enumerate(filtered_df['Workout_Type'].unique()):
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_data[i],
            theta=[m.replace('_', ' ') for m in radar_metrics],
            fill='toself',
            name=workout,
            line_color=colors.get(workout, '#ffffff')
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title='Performance Metrics by Workout Type (Normalized)',
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e8eaf6'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Tab 3: Workouts
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Workout frequency distribution
        fig_freq = px.histogram(
            filtered_df, x='Workout_Frequency (days/week)', color='Workout_Type',
            nbins=7, title='Workout Frequency Distribution',
            color_discrete_map={'HIIT': '#f97316', 'Cardio': '#00d4ff', 
                               'Strength': '#a855f7', 'Yoga': '#22d3ee'}
        )
        fig_freq.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_freq, use_container_width=True)
        
        # Calories by gender and workout
        cal_gender = filtered_df.groupby(['Workout_Type', 'Gender'])['Calories_Burned'].mean().reset_index()
        fig_cal_gender = px.bar(
            cal_gender, x='Workout_Type', y='Calories_Burned', color='Gender',
            barmode='group', title='Calories by Gender & Workout',
            color_discrete_map={'Male': '#00d4ff', 'Female': '#f97316'}
        )
        fig_cal_gender.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_cal_gender, use_container_width=True)
    
    with col2:
        # Fat percentage by experience level
        fat_exp = filtered_df.groupby(['Experience_Level', 'Gender'])['Fat_Percentage'].mean().reset_index()
        fat_exp['Experience'] = fat_exp['Experience_Level'].map({1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'})
        fig_fat = px.bar(
            fat_exp, x='Experience', y='Fat_Percentage', color='Gender',
            barmode='group', title='Average Fat % by Experience Level',
            color_discrete_map={'Male': '#00d4ff', 'Female': '#f97316'}
        )
        fig_fat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_fat, use_container_width=True)
        
        # Frequency vs Calories line chart
        freq_cal = filtered_df.groupby('Workout_Frequency (days/week)')['Calories_Burned'].mean().reset_index()
        fig_line = px.line(
            freq_cal, x='Workout_Frequency (days/week)', y='Calories_Burned',
            title='Workout Frequency vs Average Calories', markers=True
        )
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_line, use_container_width=True)

# Tab 4: Predict
with tab4:
    st.markdown("### 🤖 AI Calorie Predictor")
    st.markdown("Linear Regression model · Adjust sliders to estimate your calories burned per session in real-time.")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("#### 👤 Personal Stats")
        age = st.slider("Age", 18, 70, 30)
        weight = st.slider("Weight (kg)", 40.0, 140.0, 70.0, 0.5)
        height = st.slider("Height (m)", 1.40, 2.10, 1.70, 0.01)
        gender = st.selectbox("Gender", ["Male", "Female"])
        workout_type = st.selectbox("Workout Type", ["HIIT", "Cardio", "Strength", "Yoga"])
        experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        
    with col2:
        st.markdown("#### ❤️ Cardio Stats")
        max_bpm = st.slider("Max BPM", 130, 210, 175)
        avg_bpm = st.slider("Avg BPM", 100, 200, 145)
        resting_bpm = st.slider("Resting BPM", 40, 90, 60)
        duration = st.slider("Session Duration (hrs)", 0.3, 3.0, 1.0, 0.05)
        fat_percentage = st.slider("Fat Percentage", 5.0, 45.0, 25.0, 0.5)
        water_intake = st.slider("Water Intake (L)", 1.0, 4.0, 2.5, 0.1)
        workout_freq = st.slider("Workout Days/Week", 1, 7, 3)
    
    # Calculate BMI
    bmi = weight / (height ** 2)
    
    # Prepare features for prediction
    gender_val = 1 if gender == "Male" else 0
    exp_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    exp_val = exp_map[experience]
    
    hiit = 1 if workout_type == "HIIT" else 0
    cardio = 1 if workout_type == "Cardio" else 0
    strength = 1 if workout_type == "Strength" else 0
    yoga = 1 if workout_type == "Yoga" else 0
    
    features = np.array([[age, weight, height, max_bpm, avg_bpm, resting_bpm, 
                          duration, fat_percentage, water_intake, workout_freq, 
                          exp_val, bmi, hiit, cardio, strength, yoga, gender_val]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    prediction = max(100, min(3000, prediction))
    
    # Calculate peer comparison
    peer_data = filtered_df[
        (filtered_df['Workout_Type'] == workout_type) & 
        (abs(filtered_df['Age'] - age) <= 5)
    ]
    peer_avg = peer_data['Calories_Burned'].mean() if len(peer_data) > 0 else prediction
    diff = prediction - peer_avg
    
    with col3:
        st.markdown(f"""
            <div class="prediction-card">
                <div class="kpi-label">🔥 Estimated Calories Burned</div>
                <div class="prediction-value">{prediction:.0f}</div>
                <div style="color: #6b8cae; font-size: 0.75rem;">kcal per session</div>
            </div>
        """, unsafe_allow_html=True)
        
        diff_color = "#22c55e" if diff >= 0 else "#f43f5e"
        diff_symbol = "▲" if diff >= 0 else "▼"
        st.markdown(f"""
            <div class="prediction-card" style="margin-top: 1rem;">
                <div class="kpi-label">📊 vs. Similar Members</div>
                <div style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: {diff_color}">
                    {diff_symbol} {abs(diff):.0f}
                </div>
                <div style="color: #6b8cae; font-size: 0.75rem;">peer avg: {peer_avg:.0f} kcal</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="prediction-card" style="margin-top: 1rem;">
                <div class="kpi-label">📅 Weekly Burn</div>
                <div style="font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: #a855f7">
                    {prediction * workout_freq:.0f}
                </div>
                <div style="color: #6b8cae; font-size: 0.75rem;">~{prediction * workout_freq * 4.33:.0f} kcal/month</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="margin-top: 1rem; background: #111827; border: 1px solid #1e3a5f; border-radius: 8px; padding: 0.8rem; text-align: center;">
                <div style="font-size: 0.7rem; color: #6b8cae;">Calculated BMI</div>
                <div style="font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: #22d3ee;">{bmi:.1f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Distribution chart
    st.markdown("---")
    workout_data = filtered_df[filtered_df['Workout_Type'] == workout_type]['Calories_Burned']
    if len(workout_data) > 0:
        fig_dist = px.histogram(
            workout_data, nbins=30, title=f'Your Prediction vs {workout_type} Members',
            labels={'value': 'Calories Burned', 'count': 'Number of Members'}
        )
        fig_dist.add_vline(x=prediction, line_dash="dash", line_color="#00d4ff",
                          annotation_text=f"Your Prediction: {prediction:.0f}")
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8eaf6'
        )
        st.plotly_chart(fig_dist, use_container_width=True)