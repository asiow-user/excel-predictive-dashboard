import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

# Page configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Viewership Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — palette: #24232A (bg), #523F93 (accent), #CFC1FF (light)
st.markdown(""" 
<style>
    /* Global font */
    html, body, [class*="css"], .stApp, .stMarkdown, input, textarea, select, button {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    }

    /* App background — darker than spec for more depth */
    .stApp {
        background-color: #15141A;
        color: #FFFFFF;
    }

    /* Headers — keep accent purple */
    h1, h2, h3, h4, h5, h6 {
        color: #F4F4F4 !important;
        letter-spacing: -0.01em;
    }

    /* Body text + markdown — thin white */
    .stMarkdown, .stMarkdown p, .stApp p, label, .stRadio label, .stCheckbox label {
        color: #FFFFFF !important;
    }

    /* Field label block (label on top, italic hint underneath) */
    .field-label {
        color: #F4F4F4;
        font-size: 0.95rem;
        margin: 0.6rem 0 0.15rem 0;
        line-height: 1.2;
    }
    .field-hint {
        display: block;
        font-style: italic;
        font-size: 0.78rem;
        color: #CFC1FF;
        opacity: 0.65;
        margin-top: 0.1rem;
        line-height: 1.3;
    }

    /* Horizontal rules */
    hr {
        border-color: #523F93 !important;
        opacity: 0.5;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0e13;
        border-right: 1px solid #523F93;
    }

    /* Buttons */
    .stButton > button {
        background-color: #523F93;
        color: #CFC1FF;
        border-radius: 8px;
        border: 1px solid #523F93;
        padding: 0.5rem 1rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        background-color: #CFC1FF;
        color: #24232A;
        border-color: #CFC1FF;
    }

    /* Inputs — text, number, date, time */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input {
        background-color: #1F1E26 !important;
        color: #CFC1FF !important;
        border: 1px solid #523F93 !important;
        border-radius: 6px !important;
    }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1F1E26 !important;
        color: #CFC1FF !important;
        border: 1px solid #523F93 !important;
        border-radius: 6px !important;
    }
    .stSelectbox div[data-baseweb="select"] svg {
        color: #CFC1FF !important;
        fill: #CFC1FF !important;
    }

    /* Selectbox dropdown menu */
    div[data-baseweb="popover"] div[role="listbox"] {
        background-color: #1F1E26 !important;
        border: 1px solid #523F93 !important;
    }
    div[data-baseweb="popover"] li {
        color: #CFC1FF !important;
        background-color: #1F1E26 !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #523F93 !important;
        color: #CFC1FF !important;
    }

    /* Number input +/- buttons */
    .stNumberInput button {
        background-color: #523F93 !important;
        color: #CFC1FF !important;
        border: none !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #CFC1FF !important;
    }
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: #523F93 !important;
    }

    /* Radio */
    .stRadio [role="radiogroup"] label {
        color: #CFC1FF !important;
    }

    /* Info / alert boxes */
    .stAlert, div[data-baseweb="notification"] {
        background-color: #1F1E26 !important;
        color: #CFC1FF !important;
        border-left: 4px solid #523F93 !important;
        border-radius: 8px !important;
    }
    .stAlert p, .stAlert li, .stAlert strong {
        color: #CFC1FF !important;
    }

    /* Inline code */
    code {
        background-color: #1F1E26 !important;
        color: #CFC1FF !important;
        padding: 0.1rem 0.35rem;
        border-radius: 4px;
        border: 1px solid #523F93;
    }

    /* Title styling */
    h1 {
        color: #CFC1FF !important;
        border-bottom: 2px solid #523F93;
        padding-bottom: 0.5rem;
    }

    /* Section box (Settings / Event Details containers) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #523F93 !important;
        border-radius: 14px !important;
        padding: 1.5rem 1.75rem !important;
        background-color: #1A1921 !important;
    }

    /* Prediction box */
    .prediction-box {
        background-color: #1A1921;
        padding: 2.5rem 2rem;
        margin: 32px;
        border-radius: 16px;
        border: 1px solid #523F93;
        text-align: center;
        box-shadow: 0 6px 28px rgba(82, 63, 147, 0.3);
    }
    .prediction-box .prediction-label {
        color: #CFC1FF;
        font-size: 1rem;
        opacity: 0.7;
        margin: 0 0 0.5rem 0;
        letter-spacing: 0.02em;
    }
    .prediction-number {
        font-size: 5.5rem;
        font-weight: 300 !important;
        color: #CFC1FF !important;
        letter-spacing: -0.03em;
        margin: 0.5rem 0 2.5rem 0 !important;
        line-height: 1;
    }
    .prediction-box .prediction-detail {
        color: #CFC1FF;
        font-size: 0.85rem;
        opacity: 0.55;
        margin: 0;
        padding-top: 1.25rem;
        border-top: 1px solid rgba(82, 63, 147, 0.4);
    }
    /* Tooltip help icon */
    [data-testid="stTooltipIcon"] svg {
        color: #523F93 !important;
        fill: #523F93 !important;
    }
</style>
""", unsafe_allow_html=True)

def field(label: str, hint: str):
    st.markdown(
        f'<div class="field-label">{label}<span class="field-hint">{hint}</span></div>',
        unsafe_allow_html=True,
    )

# Title
st.title("Viewership Predictor")
# st.markdown("*Interactive mock-up for predictive modeling*")

# Create two columns for the main sections
left_col, right_col = st.columns([1, 1.5], gap="medium")

