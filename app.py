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

# Custom CSS for color scheme (based on your image.png colors)
st.markdown("""
<style>
    /* Main background colors */
    .stApp {
        background: linear-gradient(135deg, #1b1534 0%, #312e34 100%);
    }
    
    /* Headers */
    h1, h2, h3, .stMarkdown {
        color: #ad9aefff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #312e34ff;
        border-right: 2px solid #6e3effff;
    }
    
    /* Buttons and interactive elements */
    .stButton > button {
        background-color: #6e3effff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #523f93ff;
        color: #e69138ff;
    }
    
    /* Select boxes and inputs */
    .stSelectbox, .stNumberInput, .stDateInput, .stTimeInput {
        background-color: #595959ff;
        border-radius: 5px;
    }
    
    /* Prediction box */
    .prediction-box {
        background-color: #4d217aff;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #e69138ff;
        text-align: center;
    }
    
    .prediction-number {
        font-size: 3rem;
        font-weight: bold;
        color: #e69138ff;
    }
    
    /* Toggle switches */
    .stCheckbox {
        color: #c4c0cfff;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Viewership Predictor")
st.markdown("*Interactive mock-up for predictive modeling*")

# Create two columns for the main sections
left_col, right_col = st.columns([1, 1.5], gap="large")

# ==================== LEFT COLUMN: SETTINGS ====================
with left_col:
    st.header("Settings")
    st.markdown("---")
    
    # Target feature dropdown
    target_feature = st.selectbox(
        "Target Feature",
        ["sbj_viewers", "sbj_us_viewers_millions", "trajektory_households", "viewers_per_household"],
        help="Select which metric to predict"
    )
    
    # Season portion (0-1 slider)
    season_portion = st.slider(
        "Season Portion",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        help="0 = start of season, 1 = end of season"
    )
    
    # Season index adjustment
    season_index = st.number_input(
        "Season Index Adjustment",
        min_value=-10,
        max_value=10,
        value=0,
        step=1,
        help="Adjust for seasonal trends (+/- integer)"
    )
    
    # Model name dropdown
    model_name = st.selectbox(
        "Model Name",
        ["Linear Regression"],
        help="Select the prediction model to use"
    )
    
    # Display current settings summary
    st.markdown("---")
    st.markdown("### Current Configuration")
    st.write(f"**Target:** `{target_feature}`")
    st.write(f"**Season Progress:** {season_portion*100:.0f}%")
    st.write(f"**Season Index:** {season_index}")
    st.write(f"**Model:** {model_name}")

# ==================== RIGHT COLUMN: INPUTS ====================
with right_col:
    st.header("Event Details")
    st.markdown("---")
    
    # Create two sub-columns for better organization
    col_a, col_b = st.columns(2)
    
    with col_a:
        # League dropdown
        league = st.selectbox(
            "League",
            ["NBA", "NFL", "MLB", "NHL", "MLS", "WNBA"],
            help="Select the sports league"
        )
        
        # Season type
        season_type = st.selectbox(
            "Season Type",
            ["Regular Season", "Preseason", "Postseason"],
            help="Regular, Preseason, or Postseason"
        )
        
        # Game date
        game_date = st.date_input(
            "Game Date",
            value=datetime.now(),
            help="Date of the event"
        )
        
        # Game time
        game_time = st.time_input(
            "Game Time",
            value=time(19, 30),
            help="Tip-off/kickoff time"
        )
        
        # Home team
        home_team = st.selectbox(
            "Home Team",
            ["None","Wisconsin","Tennessee","Am","Spurs","Knicks","SMU","USC","Wake Forest","Washington State","Indiana","Alabama","Northwestern","Packers","Eagles","Broncos","Washington","Oregon State","Ole Miss","Georgia","Steelers","Chiefs","Atalanta","Fever","Duke","UCLA","Illinois State","Jaguars","Michigan State","Miami","Lions","Grizzlies","Nebraska","Ohio State","Dodgers","Flyers","Mariners","Guardians","Houston","Navy","Cal","Aces","Blue Jays","Stanford","Bengals","Falcons","Cowboys","76ers","Warriors","Oregon","Arizona State","Kansas","Vanderbilt","Patriots","Appalachian State","Seahawks","Arsenal","T'Wolves","Kentucky","BYU","Clippers","Texas Tech","Arizona","Yankees","Brewers","Phillies","Auburn","Argentina","Giants","Rangers","nan","Thunder","Rockets","Kings","Mavericks","Hawks","Pacers","Bucks","Celtics","Heat","Magic","Bulls","Nets","Cavaliers","Suns","Lakers","Jazz","Pelicans","Nuggets","Trail Blazers","South Alabama","Florida State","Syracuse","Iowa","Arkansas State","Clemson","Penn State","Fil-A Peach Bowl","Boise State","Michigan","LSU","South Carolina","USF","Baylor","San Diego State","Oklahoma State","Air Force","Missouri","Texas A&M","Colorado","Iowa State","Utah","Notre Dame","ECU","Georgia Tech","TCU","Wyoming","Florida","Southern","Maryland","UNAM Pumas","LAFC","Jamaica","Canada","Suriname","El Salvador","Haiti","Trinidad & Tobago","Panama","Grenada","Brazil","Colombia","Bolivia","Venezuela","Ecuador","Chile","Liverpool","Chelsea","Manchester City","Newcastle","Bournemouth","Everton","Crystal Palace","Fulham","Sheffield United","Leicester City","Brighton","Leeds","Wolverhampton","Paris Saint-Germain","Nigeria","Honduras","Germany","Wales","Netherlands","South Korea","place game","Rayo Vallecano","Alaves","Real Madrid","Valencia","FC Barcelona","Tigres UANL","Club America","Toluca","Cruz Azul","Monterrey","Pachuca","Puebla","Club Atletico","Chivas","Leon","Mazatlan","Tigres","Atlas","New York","Taiwan","Australia","Hawaii","Southern Cal","Astros","Red Sox","Orioles","Rays","Indians","Cardinals","Padres","Reds","Mets","Braves","Angels","White Sox","backs-Dodgers","backs-Rangers","D-backs","Timbers","Charlotte FC","Fire","Sounders","Atlanta United","Austin FC","Sporting K.C.","Galaxy","Nashville SC","Jackson State","Middle Tennessee","Louisville","West Virginia","South Dakota State","Oklahoma","DePaul","Marquette","Creighton","Bills","Raiders","Chargers","Vikings","49ers","Rams","Buccaneers","7","Colts","Titans","Bears","Panthers","Jets","Saints","Commanders","Dolphins","Browns","Ravens","Texans","Maple Leafs","Bruins","Hurricanes","Canadiens","Oilers","Stars","Avalanche","Kraken","Sabres","Penguins","Red Wings","Lightning","Blues","Islanders","Cincinnati","San Diego Wave","Gotham FC","Portland Thorns","Angel CIty","Seattle Reign","Angel City","K.C. Current","North Carolina Courage","Bay FC","Chicago Red Stars","N.C. Courage","Texas","Arkansas","Virginia Tech","Illinois","North Carolina","Florida A&M","UCF","Virginia","Rutgers","Tulane","Minnesota","Kansas State","Mississippi State","Purdue","WVU","Pitt","South Carolina State","South Dakota","Montana","Holy Cross","N.C. State","San Jose State","New Mexico State","Fresno State","Ohio","Coastal Carolina","Western Michigan","10 Championship","UConn","Memphis","Western Kentucky","Drake","12 Championship","Georgetown","New Mexico","Providence","Xavier","Gonzaga","St. John's","Villanova","Morehead State","Akron","Vermont","Lipscomb","Troy","Wagner","Grambling State","Wofford","James Madison","FAU","Oral Roberts","Delaware","Colgate","N.Y. Atlas","Utah Archers","Fiorentina","N.Y. GC","Jupiter Links GC","Atlanta Drive GC","Villarreal","Atletico Madrid","Dortmund","Paris St Germain","Ukraine","Belgium","Denmark","Slovenia","Albania","Slovakia","Italy","France","Spain","San Antonio Brahmas","Arlington Renegades","D.C. Defenders","Michigan Panthers","Birmingham Stallions","Philadelphia Stars","Memphis Showboats","Tampa Bay Bandits","New Orleans Breakers","Houston Outlaws","Las Vegas Aces","Indiana Fever","Storm","Connecticut Sun","Valkyries","Liberty","Phoenix Mercury","Washington Mystics","N.Y. Liberty","Chicago Sky","L.A. Sparks","Atlanta Dream","Dallas Wings","Minnesota Lynx","Seattle Storm","Sky","Firefighters","NYCFC","Conquerors","Rugby ATL","New England Free","Southern Miss","Sam Houston State","Bryant Perrella","Fiji","Guatemala","Iceland","Paraguay","Uzbekistan","Mexico","New Zealand","Rose","Vinyl","Pistons","Orlando Pride","Lynx","Blue-Jays","Cubs","Nottingham Forest","Tigers","North Texas","Alexander Zverev","Bayer Leverkusen","FC Koln","Leipzig","Costa Rica","U.S.","Qatar","Dominican Republic","Manchester United","West Ham","Southampton","Tottenham","Norwich","Palmeiras","Al Ain","England","China","Saudi Arabia","Ghana","Senegal","Poland","Morocco","Croatia","Necaxa","Queretaro","Twins","Royals","2","Marlins","Nationals","A's","backs-Phillies","Red Bulls","Minnesota United","Orlando City SC","Atlanta FC","Union","Hornets","Heats","fil-A Peach Bowl","Boston College","East Tennessee State","Mercer","Uconn","-Bears","Capitals","Canucks","Golden Knights","Wild","Blackhawks","Devils","Blue Jackets","UC Irvine","Washington Spirit","Racing Louisville","chicago Red Stars","Utah Royals","Charlotte","Grambling","Howard","Northern Illinois","Louisiana","Texas State","George Mason","Seton Hall","Utah State","memphis","Butler","Nova Southeastern","Saint Francis","American","Robert Morris","Norfolk State","Stetson","Dayton","Oakland","II Championship","St. Peter's","Northern Kentucky","Davidson","Colorado State","San Francisco","Murray State","Loyola Chicago","St. Mary's","South Sudan","Workday Championship","Whipsnakes","Archers","Waterdogs","Philadelphia Waterdogs","Cannons","AC Milan","New York GC","Boston Commons Golf","Atlanta Drive","Russia","Inter Milan","Benfica","Bayern Munich","Germain-FC Barcelona","Paris St. Germain","Austria","Switzerland","Marvin Vettori","St. Louis Battlehawks","Houston Roughnecks","Pittsburgh Maulers","Houston Gamblers","New Jersey Generals","N.Y.Liberty","Mystics","Sun","Wings","Aryna Sabalenka","Fedor","Generals","Jousters","American Bowl","Rugby New York","Saskatchewan Rush","Japan","Northern Ireland","Sweden","La Familia","Sports Leagues Canada","FC Cincinnati","Borussia Monchengladbach","Martinique","Uruguay","Aston Villa","Brentford","Nottingham","Romagna Grand Prix","Al Ahly","Al Hilal","Vietnam","Serbia","Tunisia","Iran","Portugal","Prix","Santos Laguna","Juarez","Club Atletico San Luis","Tigers UANL","Nevada","Rapids","Uion","Earthquakes","Inter Miami CF","Revolution","Saint Louis","Buffalo","Washington Football Team","3","WFT","Chicago Stars","Houston Dash","N.C. Central","Bowling Green","Louisiana Tech","Ball State","Grand Canyon","Omaha","West Texas A&M","Iona","Texas Southern","Texas A&M Corpus Christi","Georgia State","Montana State","Longwood","Furman","- Theegala","Chaos","Boston Common Golf","Germain-Arsenal","Romania","Turkey","Topuria","New Orleans Gamblers","Rhode Island FC","Jasmine Paolini","Arizona Burn","Pacific Amateur Championship","Greece","Sea Lions","Marshall","Kyrone Davis","Toulouse","Peru","Lunar Owls","Laces","Great Britain","Raptors","Tarleton State","UNLV","Mercury","Aliassime","Casper Ruud","Leeds United","West Brom","Burnley","Boca Juniors","Las Vegas","backs-Yankees","Real Salt Lake","Portland Timbers","Seattle Sounders","Wizards","UNC Greensboro","Missouri State","Star Funny Car Callout","Indiana State","OL Reign","Racing Lousiville","Army","Temple","-Miami","Jacksonville State","UAB","Star Game","Bradley","Bryant","Yale","Cal State Fullerton","Chattanooga","Fairleigh Dickinson","Princeton","Maryland Whipsnakes","Lille","Calvin Kattar","Brimingham Stallions","Orlando Guardians","Indy Eleven","Phoenix Rising FC","Ons Jabeur","Party Animals","Texas Tailgaters","New England Free Jacks","South Africa","Scotland","Cameroon","Bosnia & Herzegovina","Carmen's Crew","Eberlein Drive","Midtown Prestige","Inter Miami","Ireland"],
            help="Home team name"
        )
        
        
        # Away team
        away_team = st.selectbox(
            "Away Team",
            ["None","Michigan State","Texas","AT&T Pebble Beach Pro","Warriors","Magic","Butler","South Carolina","North Carolina","Iowa","Louisiana Tech","Wisconsin","Oklahoma","Michigan","Eagles","Lions","Chiefs","Ohio State","Houston","LSU","Alabama","Vikings","Ravens","Juventus","Aces","Lakers","SMU","Maryland","Montana State","Bills","Duke","Western Michigan","Cowboys","Texans","Bears","USC","Penn State","Blue Jays","Penguins","Tigers","Texas Tech","Air Force","Mercury","Brewers","Mariners","Florida State","Steelers","Commanders","Cavaliers","Knicks","Baylor","Florida","Mississippi State","Utah","Georgia","Georgia Southern","TCU","49ers","Bournemouth","Mavericks","Rockets","Iowa State","Indiana","Ole Miss","West Virginia","Rams","Cubs","Dodgers","Kansas","Mexico","nan","Bucks","Trail Blazers","Hornets","Celtics","Hawks","Heat","Pacers","Nets","Raptors","Bulls","76ers","Thunder","Nuggets","Suns","T'Wolves","Grizzlies","Pelicans","Clippers","Jazz","Kings","Eastern Michigan","Louisville","Minnesota","Northern Illinois","Tennessee","Notre Dame","Chick","Oklahoma State","Arizona State","Arizona","Arkansas","Army","Auburn","Boise State","Boston College","BYU","Cal","Cincinnati","Clemson","Colorado","Fresno State","Georgia Tech","Grambling","Hawaii","Illinois","Kansas State","Sounders","Leon","U.S.","Costa Rica","Argentina","Everton","Arsenal","Aston Villa","Brentford","Brighton","Chelsea","Liverpool","Manchester City","Manchester city","Manchester United","Newcastle","Southampton","Watford","Atletico Madrid","Canada","Spain","Brazil","third","FC Barcelona","Real Madid","Real Madrid","Atlas","Pachuca","Atletico San Luis","Chivas","Toluca","Tigres UANL","Club America","Club Atletico","Cruz Azul","FC Juarez","Juarez","Mazatlan","Monterrey","Necaxa","Puebla","Queretaro","San Luis","Santos Laguna","Tijuana","UNAM Pumas","UNAM","Aruba","Venezuela","Italy","Astros","Rangers","Yankees","Red Sox","Twins","Angels","Braves","Cardinals","Giants","Mets","Padres","Phillies","White Sox","D","Crew","NYCFC","Atlanta United","Galaxy","LAFC","Orlando City","Red Bulls","Revolution","Timbers","Union","Minnesota United","UConn","N.C. State","Villanova","Virginia","Dolphins","Bengals","Jaguars","Falcons","Patriots","Saints","Buccaneers","Packers","Rounds 4","Jets","Broncos","Browns","Chargers","Panthers","Seahawks","Raiders","Titans","Colts","Bruins","Maple Leafs","Islanders","Lightning","Oilers","Stars","Blues","Capitals","Devils","Flyers","Golden Knights","Kraken","Red Wings","Sabres","Star","Wild","Avalanche","Indiana State","Angel City","Portland Thorns","Chicago Stars","Gotham FC","K.C. Current","North Carolina Courage","Orlando Pride","Racing Louisville","San Diego Wave","Utah Royals","Kent State","Louisiana","Miami","Missouri","Nebraska","Norfolk State","Northwestern","Oregon","Pitt","Purdue","San Jose State","Stanford","Syracuse","Texas A&M","Texas AM","Tulane","UCF","UCLA","UNLV","USF","Utah State","Virginia Tech","Wake Forest","Washington State","Washington","Wyoming","Jackson State","South Carolina State","North Dakota State","South Dakota State","ECU","Navy","UTSA","Ball State","South Alabama","Kentucky","St. John's","A","Creighton","Georgetown","Gonzaga","Loyola Chicago","Pac","Providence","San Diego State","Seton Hall","Marquette","Yale","Oral Roberts","Fairleigh Dickinson","Xavier","Spurs","Denver Outlaws","Philadelphia Waterdogs","Atalanta","L.A. GC","Bay GC","Jupiter Links GC","England","Czech Republic","Belgium","Switzerland","D.C. Defenders","Birmingham Stallions","Houston Roughbecks","Houston Roughnecks","San Antonio Brahmas","St. Louis Battlehawks","New Orleans Breakers","Boston Breakers","Houston Gamblers","New Jersey Generals","Philadelphia Stars","Pittsburgh Maulers","N.Y. Liberty","Connecticut Sun","Dallas Wings","Dream","Lynx","Minnesota Lynx","Chicago Sky","Indiana Fever","L.A. Sparks","Las Vegas Aces","Phoenix Mercury","Seattle Storm","Sun","Wings","Savannah Bananas","Alphas","L.A. Giltinis","San Diego Legion","James Madison","Tony Harrison","Vinyl","Rose","South Dakota","Prairie View A&M","Rutgers","Tulsa","Jannik Sinner","Bayern Munich","Dortmund","Panama","Cuba","Guadeloupe","Honduras","El Salvador","Crystal Palace","Fulham","Leeds","Leicester","Norwich","Tottenham","West Ham","Wolverhampton","Inter Miami","Denmark","Ecuador","France","Portugal","Saudi Arabia","Atletico de San Luis","Tigres","Royals","Guardians","Rounds 1","Orioles","Rays","Earthquakes","Nashville SC","St. Louis City SC","St. Louis City","Pistons","Wizards","ets","Akron","Albany","Colorado State","Delaware","Idaho","Hurricanes","UT Chattanooga","Bay FC","Houston Dash","Kansas City Current","OL Reign","Racing Lousiville","Washington Spirit","Ohio","Oregon State","Southern","Temple","Toledo","UMass","Florida A&M","North Texas","Western Kentucky","Rice","VCU","Charlotte","Vanderbilt","Minnesota State Morehead","Alabama State","Mount St. Mary's","FAU","Murray State","St. Peter's","Sunderland","WGC","AT&T Pebble Peach Pro","Archers","Waterdogs","Cannons","Chaos","N.Y. Atlas","Whipsnakes","Carolina Chaos","Parma","Atlanta Drive GC","Boston Common Golf","Jupiter GC","N.Y. GC","AC Milan","Paris Saint","Inter Milan","Germany","Scotland","Sweden","Kevin Holland","Arlington Renegades","Memphis Showboats","Michigan Panthers","Tampa Bay Bandits","Fever","Atlanta Dream","Liberty","Lminnesota Lynx","Sky","Sparks","Storm","Washington Mystics","Washngton Mystics","Madison Keys","Bader","Generals","All","Seattle Seawolves","Coastal Carolina","Cornell","Buffalo Bandits","Wales","Chile","The Nawf","Newtown Pride","Lunar Owls","Memphis","Marshall","Arkansas State","Central Michigan","Leverkusen","Grenada","Jamaica","Uruguay","Nottingham Forest","Emilia","Croatia","Morocco","Sao Paulo E","Real Socieded","Club Atletico de San Luis","Club San Luis","Curacao","North Dakota","Austin FC","Real Salt Lake","Fire","Nashcille SC","Sporting K.C.","Sporting KC","St. Louis","Rounds 2","Dolpins","Blackhawks","Predators","Seattle Reign","Nevada","New Mexico","North Alabama","UTEP","Georgia State","Old Dominion","UAB","Appalachian State","DePaul","Loyola","St. Mary's","Drake","St. Johns","Northwest Missouri State","The Life","Whipnakes","Boston Cannons","California Redwoods","Redwoods","Netherlands","Emmett","Phialdelphia Stars","Vegas Vipers","Detroit City","Barbora Krejcikova","Pennsylvania Ringers","Asia","Jousters","Sea Lions","Vermont","Anthony Dirrell","La Rochelle","Ireland","Celtic","Mexcio","Mist","Phantom","USC Upstate","Reds","Lafayette","Jannik Sinner d. Felix Auger","Carlos Alcaraz","Qatar","Colombia","Paraguay","Peru","Brighton & Hove Albion","Leicester City","Norwich City","River Plate","Poland","Senegal","Japan","Cadiz","Taiwan","Inter Miami CF","Charlotte FC","Bowling Green","WFT","N.C. Courage","Kansas City","San Diego Waves","Tennessee State","Lousiana","HBCU All","Bradley","Valparaiso","Wichita State","Grambling State","Wagner","New Mexico State","Western Carolina","Sam Houston State","Utah Archers","Maryland Whipsnakes","Red Bull Leipzig","Turkey","Max Holloway","Seattle Sea Dragons","Louisville City","San Antonio FC","Valkyries","Iga Swiatek","Linemen","Denver","New Zealand","Ghana","Forever Coogs","AfterShocks","Aftershocks","Dynamo"],
            help="Away team name"
        )
    
    with col_b:
        # Venue
        venue = st.text_input(
            "Venue",
            value="TD Garden",
            help="Stadium/arena name"
        )
        
        # City
        city = st.text_input(
            "City",
            value="Boston",
            help="Event city"
        )
        
        # State
        state = st.text_input(
            "State",
            value="MA",
            help="State (2-letter code)"
        )
        
        # Country
        country = st.selectbox(
            "Country",
            ["USA", "Canada", "UK", "Other"],
            help="Country of the event"
        )
        
        # Broadcast name
        broadcast_name = st.selectbox(
            "Broadcast Network",
            ["ESPN", "TNT", "FOX", "NBC", "ABC", "CBS", "NBA TV", "MLB Network"],
            help="Primary broadcast network"
        )
        
        # Local/National toggle
        local_national = st.radio(
            "Game Type",
            ["National", "Local"],
            horizontal=True,
            help="Is this a national or local broadcast?"
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
    league_factor = league_multipliers.get(league, 1.0)
    
    # Adjust based on season type
    season_factors = {"Regular Season": 1.0, "Preseason": 0.5, "Postseason": 1.8}
    season_factor = season_factors.get(season_type, 1.0)
    
    # Adjust based on broadcast
    broadcast_factors = {"ESPN": 1.3, "TNT": 1.2, "FOX": 1.4, "NBC": 1.1, 
                         "ABC": 1.5, "CBS": 1.3, "NBA TV": 0.6, "MLB Network": 0.5}
    broadcast_factor = broadcast_factors.get(broadcast_name, 1.0)
    
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
        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">Predicted {target_feature.replace('_', ' ').title()}</p>
        <p class="prediction-number">{predicted_value}</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; color: #c4c0cfff;">
            Based on {model_name} • {local_national} Broadcast
        </p>
    </div>
    """, unsafe_allow_html=True)

# Display additional info about the prediction
st.info(f"""
**Prediction Details:**
- Using `{model_name}` with target feature `{target_feature}`
- Event: {away_team} @ {home_team} ({game_date} at {game_time.strftime('%I:%M %p')})
- Broadcast: {broadcast_name} ({local_national})
- Season progress: {season_portion*100:.0f}% complete
- Confidence: High (mock prediction - replace with actual model)
""")


