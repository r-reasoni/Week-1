import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="🔋 EV Adoption Forecaster",
    layout="wide",
    page_icon="🚗"
)

# === Load model ===
model = joblib.load('forecasting_ev_model.pkl')

# === Dark neon aesthetic CSS (inspired by EV charging station visuals) ===
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0f1117;
            color: #e0f2f1;
        }
        .stApp {
            background: linear-gradient(to bottom, #0f1117, #131720);
        }
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
        }
        h1, h2, h3, h4, .stMarkdown {
            color: #90caf9;
        }
        .stSelectbox > div, .stMultiSelect > div, .stButton > button {
            background-color: #1c1c2b;
            color: #e0f2f1;
        }
        .stButton > button:hover {
            background-color: #1976d2;
            color: white;
        }
        .glow-card {
            background-color: #121c2b;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 153, 0.2);
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# === Title and Banner ===
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #00e676;'>🔋 EV Adoption Forecast</h1>
        <h4 style='color: #80cbc4;'>Electric Vehicle Growth Estimator for Washington State</h4>
    </div>
""", unsafe_allow_html=True)

# === EV background image ===
st.image("ev1.jpg", use_container_width=True)

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_csv("preprocessed_ev_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# === County selection ===
st.markdown("""
    <h3 style='margin-top: 20px; color: #00e5ff;'>📍 Choose a County:</h3>
""", unsafe_allow_html=True)

county_list = sorted(df['County'].dropna().unique().tolist())
county = st.selectbox("Select a County", county_list)

if county not in df['County'].unique():
    st.warning(f"County '{county}' not found in dataset.")
    st.stop()

county_df = df[df['County'] == county].sort_values("Date")
county_code = county_df['county_encoded'].iloc[0]

# === Forecasting logic ===
historical_ev = list(county_df['Electric Vehicle (EV) Total'].values[-6:])
cumulative_ev = list(np.cumsum(historical_ev))
months_since_start = county_df['months_since_start'].max()
latest_date = county_df['Date'].max()

future_rows = []
forecast_horizon = 36

for i in range(1, forecast_horizon + 1):
    forecast_date = latest_date + pd.DateOffset(months=i)
    months_since_start += 1
    lag1, lag2, lag3 = historical_ev[-1], historical_ev[-2], historical_ev[-3]
    roll_mean = np.mean([lag1, lag2, lag3])
    pct_change_1 = (lag1 - lag2) / lag2 if lag2 != 0 else 0
    pct_change_3 = (lag1 - lag3) / lag3 if lag3 != 0 else 0
    ev_growth_slope = np.polyfit(range(len(cumulative_ev[-6:])), cumulative_ev[-6:], 1)[0] if len(cumulative_ev) >= 6 else 0

    new_row = {
        'months_since_start': months_since_start,
        'county_encoded': county_code,
        'ev_total_lag1': lag1,
        'ev_total_lag2': lag2,
        'ev_total_lag3': lag3,
        'ev_total_roll_mean_3': roll_mean,
        'ev_total_pct_change_1': pct_change_1,
        'ev_total_pct_change_3': pct_change_3,
        'ev_growth_slope': ev_growth_slope
    }

    pred = model.predict(pd.DataFrame([new_row]))[0]
    future_rows.append({"Date": forecast_date, "Predicted EV Total": round(pred)})

    historical_ev.append(pred)
    historical_ev.pop(0)
    cumulative_ev.append(cumulative_ev[-1] + pred)
    cumulative_ev.pop(0)

# === Combine and plot ===
historical_cum = county_df[['Date', 'Electric Vehicle (EV) Total']].copy()
historical_cum['Cumulative EV'] = historical_cum['Electric Vehicle (EV) Total'].cumsum()
forecast_df = pd.DataFrame(future_rows)
forecast_df['Cumulative EV'] = forecast_df['Predicted EV Total'].cumsum() + historical_cum['Cumulative EV'].iloc[-1]
forecast_df['Source'] = 'Forecast'
historical_cum['Source'] = 'Historical'

combined = pd.concat([
    historical_cum[['Date', 'Cumulative EV', 'Source']],
    forecast_df[['Date', 'Cumulative EV', 'Source']]
])

# === Plotting ===
st.markdown("""
    <h3 style='margin-top: 40px; color: #00e5ff;'>📈 Forecasted Cumulative EV Growth</h3>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(12, 6))
for source, grp in combined.groupby('Source'):
    ax.plot(grp['Date'], grp['Cumulative EV'], label=source, marker='o')

ax.set_facecolor('#121212')
fig.patch.set_facecolor('#121212')
ax.grid(True, alpha=0.3)
ax.set_title(f"Cumulative EV Forecast - {county}", fontsize=16, color='#90caf9')
ax.set_xlabel("Date", fontsize=12, color='#eeeeee')
ax.set_ylabel("Cumulative EVs", fontsize=12, color='#eeeeee')
ax.tick_params(colors='#b0bec5')
ax.legend()
st.pyplot(fig)

# === Forecast Summary ===
historical_total = historical_cum['Cumulative EV'].iloc[-1]
forecasted_total = forecast_df['Cumulative EV'].iloc[-1]
if historical_total > 0:
    forecast_growth_pct = ((forecasted_total - historical_total) / historical_total) * 100
    trend = "increase 📈" if forecast_growth_pct > 0 else "decrease 📉"
    st.markdown(f"""
        <div class='glow-card'>
            <h4 style='color: #00e676;'>🔮 Forecast Summary</h4>
            <p>EV adoption in <b>{county}</b> is projected to <b>{trend}</b> by <b>{forecast_growth_pct:.2f}%</b> in the next 3 years.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Historical EV total is zero, cannot compute forecast.")

# === Footer ===
st.markdown("""
---
<div style='text-align: center; font-size: 14px; color: #90caf9;'>
    🚀 Developed as part of the <b>AICTE Green AI Internship</b> | REA SONI 
</div>
""", unsafe_allow_html=True)