# ==================== LEFT COLUMN: SETTINGS ====================
with left_col:
    with st.container(border=True):
        st.header("Model Settings")

        field("Target Feature", "Which feature column to predict")
        target_feature = st.selectbox(
            "Target Feature",
            ["traj_avg_household_viewership"],
            label_visibility="collapsed",
            disabled=True
        )

        field("Target Log", "Train on log1p and predict expm1?")
        local_national = st.radio(
            "Game Type",
            ["Enabled", "Disabled"],
            horizontal=True,
            label_visibility="collapsed",
            disabled=True
        )


        field("Season Portion", "0 = start of season, 1 = end of season")
        season_portion = st.slider(
            "Season Portion",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            label_visibility="collapsed",
            disabled=True,
        )

        field("Season Index Adjustment", "Cutoff season for the data to train on, -1 is most recent")
        season_index = st.number_input(
            "Season Index Adjustment",
            min_value=-2,
            max_value=0,
            value=-1,
            step=1,
            label_visibility="collapsed",
            disabled=True,
        )

        field("Model Name", "Select the prediction model to use")
        model_name = st.selectbox(
            "Model Name",
            ["HistGradientBoostingRegressor"],
            label_visibility="collapsed",
            disabled=True
        )

        # # st.markdown("---")
        # st.markdown("### Current Configuration")
        # st.write(f"**Target:** `{target_feature}`")
        # st.write(f"**Season Progress:** `{season_portion*100:.0f}%`")
        # st.write(f"**Season Index:** `{season_index}`")
        # st.write(f"**Model:** `{model_name}`")

# ==================== RIGHT COLUMN: INPUTS ====================
with right_col:
    with st.container(border=True):
        st.header("Model Parameters")

        col_a, col_b = st.columns(2)

        with col_a:
            field("League Network Prior Mean", "Average prior target for league-network")
            league_network_prior_mean = st.number_input(
                "league_network_prior_mean",
                value=0.0,
                label_visibility="collapsed",
            )

            field("League Network Prior Median", "Median prior target for league-network")
            league_network_prior_median = st.number_input(
                "league_network_prior_median",
                value=0.0,
                label_visibility="collapsed",
            )

            field("Team Prior Sum", "Combined prior target mean for home/away teams")
            team_prior_sum = st.number_input(
                "team_prior_sum",
                value=0.0,
                label_visibility="collapsed",
            )

            field("Is Playoff", "Whether the game is a playoff game")
            is_playoff = st.radio(
                "is_playoff",
                [True, False],
                horizontal=True,
                label_visibility="collapsed",
            )

        with col_b:
            field("Is National", "Whether the game is nationally broadcast")
            is_national = st.radio(
                "is_national",
                [True, False],
                horizontal=True,
                label_visibility="collapsed",
            )

            field("Home Team Prior Median", "Median prior target for home team")
            home_team_prior_median = st.number_input(
                "home_team_prior_median",
                value=0.0,
                label_visibility="collapsed",
            )

            field("Away Team Prior Median", "Median prior target for away team")
            away_team_prior_median = st.number_input(
                "away_team_prior_median",
                value=0.0,
                label_visibility="collapsed",
            )

            field("League Prior Median", "Median prior target for league")
            league_prior_median = st.number_input(
                "league_prior_median",
                value=0.0,
                label_visibility="collapsed",
            )

# ==================== PREDICTION SECTION ====================
st.markdown("---")
st.header("Predicted Viewership")

# Create a mock prediction based on inputs
# In the real app, this would call your model
def mock_prediction(): ##FIXME @Daniel Replace `mock_prediction()` function with your model integration
    """Generate a mock prediction based on inputs"""
    base_viewers = 1.5  # million viewers base
    
    # Adjust based on league
    league_multipliers = {"NBA": 1.2, "NFL": 2.0, "MLB": 0.9, "NHL": 0.7, "MLS": 0.5, "WNBA": 0.4}
    league_factor = 1.0
    
    # Adjust based on season type
    season_factors = {"Regular Season": 1.0, "Preseason": 0.5, "Postseason": 1.8}
    season_factor = 1.0
    
    # Adjust based on broadcast
    broadcast_factors = {"ESPN": 1.3, "TNT": 1.2, "FOX": 1.4, "NBC": 1.1, 
                         "ABC": 1.5, "CBS": 1.3, "NBA TV": 0.6, "MLB Network": 0.5}
    broadcast_factor = 1.0
    
    # National vs Local
    game_type_factor = 1.5 if local_national == "National" else 0.3
    
    # Season portion effect (mid-season peak)
    season_effect = 1 + np.sin(season_portion * np.pi) * 0.3
    
    # Calculate predicted viewers (millions)
    predicted = base_viewers * league_factor * season_factor * broadcast_factor * game_type_factor * season_effect
    
    # Adjust by season index
    predicted = predicted + (season_index * 0.05)
    
    # Ensure positive
    predicted = max(0.1, predicted)
    
    return round(predicted, 3)

# Make prediction
predicted_value = mock_prediction()

# Display prediction in styled box based on target feature
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="prediction-box">
        <p class="prediction-label">Predicted {target_feature.replace('_', ' ').title()}</p>
        <p class="prediction-number">{predicted_value}</p>
        <p class="prediction-detail">Based on {model_name} &middot; {local_national} Broadcast</p>
    </div>
    """, unsafe_allow_html=True)

# # Display additional info about the prediction
# st.info(f"""
# **Prediction Details:**
# - Using `{model_name}` with target feature `{target_feature}`
# - Event: {away_team} @ {home_team} ({game_date} at {game_time.strftime('%I:%M %p')})
# - Broadcast: {broadcast_name} ({local_national})
# - Season progress: {season_portion*100:.0f}% complete
# - Confidence: High (mock prediction - replace with actual model)
# """)


