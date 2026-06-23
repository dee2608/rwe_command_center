# ============================================================================
# REAL-WORLD EVIDENCE COMMAND CENTER — CagriSema | US Market
# Streamlit Application  |  Single-File Deployment
# Credentials: UserID = RWE123 | Password = 1234
#
# Dependencies:
#   pip install streamlit pandas numpy plotly scipy requests
# Run:
#   streamlit run rwe_app.py
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import random
import time
import io
import os
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RWE Command Center | CagriSema",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Brand colours ─────────────────────────────────────────────────────────────
C_PRIMARY   = "#1171B9"
C_DARK      = "#0D558B"
C_LIGHT     = "#51ADEF"
C_GRAY      = "#666666"
C_LIGHTGRAY = "#F2F6FA"
C_WHITE     = "#FFFFFF"
C_BORDER    = "#D0DCE8"
C_ALERT     = "#C0392B"
C_WARN      = "#D4900A"
C_GOOD      = "#1A7C4F"
C_GRID      = "#E5EEF7"
# Light/pastel traffic-light variants — used for chart fills where a soft palette reads better than the saturated brand colors
C_GOOD_LT   = "#8FD9B6"
C_WARN_LT   = "#F5CC7A"
C_ALERT_LT  = "#F0A8A0"

# ── Global CSS ────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', Arial, sans-serif;
        background-color: {C_WHITE};
        color: #1A1A1A;
    }}

    /* Force white background across every native Streamlit wrapper.
       Streamlit Cloud falls back to a dark theme for these containers
       unless explicitly overridden — this is what was causing the
       black background even though custom components were already white. */
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stBottom"],
    section[data-testid="stSidebar"] > div,
    .main, .block-container, .stApp {{
        background-color: {C_WHITE} !important;
        color: #1A1A1A !important;
    }}
    [data-testid="stSidebar"] * {{ color: #1A1A1A; }}
    [data-testid="stSidebar"] {{ border-right: 1px solid {C_BORDER}; }}

    /* Hide Streamlit chrome */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }}

    /* Top navigation bar */
    .topbar {{
        background: {C_WHITE};
        border-bottom: 2px solid {C_BORDER};
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        position: sticky;
        top: 0;
        z-index: 999;
    }}
    .topbar-logo {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {C_PRIMARY};
        letter-spacing: -0.02em;
    }}
    .topbar-sub {{
        font-size: 0.75rem;
        color: {C_GRAY};
        font-weight: 400;
    }}
    .topbar-right {{
        font-size: 0.78rem;
        color: {C_GRAY};
    }}

    /* KPI cards */
    .kpi-card {{
        background: {C_WHITE};
        border-radius: 6px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 8px rgba(17,113,185,0.08);
        border: 1px solid {C_BORDER};
        margin-bottom: 0.5rem;
    }}
    .kpi-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: {C_GRAY};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.3rem;
    }}
    .kpi-value {{
        font-size: 1.85rem;
        font-weight: 700;
        color: {C_PRIMARY};
        line-height: 1.1;
    }}
    .kpi-sub {{
        font-size: 0.72rem;
        color: {C_GRAY};
        margin-top: 0.25rem;
    }}
    .kpi-pos {{ color: {C_GOOD}; font-weight: 600; }}
    .kpi-neg {{ color: {C_ALERT}; font-weight: 600; }}
    .kpi-warn {{ color: {C_WARN}; font-weight: 600; }}

    /* Section headers */
    .section-header {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {C_DARK};
        border-bottom: 2px solid {C_PRIMARY};
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
        margin-top: 1.2rem;
    }}

    /* Interface landing cards */
    .interface-card {{
        background: {C_WHITE};
        border-radius: 8px;
        padding: 1.6rem 1.4rem;
        box-shadow: 0 2px 12px rgba(17,113,185,0.09);
        border: 1px solid {C_BORDER};
        border-bottom: 3px solid {C_PRIMARY};
        cursor: pointer;
        transition: box-shadow 0.2s, transform 0.2s;
        min-height: 130px;
    }}
    .interface-card:hover {{
        box-shadow: 0 6px 20px rgba(17,113,185,0.16);
        transform: translateY(-3px);
    }}
    .card-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {C_PRIMARY};
        margin-bottom: 0.4rem;
    }}
    .card-desc {{
        font-size: 0.78rem;
        color: {C_GRAY};
        line-height: 1.45;
    }}
    .card-num {{
        font-size: 0.65rem;
        font-weight: 700;
        color: {C_LIGHT};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.5rem;
    }}

    /* Insight boxes */
    .insight-box {{
        background: {C_LIGHTGRAY};
        border-left: 4px solid {C_PRIMARY};
        border-radius: 0 6px 6px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }}
    .insight-obs {{ font-size: 0.82rem; color: #1A1A1A; margin-bottom: 0.3rem; }}
    .insight-label {{ font-size: 0.68rem; font-weight: 700; color: {C_PRIMARY};
                      text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.15rem; }}
    .insight-action {{ font-size: 0.82rem; color: {C_DARK}; font-weight: 500; }}
    .insight-kra {{ font-size: 0.75rem; color: {C_GOOD}; font-style: italic; margin-top: 0.25rem; }}

    /* Callout / info banner */
    .callout {{
        background: #EBF4FD;
        border: 1px solid {C_LIGHT};
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-size: 0.82rem;
        color: {C_DARK};
        margin-bottom: 1rem;
    }}
    .callout-warn {{
        background: #FFF8EC;
        border: 1px solid {C_WARN};
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-size: 0.82rem;
        color: #7A4500;
        margin-bottom: 1rem;
    }}
    .callout-good {{
        background: #EAF6F1;
        border: 1px solid {C_GOOD};
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-size: 0.82rem;
        color: #0F4A2E;
        margin-bottom: 1rem;
    }}

    /* Chat bubbles */
    .chat-user {{
        background: {C_PRIMARY};
        color: white;
        border-radius: 14px 14px 2px 14px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
        margin-left: 20%;
        font-size: 0.85rem;
    }}
    .chat-ai {{
        background: {C_LIGHTGRAY};
        color: #1A1A1A;
        border-radius: 14px 14px 14px 2px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        margin-right: 10%;
        font-size: 0.85rem;
        border-left: 3px solid {C_PRIMARY};
    }}
    .chat-source {{
        font-size: 0.7rem;
        color: {C_GRAY};
        font-style: italic;
        margin-top: 0.3rem;
    }}
    .chat-confidence {{
        display: inline-block;
        padding: 0.1rem 0.45rem;
        border-radius: 10px;
        font-size: 0.67rem;
        font-weight: 600;
        margin-right: 0.3rem;
    }}
    .conf-high {{ background: #D4EDDA; color: #155724; }}
    .conf-med  {{ background: #FFF3CD; color: #856404; }}
    .conf-low  {{ background: #F8D7DA; color: #721C24; }}

    /* SQL code block */
    .sql-block {{
        background: #1E2A38;
        color: #A8C9E8;
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        line-height: 1.6;
        overflow-x: auto;
        margin-bottom: 0.8rem;
    }}

    /* Federated node card */
    .fed-node {{
        background: {C_WHITE};
        border: 1px solid {C_BORDER};
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }}
    .fed-node-name {{ font-size: 0.82rem; font-weight: 700; color: {C_DARK}; }}
    .fed-node-pts  {{ font-size: 1.3rem; font-weight: 700; color: {C_PRIMARY}; }}
    .fed-node-stat {{ font-size: 0.72rem; color: {C_GRAY}; margin-top: 0.2rem; }}
    .status-dot-green  {{ display:inline-block; width:8px; height:8px;
                          border-radius:50%; background:{C_GOOD}; margin-right:5px; }}
    .status-dot-amber  {{ display:inline-block; width:8px; height:8px;
                          border-radius:50%; background:{C_WARN}; margin-right:5px; }}
    .status-dot-blue   {{ display:inline-block; width:8px; height:8px;
                          border-radius:50%; background:{C_PRIMARY}; margin-right:5px; }}

    /* Login card */
    .login-wrap {{
        max-width: 400px;
        margin: 5vh auto;
        background: {C_WHITE};
        border-radius: 10px;
        padding: 2.5rem 2.5rem 2rem;
        box-shadow: 0 4px 24px rgba(17,113,185,0.12);
        border: 1px solid {C_BORDER};
    }}
    .login-logo {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {C_PRIMARY};
        text-align: center;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
    }}
    .login-sub {{
        font-size: 0.78rem;
        color: {C_GRAY};
        text-align: center;
        margin-bottom: 1.8rem;
    }}
    .login-disclaimer {{
        font-size: 0.68rem;
        color: #AAAAAA;
        text-align: center;
        margin-top: 1.2rem;
        line-height: 1.5;
    }}

    /* Dividers */
    .hdivider {{
        border: none;
        border-top: 1px solid {C_BORDER};
        margin: 1rem 0;
    }}

    /* Funnel step */
    .funnel-step {{
        background: {C_LIGHTGRAY};
        border-left: 4px solid {C_PRIMARY};
        border-radius: 0 4px 4px 0;
        padding: 0.5rem 0.9rem;
        margin-bottom: 0.3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
    }}
    .funnel-step-label {{ color: #1A1A1A; font-weight: 500; }}
    .funnel-step-count {{ color: {C_PRIMARY}; font-weight: 700; }}
    .funnel-step-pct   {{ color: {C_GRAY}; font-size: 0.72rem; }}

    /* Bias badge */
    .bias-badge {{
        display: inline-block;
        background: #EBF4FD;
        border: 1px solid {C_LIGHT};
        border-radius: 12px;
        padding: 0.15rem 0.6rem;
        font-size: 0.7rem;
        color: {C_DARK};
        font-weight: 600;
        margin: 0.15rem;
    }}

    /* Stframlit widget overrides */
    div[data-testid="stSelectbox"] > div {{ border-color: {C_BORDER} !important; }}
    div[data-testid="stTextInput"] > div {{ border-color: {C_BORDER} !important; }}
    .stButton > button {{
        background: {C_PRIMARY};
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.5rem 1.2rem;
        transition: background 0.2s;
    }}
    .stButton > button:hover {{ background: {C_DARK}; color: white; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 0.82rem; font-weight: 600; color: {C_GRAY}; }}
    .stTabs [aria-selected="true"] {{ color: {C_PRIMARY} !important; border-bottom-color: {C_PRIMARY} !important; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DEMO DATA GENERATION
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def generate_ehr_data(n=500):
    """Generate synthetic EHR data for 500 representative patients (preview sample)."""
    np.random.seed(42)
    races = np.random.choice(
        ["White", "Hispanic", "Black", "Asian", "Other"],
        size=n, p=[0.61, 0.18, 0.13, 0.06, 0.02]
    )
    ages = np.clip(np.random.normal(52, 14, n).astype(int), 18, 89)
    sexes = np.random.choice(["Female", "Male", "Non-binary"], size=n, p=[0.50, 0.48, 0.02])
    bmi = np.clip(np.random.lognormal(3.44, 0.22, n), 18.5, 58.0)
    hba1c_base = np.clip(np.random.normal(78, 18, n), 42, 115)
    egfr = np.clip(np.random.normal(72, 22, n), 15, 120)
    treatment = np.random.choice(["CagriSema", "Semaglutide 2.4", "Tirzepatide",
                                   "Dulaglutide", "Liraglutide"], size=n,
                                  p=[0.318, 0.28, 0.22, 0.12, 0.062])
    state_names = ["CA","TX","FL","NY","OH","PA","IL","GA","NC","MI",
                   "AZ","WA","CO","MA","TN","IN","MO","MD","WI","MN"]
    state_probs = np.array([0.12,0.09,0.08,0.08,0.05,0.05,0.05,0.04,0.04,0.04,
                             0.04,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03,0.03])
    state_probs = state_probs / state_probs.sum()  # guard against float rounding (was raising ValueError: probabilities do not sum to 1)
    states = np.random.choice(state_names, size=n, p=state_probs)
    insurance = np.random.choice(["Commercial","Medicare","Medicaid","Cash"],
                                   size=n, p=[0.52,0.28,0.16,0.04])
    # Weight reduction at 12 months
    weight_redux = np.where(
        treatment == "CagriSema",
        np.clip(np.random.normal(15.3, 4.2, n), -2, 28),
        np.clip(np.random.normal(9.7,  3.8, n), -2, 22)
    )
    hba1c_redux = np.where(
        treatment == "CagriSema",
        np.clip(np.random.normal(1.84, 0.45, n), 0.2, 3.5),
        np.clip(np.random.normal(1.21, 0.40, n), 0.1, 3.0)
    )
    # PDC (adherence)
    pdc = np.where(
        treatment == "CagriSema",
        np.clip(np.random.beta(5.2, 3.1, n), 0, 1),
        np.clip(np.random.beta(3.4, 3.8, n), 0, 1)
    )
    discontinued = (pdc < 0.5) | (np.random.random(n) < 0.12)
    adi = np.clip(np.random.beta(2.5, 3.0, n) * 100, 1, 100)
    sdoh_flag = (adi > 65).astype(int)

    df = pd.DataFrame({
        "patient_id": [f"PT-{str(i+1).zfill(6)}" for i in range(n)],
        "age": ages,
        "sex": sexes,
        "race": races,
        "bmi": bmi.round(1),
        "hba1c_baseline": hba1c_base.round(1),
        "egfr": egfr.round(0).astype(int),
        "treatment": treatment,
        "state": states,
        "insurance": insurance,
        "weight_reduction_pct": weight_redux.round(1),
        "hba1c_reduction": hba1c_redux.round(2),
        "pdc": pdc.round(3),
        "discontinued": discontinued.astype(int),
        "adi_score": adi.round(1),
        "sdoh_flag": sdoh_flag,
    })
    return df


@st.cache_data
def generate_km_data():
    """Kaplan-Meier style survival data."""
    np.random.seed(7)
    days = np.arange(0, 366, 1)
    # CagriSema: slower drop-off
    km_cs  = np.exp(-0.00055 * days) * (1 - 0.003 * np.clip(days/365, 0, 1)**1.5)
    km_cmp = np.exp(-0.00095 * days) * (1 - 0.005 * np.clip(days/365, 0, 1)**1.4)
    ci_cs_lo  = km_cs  * 0.962
    ci_cs_hi  = km_cs  * 1.038
    ci_cmp_lo = km_cmp * 0.955
    ci_cmp_hi = km_cmp * 1.045
    return days, km_cs, km_cmp, ci_cs_lo, ci_cs_hi, ci_cmp_lo, ci_cmp_hi


@st.cache_data
def generate_wearable_data():
    """Rolling 12-week CGM time-series for the wearable feed."""
    np.random.seed(99)
    weeks = np.arange(1, 13)
    tir_mean = np.clip(55 + weeks * 1.4 + np.random.normal(0, 0.8, 12), 50, 80)
    cv_mean  = np.clip(36 - weeks * 0.65 + np.random.normal(0, 0.5, 12), 22, 38)
    steps    = np.clip(5200 + weeks * 145 + np.random.normal(0, 180, 12), 4500, 8500)
    weight   = np.clip(105 - weeks * 0.52 + np.random.normal(0, 0.25, 12), 94, 106)
    gi_score = np.clip(4.2 - weeks * 0.22 + np.random.normal(0, 0.15, 12), 1.2, 4.5)
    return pd.DataFrame({
        "week": weeks,
        "tir_pct": tir_mean.round(1),
        "cv_pct":  cv_mean.round(1),
        "steps":   steps.astype(int),
        "weight_kg": weight.round(1),
        "gi_score": gi_score.round(1),
    })


@st.cache_data
def generate_claims_summary():
    """Summarised claims data by state for the geo heatmap."""
    states_full = {
        "CA":9800,"TX":7200,"FL":6800,"NY":6100,"OH":3400,"PA":3300,
        "IL":3200,"GA":2800,"NC":2700,"MI":2600,"AZ":2400,"WA":2200,
        "CO":1900,"MA":1850,"TN":1800,"IN":1700,"MO":1650,"MD":1600,
        "WI":1550,"MN":1500,"NV":1400,"SC":1350,"AL":1300,"LA":1250,
        "KY":1200,"OR":1150,"OK":1100,"CT":1000,"UT":980,"IA":950,
        "MS":900,"AR":870,"KS":840,"NM":820,"NE":800,"ID":760,
        "WV":730,"HI":700,"NH":680,"ME":650,"MT":620,"RI":600,
        "DE":580,"SD":560,"ND":540,"AK":520,"VT":500,"WY":480,
    }
    df = pd.DataFrame(list(states_full.items()), columns=["state_abbr","rx_count"])
    df["opportunity_score"] = np.clip(
        (df["rx_count"].max() - df["rx_count"]) / df["rx_count"].max() * 100 + 10, 5, 95
    ).round(0)
    return df


@st.cache_data
def generate_payer_data():
    payers = ["UnitedHealth","Aetna","BCBS (National)","Cigna","Humana",
              "CVS/Caremark","Molina","Centene","Anthem","Kaiser"]
    pa_approval = [0.72,0.68,0.74,0.65,0.71,0.69,0.58,0.61,0.76,0.83]
    formulary_tier = [3,3,2,3,3,3,4,4,2,2]
    step_therapy = [True,True,False,True,True,True,True,True,False,False]
    obc_in_place = [True,True,True,False,True,False,False,False,True,True]
    return pd.DataFrame({
        "payer": payers,
        "pa_approval_rate": pa_approval,
        "formulary_tier": formulary_tier,
        "step_therapy_required": step_therapy,
        "obc_in_place": obc_in_place,
    })


# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    font_family="Inter, Arial, sans-serif",
    paper_bgcolor=C_WHITE,
    plot_bgcolor=C_WHITE,
    font_color="#1A1A1A",
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
)

def styled_fig(fig, title="", height=340):
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font_size=13, font_color=C_DARK, x=0),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=C_GRID, linecolor=C_BORDER, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=C_GRID, linecolor=C_BORDER, zeroline=False),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# ANTHROPIC API  (claude-sonnet-4-6 via Anthropic API)
# ─────────────────────────────────────────────────────────────────────────────
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

PHARMA_SYSTEM = """You are a senior pharmaceutical Real-World Evidence (RWE) analyst at a US pharmaceutical company working on CagriSema (cagrilintide + semaglutide), a fixed-ratio GLP-1 + amylin co-formulation for obesity and Type 2 diabetes in the US market.

You have access to synthetic but clinically realistic real-world datasets including:
- EHR records (500,000 patients): diagnoses (ICD-10), labs (HbA1c, eGFR, BMI), medications (RxNorm), demographics
- Pharmacy dispensing records (2.1 million events): NDC codes, PDC adherence, refill sequences, specialty pharmacy data
- Insurance claims (8.4 million lines): CPT/HCPCS, prior authorisation decisions, payer data, OBC flags
- Wearable/CGM data (892 enrolled patients): Dexcom G7 glucose, smartwatch activity, weight
- SDOH data: ADI, SVI, food desert flags, broadband access, specialist distance
- PRO surveys: IWQOL-Lite, EQ-5D, GIQLI, DTSQ

Key data points to reference:
- CagriSema cohort: 12,340 patients (31.8% of 38,750-patient study cohort)
- Mean weight reduction CagriSema: 15.3% vs 9.7% comparator GLP-1 class
- Mean HbA1c reduction: 1.84 pp vs 1.21 pp comparator
- PDC >80% (high adherence): 58% CagriSema vs 41% comparator at 12 months
- Discontinuation: 19.4% CagriSema vs 31.2% comparator
- Asian patients: 6.1% of cohort but 11.4% of High Efficacy / High Tolerability quadrant
- 68.3% average CGM time-in-range (up 11.2 pp from baseline)
- Top discontinuation driver: GI adverse events (nausea grade 2-3) first 8 weeks
- High-risk discontinuation segment: age 65+ with GI history (K21/K58) — 34% predicted 6-month discontinuation

US market context:
- GLP-1 market competitors: semaglutide 2.4 (Wegovy), tirzepatide (Zepbound), dulaglutide (Trulicity), liraglutide (Saxenda)
- >58% of US payers have at least one outcome-based contract
- CMS Medicare Part D coverage for anti-obesity medications evolving post-IRA 2022
- FDA Real-World Evidence Program guidance 2018 + 2023 draft guidance apply

When answering:
1. Always cite specific data values, ICD-10 codes, or RxNorm references where relevant
2. Connect observations to actionable next steps for RWE managers
3. Specify which KRA (Key Result Area) the recommended action addresses
4. For clinical questions, note whether evidence is from RWD, RCT, or published literature
5. Flag any limitations or potential biases in the analysis
6. Keep language professional and accessible — avoid unnecessary jargon

If the user asks about data not available in the datasets, state that clearly and suggest what additional data would be needed."""


def _get_anthropic_api_key():
    """Look for the API key in Streamlit secrets first (recommended for Streamlit
    Community Cloud — set under App settings > Secrets), then fall back to a
    plain environment variable for local/other deployments."""
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY", "")


def call_claude(messages: list, system: str = PHARMA_SYSTEM) -> str:
    """Call Anthropic API — returns response text. If no API key is configured,
    falls back to a free, data-grounded rule-based answer engine (see
    generate_fallback_insight below) so every AI feature in the app still works
    end-to-end with zero ongoing cost. As soon as an ANTHROPIC_API_KEY secret is
    added, this automatically switches to live Claude responses — no other code
    changes needed."""
    api_key = _get_anthropic_api_key()
    if not api_key:
        user_text = messages[-1]["content"] if messages else ""
        return generate_fallback_insight(user_text, system)
    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "system": system,
            "messages": messages,
        }
        resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            texts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            return " ".join(texts).strip()
        elif resp.status_code == 401:
            return ("API authentication failed — the configured ANTHROPIC_API_KEY appears to be "
                    "invalid or expired. Check the key under Streamlit Cloud > App settings > Secrets. "
                    "Showing a data-grounded fallback answer instead:\n\n"
                    + generate_fallback_insight(messages[-1]["content"] if messages else "", system))
        else:
            return generate_fallback_insight(messages[-1]["content"] if messages else "", system)
    except Exception:
        return generate_fallback_insight(messages[-1]["content"] if messages else "", system)


# ─────────────────────────────────────────────────────────────────────────────
# FREE, DATA-GROUNDED FALLBACK ANSWER ENGINE (used when no API key is set)
# ─────────────────────────────────────────────────────────────────────────────
# This does not call any external AI service. It pattern-matches the question
# against keywords and returns a specific, numbers-backed answer assembled from
# the same dataset figures used throughout the rest of the platform (see
# PHARMA_SYSTEM above for the canonical figures). This keeps every "Ask
# Anything" / "AI Insight" / "Generate Insight" feature fully functional with
# zero API cost. It is intentionally template-based rather than free-form —
# swap in real Claude calls later by adding an ANTHROPIC_API_KEY secret.

_FALLBACK_FACTS = {
    "cohort_size": "38,750 patients (CagriSema arm: 12,340 patients, 31.8% of cohort)",
    "weight": "CagriSema patients show 15.3% mean weight reduction at 12 months vs 9.7% for the GLP-1 comparator class",
    "hba1c": "CagriSema patients show a 1.84 percentage-point HbA1c reduction at 12 months vs 1.21 pp for comparators",
    "adherence": "58% of CagriSema patients reach PDC >80% adherence at 12 months vs 41% for comparators",
    "discontinuation": "19.4% of CagriSema patients discontinue by 12 months vs 31.2% for comparators",
    "asian": "Asian patients are 6.1% of the cohort but 11.4% of the High-Efficacy/High-Tolerability quadrant, with the highest adherence rate (71%) of any demographic group",
    "gi_risk": "Patients aged 65+ with a prior GI diagnosis (ICD-10 K21/K58) show a 34% predicted 6-month discontinuation rate — the single highest-risk segment, driven mainly by Grade 2-3 nausea in the first 8 weeks",
    "payer": "67.4% mean prior-authorization approval rate across payers; Kaiser (83%) and Anthem (76%) approve most readily, Molina (58%) and Centene (61%) least",
    "obc": "More than 58% of US commercial payers already hold at least one outcome-based contract; 72% of payers have an OBC in place specifically for CagriSema",
    "western_us": "CA, WA, OR, and CO show high obesity prevalence and high endocrinologist density, but CagriSema prescribing ranks in the bottom quartile there relative to comparators — a commercial access gap rather than a patient-population gap",
    "mace": "CagriSema shows a 4.2% MACE event rate vs 5.8% for the GLP-1 comparator class",
}

def _ff_pick_facts(text_lower):
    """Return the 1-3 most relevant fact keys for the given question text."""
    keyword_map = {
        "cohort_size":      ["cohort", "population", "how many patients", "sample size", "total patients"],
        "weight":           ["weight"],
        "hba1c":            ["hba1c", "glyc", "diabetes", "blood sugar", "a1c"],
        "adherence":        ["adher", "pdc", "compliance", "persisten"],
        "discontinuation":  ["discontinu", "drop", "stop", "churn"],
        "asian":            ["asian", "ethnic", "race", "demographic"],
        "gi_risk":          ["gi ", "nausea", "gastro", "vomit", "tolerab", "side effect", "adverse"],
        "payer":            ["payer", "prior auth", "pa rate", " pa ", "denial", "formulary"],
        "obc":              ["obc", "outcome-based", "outcome based", "contract"],
        "western_us":       ["western", "geograph", "state", "region", "ca ", "washington", "oregon", "colorado"],
        "mace":             ["mace", "cardiovascular", "cardiac", "heart"],
    }
    hits = []
    for key, kws in keyword_map.items():
        if any(kw in text_lower for kw in kws):
            hits.append(key)
    return hits[:3] if hits else ["cohort_size", "weight", "adherence"]


def generate_fallback_insight(prompt_text: str, system: str = "") -> str:
    """Free rule-based answer generator — no external API call."""
    text_lower = (prompt_text or "").lower()

    # ── Special case: Cohort Builder expects a strict JSON criteria payload ──
    if '"criteria"' in (system or "") and "icd_codes" in (system or ""):
        return json.dumps({
            "criteria": {
                "sex": "Female" if "female" in text_lower or "women" in text_lower else (
                       "Male" if "male" in text_lower and "female" not in text_lower else "Any"),
                "age_range": "50 years and above" if "50" in text_lower else "18 years and above",
                "condition_1": "Hypertension (ICD-10 I10) — diagnosed within last 24 months" if "hyperten" in text_lower else "Obesity / Type 2 Diabetes (per description provided)",
                "condition_2": "Type 2 Diabetes Mellitus (ICD-10 E11)" if "diabet" in text_lower else "—",
                "exclusions": "Pregnancy (O10), ESKD eGFR <15 (N18.5/N18.6), prior bariatric surgery",
                "index_date": "Most recent qualifying diagnosis",
                "follow_up": "12 months post-index",
            },
            "icd_codes": [
                {"code": "E11", "description": "Type 2 Diabetes Mellitus — unspecified", "status": "Primary inclusion"},
                {"code": "E11.9", "description": "Type 2 DM without complications", "status": "Included"},
                {"code": "I10", "description": "Essential (Primary) Hypertension", "status": "Primary inclusion"},
                {"code": "O10", "description": "Pre-existing hypertension in pregnancy", "status": "EXCLUDED by AI"},
                {"code": "N18.5", "description": "CKD Stage 5 / ESKD", "status": "EXCLUDED by AI (GLP-1 safety boundary)"},
            ],
            "narrative": "This cohort reflects the description provided and is drawn from the platform's 38,750-patient CagriSema RWE dataset. "
                         "(Generated by the built-in data-grounded engine — connect an ANTHROPIC_API_KEY secret for fully free-form AI extraction.)"
        })

    # ── Custom chart generator: structured 4-part recommendation ──
    if "recommended chart type" in text_lower or "sample sql query" in text_lower or "omop cdm table" in text_lower:
        chart_type = ("a box plot" if "insurance" in text_lower or "payer" in text_lower else
                       "a choropleth map" if any(k in text_lower for k in ["state","geograph","map","region"]) else
                       "a grouped bar chart" if any(k in text_lower for k in ["race","demographic","ethnic"]) else
                       "a violin plot" if any(k in text_lower for k in ["age","band"]) else
                       "an overlaid histogram" if any(k in text_lower for k in ["sex","gender","male","female"]) else
                       "a strip/scatter plot")
        return (f"**1. Recommended chart type:** {chart_type.capitalize()} — best suited to compare distributions "
                f"across the categorical groups in your request while preserving patient-level variance.\n\n"
                f"**2. Key insight:** Based on the CagriSema RWE dataset, the clearest signal is the consistent "
                f"gap between CagriSema (15.3% mean weight reduction, 58% PDC>80% adherence) and the GLP-1 "
                f"comparator class (9.7%, 41%) — segment cuts typically preserve this gap with some sub-group variation.\n\n"
                f"**3. Sample SQL (OMOP CDM):** `SELECT c.concept_name, AVG(m.value_as_number), COUNT(DISTINCT p.person_id) "
                f"FROM omop.PERSON p JOIN omop.MEASUREMENT m ON p.person_id = m.person_id "
                f"JOIN omop.CONCEPT c ON p.race_concept_id = c.concept_id GROUP BY c.concept_name;`\n\n"
                f"**4. Alternative:** A faceted small-multiples view if the audience needs to see every sub-group "
                f"on one slide.\n\n*(Generated by the built-in data-grounded engine — connect an ANTHROPIC_API_KEY "
                f"secret for fully free-form AI chart reasoning.)*")

    # ── General Q&A / insight generation: assemble from relevant facts ──
    fact_keys = _ff_pick_facts(text_lower)
    fact_lines = [f"- {_FALLBACK_FACTS[k]}" for k in fact_keys]

    if "observation" in text_lower and "implication" in text_lower and "kra" in text_lower:
        # Four-part agentic framework requested (Your Projects "Generate Insight")
        implication_extra = f" Specifically, {_FALLBACK_FACTS[fact_keys[1]]}." if len(fact_keys) > 1 else ""
        return (f"**Observation:** {_FALLBACK_FACTS[fact_keys[0]]}.\n\n"
                f"**Implication:** This pattern is consistent across the current study dataset and has direct "
                f"commercial and clinical relevance.{implication_extra}\n\n"
                f"**Recommended Action:** Cross-reference this finding against the Cohort Builder and Payer "
                f"Intelligence modules to scope a targeted intervention or sub-group analysis.\n\n"
                f"**KRA Impact:** Addressing this would directly support adherence, discontinuation, or market-access "
                f"KRAs depending on the team executing the action.\n\n"
                f"*(Generated by the built-in data-grounded engine using live platform figures — connect an "
                f"ANTHROPIC_API_KEY secret under Streamlit Secrets for fully free-form AI reasoning.)*")

    answer = "Based on the current CagriSema RWE dataset:\n\n" + "\n".join(fact_lines)
    answer += ("\n\nThis answer was generated by the platform's built-in data-grounded engine (no external API "
               "call, no cost) using the same figures shown throughout the dashboards. To enable fully free-form "
               "AI reasoning over arbitrary questions, add an ANTHROPIC_API_KEY secret under Streamlit Cloud > "
               "App settings > Secrets.")
    return answer


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "logged_in": False,
        "current_page": "landing",
        "chat_history": [],
        "cohort_chat": [],
        "cohort_built": False,
        "cohort_confirmed": False,
        "cohort_criteria": {},
        "active_study": "CagriSema — Retrospective Comparative Effectiveness",
        "custom_chart_history": [],
        "upload_done": False,
        "upload_filename": None,
        "fed_round": 7,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR
# ─────────────────────────────────────────────────────────────────────────────
def render_topbar(page_title=""):
    """Top bar now shows only a single clickable 'Home' control that returns the
    user to the interface-selection landing page. All other interfaces (Cohort
    Builder, Your Projects, etc.) are reached by opening their card from Home —
    they are no longer listed as separate clickable tabs across the top."""
    active = st.session_state.current_page

    col_logo, col_home, col_right = st.columns([5, 1, 2])
    with col_logo:
        st.markdown(f"""
        <div style="padding-top:0.3rem;">
          <div class="topbar-logo">RWE Command Center</div>
          <div class="topbar-sub">CagriSema &nbsp;|&nbsp; US Market &nbsp;|&nbsp; {datetime.now().strftime("%d %b %Y")}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_home:
        if active != "landing":
            if st.button("Home", key="topbar_home_btn", use_container_width=True):
                st.session_state.current_page = "landing"
                st.rerun()
        else:
            st.markdown(f"""
            <div style="font-size:0.82rem; font-weight:700; color:{C_PRIMARY};
                        padding-top:0.6rem; text-align:center;">Home</div>
            """, unsafe_allow_html=True)
    with col_right:
        st.markdown(f"""
        <div class="topbar-right" style="padding-top:0.7rem; text-align:right;">RWE123 &nbsp;|&nbsp; Logged In</div>
        """, unsafe_allow_html=True)
    st.markdown(f"<hr style='border-top:2px solid {C_BORDER}; margin:0.3rem 0 1.2rem;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_login():
    st.markdown("""
    <style>
    .block-container { max-width: 500px !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="login-wrap">
      <div class="login-logo">RWE Command Center</div>
      <div class="login-sub">AI-Powered Real-World Evidence Platform &nbsp;|&nbsp; CagriSema &nbsp;|&nbsp; US Market</div>
    """, unsafe_allow_html=True)

    uid  = st.text_input("User ID", placeholder="Enter your User ID", key="login_uid")
    pwd  = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")
    btn  = st.button("Sign In", use_container_width=True)

    if btn:
        if uid == "RWE123" and pwd == "1234":
            st.session_state.logged_in = True
            st.session_state.current_page = "landing"
            st.rerun()
        else:
            st.error("Invalid credentials. Use UserID: RWE123 | Password: 1234")

    st.markdown("""
      <div class="login-disclaimer">
        This platform contains simulated patient data for demonstration purposes only.<br>
        No real patient health information is processed in this environment.<br>
        Confidential — Internal Use Only
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_landing():
    render_topbar()
    st.markdown(f"""
    <div style="text-align:center; padding: 1.2rem 0 1.8rem;">
      <div style="font-size:1.6rem; font-weight:800; color:{C_PRIMARY}; letter-spacing:-0.03em;">
        Real-World Evidence Command Center
      </div>
      <div style="font-size:0.88rem; color:{C_GRAY}; margin-top:0.3rem;">
        Select an interface below to begin. Active drug: <strong>CagriSema</strong> &nbsp;|&nbsp; Market: <strong>United States</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cards = [
        ("Cohort Builder",
         "AI-powered natural language cohort definition with ICD code transparency, published precedent lookup, and digital twin simulation.",
         "cohort"),
        ("Your Projects",
         "Active and archived RWE studies with study-specific Kaplan-Meier, forest plots, Sankey flows, and agentic AI insight panels.",
         "projects"),
        ("Ask Anything",
         "Pharmaceutical RWE AI assistant grounded in uploaded data and a curated knowledge base. RAG-powered. Cite-verified responses.",
         "chat"),
        ("Upload Your Data",
         "Multi-source data ingestion, OMOP CDM v5.4 standardization, SQL transparency, and guided study type selection.",
         "upload"),
        ("Payer Intelligence",
         "Budget impact models, outcome-based contract simulators, ADR profiles, and competitive formulary analytics for US payers.",
         "payer"),
        ("Signal Lab",
         "Indication expansion, causal inference (DML/TMLE), federated learning network, CGM data feed, and predictive analytics.",
         "signal_lab"),
    ]

    for i in range(0, 6, 3):
        cols = st.columns(3, gap="medium")
        for j, col in enumerate(cols):
            if i + j < len(cards):
                title, desc, page = cards[i + j]
                with col:
                    st.markdown(f"""
                    <div class="interface-card">
                      <div class="card-title">{title}</div>
                      <div class="card-desc">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Open {title}", key=f"nav_{page}", use_container_width=True):
                        st.session_state.current_page = page
                        st.rerun()



# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 1 — COHORT BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def render_cohort():
    render_topbar("Cohort Builder")
    st.markdown("<div class='section-header'>Cohort Builder — Natural Language Cohort Definition</div>",
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="callout">
      <strong>How to use:</strong> Describe the patient population you need in plain English.
      The AI will extract inclusion/exclusion criteria, present them for your confirmation,
      generate the cohort with a population attrition funnel, display relevant ICD-10 code mappings,
      search published cohort precedents, and run a digital twin simulation.
    </div>
    """, unsafe_allow_html=True)

    # ── Cohort chat log ──
    for msg in st.session_state.cohort_chat:
        role_class = "chat-user" if msg["role"] == "user" else "chat-ai"
        st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

    # ── Input ──
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        cohort_input = st.text_area(
            "Cohort Definition Input",
            placeholder="Describe the patient population you need. For example: female patients aged 50 or above "
                        "with hypertension diagnosed within the last two years and Type 2 diabetes.",
            height=100,
            label_visibility="collapsed",
            key="cohort_input_box",
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        build_btn = st.button("Build Cohort", use_container_width=True, key="build_cohort_btn")

    if build_btn and cohort_input.strip():
        st.session_state.cohort_chat.append({"role": "user", "content": cohort_input.strip()})

        # Step 1 — AI extracts criteria
        with st.spinner("Extracting cohort criteria..."):
            sys_cohort = PHARMA_SYSTEM + """
When given a cohort description, respond in this EXACT JSON format (no markdown, no extra text):
{
  "criteria": {
    "sex": "...",
    "age_range": "...",
    "condition_1": "...",
    "condition_2": "...",
    "exclusions": "...",
    "index_date": "...",
    "follow_up": "..."
  },
  "icd_codes": [
    {"code": "E11", "description": "...", "status": "Primary inclusion"},
    {"code": "I10",  "description": "...", "status": "Primary inclusion"}
  ],
  "narrative": "Brief 2-sentence clinical rationale for why this cohort is relevant to CagriSema."
}"""
            raw = call_claude(
                [{"role": "user", "content": f"Extract cohort criteria from: {cohort_input}"}],
                system=sys_cohort
            )
            # Try to parse JSON; fall back to default
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = {
                    "criteria": {
                        "sex": "Female",
                        "age_range": "50 years and above",
                        "condition_1": "Hypertension (ICD-10 I10) — diagnosed within last 24 months",
                        "condition_2": "Type 2 Diabetes Mellitus (ICD-10 E11) — any duration",
                        "exclusions": "Pregnancy (O10), ESKD eGFR <15 (N18.5/N18.6), prior bariatric surgery",
                        "index_date": "Most recent qualifying diagnosis",
                        "follow_up": "12 months post-index"
                    },
                    "icd_codes": [
                        {"code": "E11",    "description": "Type 2 Diabetes Mellitus — unspecified",      "status": "Primary inclusion"},
                        {"code": "E11.9",  "description": "Type 2 DM without complications",             "status": "Included"},
                        {"code": "E11.65", "description": "Type 2 DM with hyperglycaemia",               "status": "Included"},
                        {"code": "I10",    "description": "Essential (Primary) Hypertension",            "status": "Primary inclusion"},
                        {"code": "I12",    "description": "Hypertensive chronic kidney disease",         "status": "Included — flag for renal sub-analysis"},
                        {"code": "O10",    "description": "Pre-existing hypertension in pregnancy",      "status": "EXCLUDED by AI"},
                        {"code": "N18.5",  "description": "CKD Stage 5 / ESKD",                          "status": "EXCLUDED by AI (GLP-1 safety boundary)"},
                    ],
                    "narrative": "This cohort represents post-menopausal women with convergent cardiometabolic risk. CagriSema's dual mechanism addressing glycaemic control and weight is highly relevant to this population."
                }
            st.session_state.cohort_criteria = parsed
            st.session_state.cohort_built = True

        confirm_msg = "I have extracted the following cohort criteria for your review and confirmation:"
        st.session_state.cohort_chat.append({"role": "assistant", "content": confirm_msg})
        st.rerun()

    # ── After criteria extracted: show confirmation panel ──
    if st.session_state.cohort_built and not st.session_state.cohort_confirmed:
        criteria = st.session_state.cohort_criteria.get("criteria", {})
        st.markdown("<div class='section-header'>Step 1 — Confirm Extracted Criteria</div>",
                    unsafe_allow_html=True)
        crit_rows = [
            ["Biological Sex",             criteria.get("sex","—")],
            ["Age Range",                  criteria.get("age_range","—")],
            ["Condition 1",                criteria.get("condition_1","—")],
            ["Condition 2",                criteria.get("condition_2","—")],
            ["AI-Suggested Exclusions",    criteria.get("exclusions","—")],
            ["Index Date",                 criteria.get("index_date","—")],
            ["Follow-up Window",           criteria.get("follow_up","—")],
        ]
        crit_df = pd.DataFrame(crit_rows, columns=["Criterion","AI-Extracted Value"])
        st.dataframe(crit_df, use_container_width=True, hide_index=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Confirm Criteria and Build Cohort", use_container_width=True, key="confirm_cohort"):
                st.session_state.cohort_confirmed = True
                st.rerun()
        with col_b:
            if st.button("Reset and Re-define", use_container_width=True, key="reset_cohort"):
                st.session_state.cohort_built = False
                st.session_state.cohort_confirmed = False
                st.session_state.cohort_chat = []
                st.session_state.cohort_criteria = {}
                st.rerun()

    # ── After confirmation: full cohort output ──
    if st.session_state.cohort_confirmed:
        st.markdown("<div class='section-header'>Step 2 — Population Attrition Funnel</div>",
                    unsafe_allow_html=True)

        funnel_steps = [
            ("Total Patients in Dataset",               "500,000", "100.0% of total"),
            ("After Sex Filter: Female",                "250,000", "50.0% of total"),
            ("After Age Filter: 50 years or above",     "112,400", "44.9% of female"),
            ("After Hypertension (past 24 months)",      "68,200", "60.7% of age-filtered"),
            ("After Type 2 Diabetes co-diagnosis",       "41,300", "60.6% of HTN-filtered"),
            ("After Exclusions Applied",                 "38,750", "93.8% retained after exclusions"),
        ]
        widths = [100, 82, 62, 48, 36, 30]
        for (label, count, pct), w in zip(funnel_steps, widths):
            is_final = "38,750" in count
            color = C_GOOD if is_final else C_PRIMARY
            st.markdown(f"""
            <div style="background:{color if is_final else C_LIGHTGRAY};
                        border-left:5px solid {color};
                        border-radius:0 5px 5px 0;
                        padding:0.55rem 1rem;
                        margin-bottom:0.3rem;
                        width:{w}%;
                        display:flex; justify-content:space-between; align-items:center;">
              <span style="font-size:0.82rem; font-weight:500;
                           color:{'white' if is_final else '#1A1A1A'};">{label}</span>
              <span>
                <strong style="font-size:1rem; color:{'white' if is_final else color};">{count}</strong>
                <span style="font-size:0.72rem; color:{'rgba(255,255,255,0.8)' if is_final else C_GRAY};
                             margin-left:0.6rem;">{pct}</span>
              </span>
            </div>
            """, unsafe_allow_html=True)

        narrative = st.session_state.cohort_criteria.get("narrative",
            "This cohort represents women aged 50+ with hypertension and Type 2 diabetes — a high-priority "
            "population for CagriSema evidence generation given the drug's cardiometabolic profile.")
        st.markdown(f"""
        <div class="callout-good" style="margin-top:0.8rem;">
          <strong>Final Qualifying Cohort: 38,750 patients</strong><br>{narrative}
        </div>
        """, unsafe_allow_html=True)

        # ICD Code Panel
        st.markdown("<div class='section-header'>Step 3 — ICD-10 Code Transparency</div>",
                    unsafe_allow_html=True)
        icd_data = st.session_state.cohort_criteria.get("icd_codes", [])
        if icd_data:
            icd_df = pd.DataFrame(icd_data)
            def color_status(val):
                if "EXCLUDED" in str(val):   return "color: #C0392B; font-weight:600;"
                if "Primary" in str(val):    return "color: #1171B9; font-weight:600;"
                if "flag" in str(val).lower(): return "color: #D4900A;"
                return ""
            st.dataframe(
                icd_df.rename(columns={"code":"ICD-10 Code","description":"Description","status":"Inclusion Status"}),
                use_container_width=True, hide_index=True
            )

        # Published Precedent
        st.markdown("<div class='section-header'>Step 4 — Published Cohort Precedents</div>",
                    unsafe_allow_html=True)
        prec_data = {
            "Study": ["SUSTAIN-6 (NEJM 2016)","SELECT Trial (NEJM 2023)","STEP-4 RWE Cohort (2022)"],
            "Cohort Definition Used": [
                "T2DM, HbA1c ≥7%, ≥50 yrs with CVD or ≥60 with risk factors",
                "Obesity (BMI≥27), no T2DM, prior MACE — no age restriction",
                "BMI≥30 or ≥27 with comorbidity, semaglutide-treated, 12-month follow-up"
            ],
            "Key Difference from Yours": [
                "Requires CVD history — your cohort is broader (primary prevention included)",
                "Excludes T2DM — your cohort includes T2DM patients",
                "No hypertension requirement — your cohort adds HTN as co-criterion"
            ],
            "Recommendation": ["Adapt exclusions","Diverge — different population","Adopt follow-up window"],
        }
        st.dataframe(pd.DataFrame(prec_data), use_container_width=True, hide_index=True)

        # Digital Twin
        st.markdown("<div class='section-header'>Step 5 — Digital Twin Simulation</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          <strong>Digital Twin Active:</strong> 500 virtual patient replicas generated from the real cohort distribution.
          Each twin is parameterized with age, sex, BMI, HbA1c, eGFR, and comorbidity burden.
          Simulated outcomes are compared against observed RWD. Calibration alerts flag divergences requiring review.
        </div>
        """, unsafe_allow_html=True)

        np.random.seed(42)
        weeks_dt = np.arange(0, 53, 4)
        real_wt   = 105 - weeks_dt * 0.28 + np.random.normal(0, 0.5, len(weeks_dt))
        twin_wt   = 105 - weeks_dt * 0.31 + np.random.normal(0, 0.3, len(weeks_dt))
        fig_dt = go.Figure()
        fig_dt.add_trace(go.Scatter(x=weeks_dt, y=real_wt,  mode="lines+markers",
                                    name="Observed RWD Cohort",
                                    line=dict(color=C_PRIMARY, width=2.5),
                                    marker=dict(size=5)))
        fig_dt.add_trace(go.Scatter(x=weeks_dt, y=twin_wt,  mode="lines",
                                    name="Digital Twin Projection",
                                    line=dict(color=C_WARN, width=2, dash="dash")))
        fig_dt.add_hrect(y0=twin_wt[-1]-1.2, y1=twin_wt[-1]+1.2,
                          fillcolor="rgba(212,144,10,0.07)", line_width=0,
                          annotation_text="Calibration Zone", annotation_position="top right")
        styled_fig(fig_dt, "Digital Twin — Mean Body Weight Trajectory (kg) over 52 Weeks")
        fig_dt.update_layout(xaxis_title="Weeks from Index Date", yaxis_title="Mean Body Weight (kg)")
        st.plotly_chart(fig_dt, use_container_width=True)

        # Agentic insight
        st.markdown("""
        <div class="insight-box">
          <div class="insight-label">Agentic AI Recommendation</div>
          <div class="insight-obs">
            <strong>Observation:</strong> Asian female patients aged 50-65 within this cohort show a 31% higher baseline BMI
            than the cohort average, yet are currently underrepresented in GLP-1 clinical studies by approximately 4x
            relative to their disease burden.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Export Asian female sub-cohort to Interface 2 (Projects) as a priority segment
            for targeted HCP outreach in CA, NY, and TX. Submit sub-group analysis proposal to medical affairs for
            regulatory inclusion. Cross-reference SDOH broadband access data for telehealth expansion feasibility.
          </div>
          <div class="insight-kra">
            KRA Impact: Addressing this sub-group gap could increase CagriSema-treated patient enrollment by 8-12%
            and strengthen the ethnic diversity evidence package required for label expansion.
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            if st.button("Export Cohort to Your Projects", key="export_cohort", use_container_width=True):
                st.success("Cohort exported to Interface 2 — Your Projects. "
                           "It is now available as 'CagriSema — Custom Cohort (Hypertension + T2DM, Female 50+)'")
        with col_exp2:
            cohort_export_df = generate_ehr_data()
            xlsx_buffer = io.BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine="xlsxwriter") as writer:
                cohort_export_df.to_excel(writer, index=False, sheet_name="Cohort Patients")
                icd_export = st.session_state.cohort_criteria.get("icd_codes", [])
                if icd_export:
                    pd.DataFrame(icd_export).to_excel(writer, index=False, sheet_name="ICD-10 Codes")
            st.download_button(
                "Download Full Cohort (Excel)",
                data=xlsx_buffer.getvalue(),
                file_name=f"cagrisema_cohort_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_cohort_xlsx",
                use_container_width=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 2 — YOUR PROJECTS
# ─────────────────────────────────────────────────────────────────────────────
def render_projects():
    render_topbar("Your Projects")
    df = generate_ehr_data()

    studies = {
        "CagriSema — Retrospective Comparative Effectiveness": "active",
        "CagriSema — Pragmatic Clinical Trial (CATALYST-RWE)": "active",
        "CagriSema — Prospective Observational (WEIGHT-FORWARD)": "active",
        "CagriSema — Claims-Based Adherence Analysis": "active",
        "CagriSema — Registry Study (APEX-OB)": "paused",
        "Semaglutide 2.4 — Retrospective Label Expansion": "archived",
        "Tirzepatide — Comparative Safety (Internal Reference)": "active",
    }

    study_options = [f"{'[ACTIVE] ' if v=='active' else '[PAUSED] ' if v=='paused' else '[ARCHIVED] '}{k}"
                     for k, v in studies.items()]
    sel = st.selectbox("Select Study", study_options, key="study_sel",
                       index=0, label_visibility="visible")
    study_name = sel.split("] ", 1)[1] if "] " in sel else sel
    st.session_state.active_study = study_name

    # KPI row
    st.markdown("<div class='section-header'>Key Performance Indicators</div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    kpi_sets = {
        "CagriSema — Retrospective Comparative Effectiveness": [
            ("38,750","Total Cohort","patients","Up 4.2% vs prior quarter","pos"),
            ("12,340","CagriSema Arm","patients","31.8% of cohort","neutral"),
            ("15.3%","Weight Reduction","mean at 12M","vs 9.7% comparator","pos"),
            ("1.84 pp","HbA1c Reduction","mean at 12M","vs 1.21 pp comparator","pos"),
            ("58%","PDC >80% Adherence","CagriSema","vs 41% comparator","pos"),
            ("19.4%","Discontinuation","CagriSema","vs 31.2% comparator","pos"),
        ],
        "CagriSema — Claims-Based Adherence Analysis": [
            ("2.1M","Dispense Events","36-month window","Across 50 states","neutral"),
            ("67.4%","PA Approval Rate","prior auth","Payer mix: commercial 52%","warn"),
            ("87.3%","Specialty Pharm Rate","of CagriSema fills","SP channel dominant","neutral"),
            ("$340","Avg Patient Copay","per 28-day supply","Post-rebate estimate","warn"),
            ("4.2 fills","Avg Refill Sequence","per patient/year","Adherence proxy","warn"),
            ("12.3%","Market Share","GLP-1 class","Trailing 12M prescriptions","pos"),
        ],
    }
    kpis = kpi_sets.get(study_name, kpi_sets["CagriSema — Retrospective Comparative Effectiveness"])
    for col, (val, label, unit, sub, trend) in zip([c1,c2,c3,c4,c5,c6], kpis):
        cls = "kpi-pos" if trend=="pos" else ("kpi-warn" if trend=="warn" else "kpi-sub")
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{val}</div>
              <div class="kpi-sub">{unit}</div>
              <div class="{cls}" style="font-size:0.72rem;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # Dropdown filters
    st.markdown("<div class='section-header'>Analysis Filters</div>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        filter_sex = st.selectbox("Sex", ["All","Female","Male"], key="f_sex")
    with fc2:
        filter_race = st.selectbox("Race / Ethnicity",
                                    ["All","White","Hispanic","Black","Asian","Other"], key="f_race")
    with fc3:
        filter_ins = st.selectbox("Insurance Type",
                                   ["All","Commercial","Medicare","Medicaid","Cash"], key="f_ins")
    with fc4:
        filter_age = st.selectbox("Age Band",
                                   ["All","18-40","41-55","56-70","71+"], key="f_age")

    # Apply filters
    dff = df.copy()
    if filter_sex  != "All": dff = dff[dff.sex == filter_sex]
    if filter_race != "All": dff = dff[dff.race == filter_race]
    if filter_ins  != "All": dff = dff[dff.insurance == filter_ins]
    if filter_age  != "All":
        band = {"18-40":(18,40),"41-55":(41,55),"56-70":(56,70),"71+":(71,120)}[filter_age]
        dff = dff[(dff.age >= band[0]) & (dff.age <= band[1])]

    tabs = st.tabs([
        "Kaplan-Meier", "Spider Chart", "Sankey Flow", "Mosaic Plot",
        "Forest Plot", "Waterfall", "Bubble Chart", "Swimmer Plot",
        "Bump Chart", "AI Insights"
    ])

    # ── TAB 1: Kaplan-Meier ──
    with tabs[0]:
        st.markdown("<div class='section-header'>Kaplan-Meier — Time to Treatment Discontinuation</div>",
                    unsafe_allow_html=True)
        days, km_cs, km_cmp, ci_cs_lo, ci_cs_hi, ci_cmp_lo, ci_cmp_hi = generate_km_data()
        fig_km = go.Figure()
        fig_km.add_trace(go.Scatter(
            x=np.concatenate([days, days[::-1]]),
            y=np.concatenate([ci_cs_hi, ci_cs_lo[::-1]]),
            fill="toself", fillcolor="rgba(17,113,185,0.10)",
            line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", showlegend=False
        ))
        fig_km.add_trace(go.Scatter(
            x=np.concatenate([days, days[::-1]]),
            y=np.concatenate([ci_cmp_hi, ci_cmp_lo[::-1]]),
            fill="toself", fillcolor="rgba(81,173,239,0.10)",
            line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip", showlegend=False
        ))
        fig_km.add_trace(go.Scatter(x=days, y=km_cs,  mode="lines", name="CagriSema",
                                     line=dict(color=C_PRIMARY, width=2.5, shape="hv")))
        fig_km.add_trace(go.Scatter(x=days, y=km_cmp, mode="lines", name="GLP-1 Comparator",
                                     line=dict(color=C_LIGHT, width=2.5, shape="hv", dash="dash")))
        fig_km.add_annotation(
            x=300, y=0.72,
            text="Log-rank p < 0.001<br>HR = 0.58 (95% CI: 0.51–0.66)",
            showarrow=False,
            bgcolor=C_LIGHTGRAY,
            bordercolor=C_BORDER,
            font=dict(size=10, color=C_DARK),
            align="left"
        )
        for d in [90, 180, 270, 365]:
            fig_km.add_vline(x=d, line_width=0.5, line_dash="dot", line_color=C_GRID)
        styled_fig(fig_km, "", 400)
        fig_km.update_layout(
            xaxis_title="Days from Index Date",
            yaxis_title="Probability of Remaining on Therapy",
            yaxis_range=[0.5, 1.02],
            legend=dict(x=0.7, y=0.95)
        )
        st.plotly_chart(fig_km, use_container_width=True)
        st.markdown("""
        <div class="callout">
          At 365 days, <strong>80.6% of CagriSema patients</strong> remain on therapy versus
          <strong>68.8% of GLP-1 comparator patients</strong>. The divergence is most pronounced
          in the first 90 days — consistent with the tolerability advantage reducing early dropout.
          Hazard Ratio: 0.58 (CagriSema favoured). Log-rank p &lt; 0.001.
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 2: Spider Chart ──
    with tabs[1]:
        st.markdown("<div class='section-header'>Spider Chart — Eight-Axis Clinical Profile</div>",
                    unsafe_allow_html=True)
        categories = ["Weight Reduction","HbA1c Improvement","Systolic BP Reduction",
                      "Tolerability Score","Adherence Rate","Time-in-Range (CGM)",
                      "MACE Risk Reduction","Renal Safety"]
        cs_vals  = [88, 82, 67, 79, 85, 78, 74, 90]
        cmp_vals = [62, 64, 58, 58, 66, 60, 68, 85]
        fig_sp = go.Figure()
        fig_sp.add_trace(go.Scatterpolar(r=cs_vals  + [cs_vals[0]],
                                          theta=categories + [categories[0]],
                                          fill="toself", name="CagriSema",
                                          fillcolor="rgba(17,113,185,0.18)",
                                          line=dict(color=C_PRIMARY, width=2.5)))
        fig_sp.add_trace(go.Scatterpolar(r=cmp_vals + [cmp_vals[0]],
                                          theta=categories + [categories[0]],
                                          fill="toself", name="GLP-1 Comparator",
                                          fillcolor="rgba(81,173,239,0.12)",
                                          line=dict(color=C_LIGHT, width=2, dash="dash")))
        fig_sp.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                                gridcolor=C_GRID),
                angularaxis=dict(tickfont=dict(size=11, color=C_DARK))
            ),
            paper_bgcolor=C_WHITE,
            font_family="Inter, Arial",
            legend=dict(orientation="h", x=0.2, y=-0.12),
            height=420,
            margin=dict(l=60, r=60, t=40, b=60),
            title=dict(text="Clinical Profile Index (0–100, higher = better)", font_size=12, x=0)
        )
        st.plotly_chart(fig_sp, use_container_width=True)

    # ── TAB 3: Sankey ──
    with tabs[2]:
        st.markdown("<div class='section-header'>Sankey Flow — Patient Treatment Pathway</div>",
                    unsafe_allow_html=True)
        labels = ["Obesity + T2DM Dx","Metformin (1L)","SGLT2i (2L)","DPP-4i (2L)",
                  "Insulin (2L)","CagriSema (GLP-1)","Sema 2.4 / Tirz (GLP-1)",
                  "Continued CagriSema","Switched to Comparator","Discontinued"]
        source = [0,1,1,1,2,3,4,5,5,6]
        target = [1,2,3,4,5,5,6,7,9,9]
        value  = [38750,14200,9800,7400,7200,6800,5600,9860,2480,8720]
        colors = [C_PRIMARY,C_LIGHT,"#85BFEF","#A8D2F3",C_PRIMARY,C_PRIMARY,
                  C_LIGHT,C_GOOD,C_WARN,C_ALERT]
        fig_sk = go.Figure(go.Sankey(
            node=dict(pad=18, thickness=20, line=dict(color=C_BORDER, width=0.5),
                      label=labels, color=colors),
            link=dict(source=source, target=target, value=value,
                      color="rgba(17,113,185,0.12)")
        ))
        fig_sk.update_layout(
            paper_bgcolor=C_WHITE, font_family="Inter, Arial",
            font_size=11, height=420,
            margin=dict(l=10,r=10,t=40,b=10),
            title=dict(text="Patient Treatment Journey — CagriSema Cohort (n=38,750)",
                       font_size=12, x=0)
        )
        st.plotly_chart(fig_sk, use_container_width=True)
        st.markdown("""
        <div class="callout">
          Of 38,750 qualifying patients, <strong>7,200 escalated directly from second-line agents to CagriSema</strong>.
          The primary switching point is from SGLT2i (second-line) — representing the highest-volume CagriSema uptake pathway.
          9,860 patients (25.4%) remained on CagriSema at 12 months without modification — the strongest persistence signal in the GLP-1 class.
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 4: Mosaic ──
    with tabs[3]:
        st.markdown("<div class='section-header'>Mosaic Plot — Demographic vs Adherence Cross-Tabulation</div>",
                    unsafe_allow_html=True)
        races_m = ["White","Hispanic","Black","Asian","Other"]
        pop_share = [0.61, 0.18, 0.13, 0.06, 0.02]
        high_adh  = [0.62, 0.54, 0.48, 0.71, 0.59]
        med_adh   = [0.24, 0.29, 0.31, 0.21, 0.26]
        low_adh   = [0.14, 0.17, 0.21, 0.08, 0.15]
        fig_mo = go.Figure()
        x_pos = 0
        bar_colors = [C_GOOD, C_WARN, C_ALERT]
        bar_labels  = ["High Adherence (PDC>80%)", "Moderate (PDC 50-80%)", "Low (PDC<50%)"]
        adh_groups  = [high_adh, med_adh, low_adh]
        for ri, (race, share) in enumerate(zip(races_m, pop_share)):
            w = share * 100
            y_bot = 0
            for gi, (adh, color, lbl) in enumerate(zip(adh_groups, bar_colors, bar_labels)):
                h = adh[ri] * 100
                fig_mo.add_trace(go.Bar(
                    x=[w], y=[h], base=[y_bot],
                    name=lbl if ri == 0 else None,
                    showlegend=(ri == 0),
                    marker_color=color,
                    marker_line=dict(color=C_WHITE, width=1),
                    width=w * 0.88,
                    offset=x_pos - w * 0.44,
                    customdata=[[race, lbl, round(h, 1)]],
                    hovertemplate="%{customdata[0]} — %{customdata[1]}: %{customdata[2]}%<extra></extra>",
                    text=f"{race}" if gi == 0 else None,
                    textposition="inside" if gi == 0 else "none",
                    insidetextanchor="start",
                    textfont=dict(size=10, color=C_WHITE),
                ))
                y_bot += h
            x_pos += w + 2
        fig_mo.update_layout(
            barmode="stack",
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
            font_family="Inter, Arial",
            xaxis=dict(showticklabels=False, showgrid=False, title="Racial / Ethnic Group (width = population share)"),
            yaxis=dict(title="Adherence Distribution (%)", range=[0, 105], showgrid=True, gridcolor=C_GRID),
            height=400, margin=dict(l=10,r=10,t=40,b=40),
            legend=dict(orientation="h", x=0, y=-0.18),
            title=dict(text="Adherence Tier by Race/Ethnicity — Mosaic (Marimekko) Plot", font_size=12, x=0)
        )
        st.plotly_chart(fig_mo, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">SDOH Insight</div>
          <div class="insight-obs">
            Asian patients show the highest high-adherence rate (71%) and the lowest low-adherence rate (8%),
            despite being the smallest demographic group (6.1% of cohort). Black patients show the highest
            low-adherence rate (21%), suggesting a targeted patient support programme is warranted.
          </div>
          <div class="insight-action">
            Action: Design culturally tailored adherence support for Black patients — specifically addressing
            cost barriers (copay assistance) and access barriers (specialty pharmacy proximity from SDOH data).
          </div>
          <div class="insight-kra">KRA: Increase overall PDC >80% rate from 58% to 65% within 18 months.</div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 5: Forest Plot ──
    with tabs[4]:
        st.markdown("<div class='section-header'>Forest Plot — Sub-Group Treatment Effect Heterogeneity</div>",
                    unsafe_allow_html=True)
        subgroups = ["Age 18-40","Age 41-55","Age 56-70","Age 71+",
                     "Female","Male",
                     "White","Hispanic","Black","Asian",
                     "BMI <30","BMI 30-40","BMI >40",
                     "Commercial Insurance","Medicare","Medicaid"]
        or_vals  = [0.71,0.62,0.58,0.67,0.57,0.61,0.60,0.63,0.69,0.52,0.74,0.60,0.55,0.58,0.64,0.70]
        ci_lower = [v - (0.12 + 0.04*abs(0.6-v)) for v in or_vals]
        ci_upper = [v + (0.14 + 0.04*abs(0.6-v)) for v in or_vals]
        n_pts    = [420,2800,4200,1100,5200,4800,6200,2400,1800,720,3100,5400,2200,6800,3200,1400]

        y_pos = list(range(len(subgroups)))
        fig_fp = go.Figure()
        # CI lines
        for i, (lo, hi, y) in enumerate(zip(ci_lower, ci_upper, y_pos)):
            fig_fp.add_shape(type="line", x0=lo, x1=hi, y0=y, y1=y,
                              line=dict(color=C_GRAY, width=1.5))
        # Point estimates
        fig_fp.add_trace(go.Scatter(
            x=or_vals, y=y_pos,
            mode="markers",
            marker=dict(symbol="square", size=[max(6, min(16, n/600)) for n in n_pts],
                        color=C_PRIMARY, line=dict(color=C_DARK, width=1)),
            customdata=list(zip(subgroups, or_vals, ci_lower, ci_upper)),
            hovertemplate="%{customdata[0]}<br>OR: %{customdata[1]:.2f} (%{customdata[2]:.2f}–%{customdata[3]:.2f})<extra></extra>",
            showlegend=False
        ))
        fig_fp.add_vline(x=1.0, line_width=1.5, line_dash="dot", line_color=C_ALERT)
        fig_fp.add_vline(x=0.60, line_width=1, line_dash="dash", line_color=C_LIGHT)
        fig_fp.update_layout(
            yaxis=dict(ticktext=subgroups, tickvals=y_pos, showgrid=False,
                       autorange="reversed", tickfont=dict(size=11)),
            xaxis=dict(title="Odds Ratio (CagriSema vs Comparator) — <1 favours CagriSema",
                       showgrid=True, gridcolor=C_GRID, zeroline=False,
                       range=[0.3, 1.3]),
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
            font_family="Inter, Arial",
            height=520,
            margin=dict(l=140, r=40, t=40, b=40),
            title=dict(text="Forest Plot — Odds Ratio of Discontinuation by Sub-Group", font_size=12, x=0)
        )
        st.plotly_chart(fig_fp, use_container_width=True)

    # ── TAB 6: Waterfall ──
    with tabs[5]:
        st.markdown("<div class='section-header'>Waterfall Chart — Individual Patient Weight Reduction at 12 Months</div>",
                    unsafe_allow_html=True)
        np.random.seed(12)
        n_wf = 80
        wt_changes = np.sort(
            np.concatenate([
                np.random.normal(-16, 5.5, 62),
                np.random.normal(2.5, 2.0, 18)
            ])
        )[::-1]
        bar_colors_wf = [C_GOOD if v < 0 else C_ALERT for v in wt_changes]
        fig_wf = go.Figure(go.Bar(
            x=list(range(len(wt_changes))),
            y=wt_changes,
            marker_color=bar_colors_wf,
            marker_line_width=0,
            hovertemplate="Patient %{x}: %{y:.1f}% weight change<extra></extra>"
        ))
        median_val = float(np.median(wt_changes))
        fig_wf.add_hline(y=median_val, line_dash="dash", line_color=C_PRIMARY, line_width=2,
                          annotation_text=f"Median: {median_val:.1f}%",
                          annotation_font_size=11, annotation_font_color=C_PRIMARY)
        fig_wf.add_hline(y=0, line_color=C_BORDER, line_width=1)
        styled_fig(fig_wf, "Individual Patient Weight Reduction — CagriSema Arm (n=80 sample, sorted)", 380)
        fig_wf.update_layout(
            xaxis_title="Individual Patients (sorted by response)",
            yaxis_title="% Weight Change at 12 Months",
            showlegend=False
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    # ── TAB 7: Bubble Chart ──
    with tabs[6]:
        st.markdown("<div class='section-header'>Risk-Benefit Quadrant — Sub-Group Bubble Chart</div>",
                    unsafe_allow_html=True)
        seg_names = ["Asian F 50-65","White F 41-55","Hispanic F 56-70",
                     "White M 41-55","Black F 56-70","Hispanic M 40-55",
                     "White M 65+","Asian M 50-65","Black M 65+"]
        efficacy  = [0.88, 0.82, 0.76, 0.74, 0.68, 0.71, 0.65, 0.84, 0.62]
        tolerab   = [0.84, 0.80, 0.73, 0.77, 0.65, 0.70, 0.58, 0.82, 0.55]
        pop_size  = [820,3200,1800,2900,1400,1600,980,740,880]
        quad_colors = []
        for e, t in zip(efficacy, tolerab):
            if e > 0.75 and t > 0.75: quad_colors.append(C_GOOD)
            elif e > 0.75 and t <= 0.75: quad_colors.append(C_WARN)
            elif e <= 0.75 and t > 0.75: quad_colors.append(C_LIGHT)
            else: quad_colors.append(C_ALERT)

        fig_bb = go.Figure()
        fig_bb.add_vrect(x0=0.75, x1=1.05, fillcolor="rgba(26,124,79,0.04)", line_width=0)
        fig_bb.add_vrect(x0=0.45, x1=0.75, fillcolor="rgba(212,144,10,0.03)", line_width=0)
        fig_bb.add_hrect(y0=0.75, y1=1.05, fillcolor="rgba(26,124,79,0.04)", line_width=0)
        fig_bb.add_vline(x=0.75, line_dash="dash", line_color=C_BORDER, line_width=1)
        fig_bb.add_hline(y=0.75, line_dash="dash", line_color=C_BORDER, line_width=1)

        for i in range(len(seg_names)):
            fig_bb.add_trace(go.Scatter(
                x=[efficacy[i]], y=[tolerab[i]],
                mode="markers+text",
                marker=dict(size=max(16, min(42, pop_size[i]/80)),
                            color=quad_colors[i], opacity=0.82,
                            line=dict(color=C_WHITE, width=2)),
                text=[seg_names[i].split(" ")[0:2][0]],
                textposition="top center",
                textfont=dict(size=9, color=C_DARK),
                name=seg_names[i],
                hovertemplate=f"<b>{seg_names[i]}</b><br>Efficacy: {efficacy[i]:.0%}<br>Tolerability: {tolerab[i]:.0%}<br>n={pop_size[i]:,}<extra></extra>",
                showlegend=False
            ))

        for text, x, y in [
            ("High Efficacy / High Tolerability\nPriority Segment", 0.9, 0.98),
            ("Lower Efficacy / High Tolerability\nAdherence Opportunity", 0.6, 0.98),
            ("High Efficacy / GI Burden\nSupport Programme", 0.9, 0.62),
            ("Review / Reconsider", 0.6, 0.62),
        ]:
            fig_bb.add_annotation(x=x, y=y, text=text, showarrow=False,
                                   font=dict(size=9, color=C_GRAY), align="center")
        styled_fig(fig_bb, "Risk-Benefit Quadrant — Patient Sub-Group Positioning", 460)
        fig_bb.update_layout(
            xaxis=dict(title="Relative Efficacy (HbA1c Reduction vs Comparator)", range=[0.45, 1.05]),
            yaxis=dict(title="Relative Tolerability (Inverse GI Adverse Event Rate)", range=[0.45, 1.05]),
        )
        st.plotly_chart(fig_bb, use_container_width=True)

    # ── TAB 8: Swimmer Plot ──
    with tabs[7]:
        st.markdown("<div class='section-header'>Swimmer Plot — Individual Patient Treatment Timeline</div>",
                    unsafe_allow_html=True)
        np.random.seed(55)
        n_swim = 30
        durations = np.sort(np.clip(np.random.normal(280, 80, n_swim), 30, 365))[::-1]
        fig_sw = go.Figure()
        for i, dur in enumerate(durations):
            fig_sw.add_trace(go.Bar(
                x=[dur], y=[i],
                orientation="h",
                marker_color=C_PRIMARY if dur > 200 else (C_WARN if dur > 90 else C_ALERT),
                marker_line_width=0,
                showlegend=False,
                hovertemplate=f"Patient {i+1}: {int(dur)} days on therapy<extra></extra>",
                width=0.7,
            ))
            # AE events
            if random.random() < 0.4:
                ae_day = random.uniform(14, min(dur*0.6, 280))
                fig_sw.add_trace(go.Scatter(
                    x=[ae_day], y=[i],
                    mode="markers",
                    marker=dict(symbol="line-ns-open", size=10, color=C_WARN, line_width=2),
                    showlegend=False,
                    hovertemplate=f"GI Adverse Event — Day {int(ae_day)}<extra></extra>"
                ))
            # discontinuation
            if dur < 300:
                fig_sw.add_trace(go.Scatter(
                    x=[dur], y=[i],
                    mode="markers",
                    marker=dict(symbol="x", size=8, color=C_ALERT, line_width=2),
                    showlegend=False,
                    hovertemplate=f"Discontinued — Day {int(dur)}<extra></extra>"
                ))
        fig_sw.update_layout(
            barmode="overlay",
            yaxis=dict(showticklabels=False, showgrid=False, title="Individual Patients (sorted by duration)"),
            xaxis=dict(title="Days from Index Date", showgrid=True, gridcolor=C_GRID),
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
            font_family="Inter, Arial",
            height=500, margin=dict(l=20,r=20,t=40,b=40),
            title=dict(text="Swimmer Plot — CagriSema Treatment Timeline (n=30 sample)", font_size=12, x=0)
        )
        st.plotly_chart(fig_sw, use_container_width=True)

    # ── TAB 9: Bump Chart ──
    with tabs[8]:
        st.markdown("<div class='section-header'>Bump Chart — GLP-1 Class Market Share Trajectory</div>",
                    unsafe_allow_html=True)
        quarters = [f"Q{q} {y}" for y in [2022,2023,2024,2025] for q in range(1,4)][:12]
        drugs = {
            "CagriSema":       [5,5,4,4,4,3,3,2,2,2,1,1],
            "Tirzepatide":     [4,4,3,3,2,2,2,1,1,1,2,2],
            "Semaglutide 2.4": [1,1,1,1,1,1,1,2,2,2,3,3],
            "Dulaglutide":     [2,2,2,2,3,4,4,4,4,4,4,4],
            "Liraglutide":     [3,3,5,5,5,5,5,5,5,5,5,5],
        }
        drug_colors = {
            "CagriSema": C_PRIMARY,
            "Tirzepatide": C_WARN,
            "Semaglutide 2.4": C_LIGHT,
            "Dulaglutide": C_GOOD,
            "Liraglutide": C_GRAY,
        }
        fig_bm = go.Figure()
        for drug, ranks in drugs.items():
            fig_bm.add_trace(go.Scatter(
                x=list(range(len(quarters))),
                y=ranks,
                mode="lines+markers",
                name=drug,
                line=dict(color=drug_colors[drug],
                           width=3 if drug == "CagriSema" else 1.5),
                marker=dict(size=8 if drug == "CagriSema" else 5,
                             color=drug_colors[drug]),
                hovertemplate=f"{drug}<br>%{{x}}: Rank %{{y}}<extra></extra>"
            ))
        fig_bm.update_layout(
            yaxis=dict(autorange="reversed", tickvals=[1,2,3,4,5],
                       ticktext=["1st","2nd","3rd","4th","5th"],
                       title="Market Share Rank",
                       showgrid=True, gridcolor=C_GRID),
            xaxis=dict(tickvals=list(range(len(quarters))), ticktext=quarters,
                       tickangle=-30, showgrid=False, title=""),
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
            font_family="Inter, Arial",
            legend=dict(orientation="h", x=0, y=-0.3),
            height=420,
            margin=dict(l=20,r=20,t=40,b=80),
            title=dict(text="GLP-1 Market Share Rank — CagriSema Ascent 2022–2025", font_size=12, x=0)
        )
        st.plotly_chart(fig_bm, use_container_width=True)

    # ── TAB 10: AI Insights ──
    with tabs[9]:
        st.markdown("<div class='section-header'>Agentic AI Insight Panel</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          Each insight below follows the four-part agentic framework:
          <strong>Observation → Implication → Recommended Action → KRA Impact.</strong>
          All insights are grounded in the current study dataset and platform knowledge base.
        </div>
        """, unsafe_allow_html=True)

        insights = [
            {
                "label": "Demographic Sub-Group Opportunity",
                "obs": "Asian patients represent 6.1% of the full CagriSema cohort but account for 11.4% of patients "
                       "in the High Efficacy / High Tolerability quadrant of the risk-benefit bubble chart. "
                       "Their PDC >80% adherence rate (71%) is the highest across all demographic groups.",
                "imp": "Asian patients appear to respond disproportionately well to CagriSema relative to their "
                       "cohort representation — consistent with published literature showing higher GLP-1 receptor "
                       "sensitivity in East Asian populations. This is a commercially underpenetrated segment with "
                       "high weight-loss drug affinity.",
                "action": "(1) Design a targeted HCP outreach campaign for endocrinologists and PCPs serving "
                           "high-density Asian communities in CA, NY, and TX. (2) Submit a subgroup analysis "
                           "proposal to medical affairs for regulatory inclusion in the label. "
                           "(3) Cross-reference SDOH broadband access data to assess telehealth expansion feasibility.",
                "kra": "Addressing this sub-group gap could increase CagriSema-treated patient enrollment by 8–12% "
                       "and strengthen the ethnic diversity evidence package required for label expansion."
            },
            {
                "label": "High-Risk Discontinuation Segment — Intervention Required",
                "obs": "Patients aged 65 and above with a pre-existing GI diagnosis (ICD-10 K21 GERD, K58 IBS) "
                       "show a predicted 6-month discontinuation probability of 34% — 75% higher than the overall "
                       "cohort rate of 19.4%. This segment represents approximately 2,800 patients in the current cohort.",
                "imp": "GI adverse events (nausea grade 2-3) in the first 8 weeks are the top SHAP-ranked predictor "
                       "of discontinuation. Losing this segment represents both a patient health risk (return to "
                       "suboptimal glycaemic control) and a revenue risk (lost persisters at the highest-payer mix age band).",
                "action": "(1) Implement a proactive pharmacist call programme at Day 14 and Day 42 post-initiation "
                           "for this sub-group. (2) Consider dose titration protocol adjustment (slower up-titration "
                           "schedule) for patients with documented GI history. (3) Flag these patients in the specialty "
                           "pharmacy system for enhanced monitoring.",
                "kra": "Reducing discontinuation in this segment from 34% to 24% would retain approximately 280 "
                       "additional patients, representing $2.4M in annual net revenue at current WAC."
            },
            {
                "label": "Western US Market Underpenetration Signal",
                "obs": "Geographic heatmap analysis shows that CA, WA, OR, and CO have high obesity prevalence "
                       "(CDC PLACES data: >35% adult obesity) but CagriSema prescribing intensity ranks in the "
                       "bottom quartile for these states relative to comparators. "
                       "Endocrinologist density is above average in all four states.",
                "imp": "A high-disease-burden, high-specialist-density market with low CagriSema prescribing "
                       "represents a structural commercial gap — not a patient population gap. This is a HCP "
                       "awareness and formulary access problem.",
                "action": "(1) Cross-reference payer intelligence module for formulary tier data in CA/WA/OR/CO "
                           "commercial plans. (2) Prioritize MSL engagement with top-50 endocrinology prescribers "
                           "in these states. (3) Investigate prior authorization denial patterns for this geography.",
                "kra": "Closing the Western US prescribing gap to market average would add an estimated 3,200 "
                       "new CagriSema patients annually — representing approximately 8.3% incremental volume growth."
            }
        ]
        for ins in insights:
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-label">{ins['label']}</div>
              <div class="insight-obs"><strong>Observation:</strong> {ins['obs']}</div>
              <br>
              <div class="insight-obs"><strong>Implication:</strong> {ins['imp']}</div>
              <br>
              <div class="insight-action"><strong>Recommended Action:</strong> {ins['action']}</div>
              <div class="insight-kra"><strong>KRA Impact:</strong> {ins['kra']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Live AI insight generation
        st.markdown("<hr class='hdivider'>", unsafe_allow_html=True)
        st.markdown("**Generate a Custom AI Insight from the Current Study Data**", unsafe_allow_html=True)
        custom_q = st.text_input("Describe the insight you want to investigate:",
                                  placeholder="e.g., What does the adherence data tell us about the Medicaid population?",
                                  key="custom_insight_q")
        if st.button("Generate Insight", key="gen_insight_btn") and custom_q.strip():
            with st.spinner("Analysing data and generating insight..."):
                prompt = (f"Study: {study_name}. "
                          f"User question: {custom_q}. "
                          "Respond using the four-part agentic framework: "
                          "Observation | Implication | Recommended Action | KRA Impact. "
                          "Be specific — cite data values from the CagriSema RWE dataset.")
                resp = call_claude([{"role":"user","content":prompt}])
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-label">AI-Generated Insight — {custom_q[:60]}...</div>
              <div class="insight-obs">{resp}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 3 — ASK ANYTHING
# ─────────────────────────────────────────────────────────────────────────────
def render_chat():
    render_topbar("Ask Anything")
    st.markdown("<div class='section-header'>Ask Anything — Pharmaceutical RWE AI Assistant</div>",
                unsafe_allow_html=True)

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">RAG Knowledge Base</div>
          <div style="font-size:0.75rem; color:{C_GRAY}; line-height:1.6; margin-top:0.3rem;">
            EHR Dataset (500k records)<br>
            Pharmacy Records (2.1M events)<br>
            Insurance Claims (8.4M lines)<br>
            CGM / Wearable Feed (892 pts)<br>
            SDOH + PRO Survey Data<br>
            FDA Guidance Documents<br>
            ADA / ACC / AHA Guidelines<br>
            Published RWE Studies (PubMed)<br>
            CMS Coverage Determinations<br>
            ISPOR / ICER HTA Guidelines
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='kpi-label' style='margin-top:1rem;'>Example Questions</div>",
                    unsafe_allow_html=True)
        examples = [
            "How many patients take weight-loss drugs in the Western US and have high cholesterol?",
            "What is the discontinuation rate for CagriSema in patients over 65 with GI comorbidities?",
            "Which payer has the highest PA denial rate in the Southeast?",
            "What does the SDOH data suggest about access barriers in rural areas?",
            "Compare CagriSema adherence vs tirzepatide across insurance types.",
        ]
        for ex in examples:
            if st.button(ex, key=f"ex_{ex[:20]}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":ex})
                with st.spinner("Analysing RWE data..."):
                    reply = call_claude(
                        [{"role":m["role"],"content":m["content"]}
                         for m in st.session_state.chat_history]
                    )
                st.session_state.chat_history.append({
                    "role":"assistant","content":reply,
                    "confidence":"High","source":"EHR + Claims dataset + RAG corpus"
                })
                st.rerun()

    with col_main:
        st.markdown(f"""
        <div class="callout">
          <strong>RAG-Grounded AI:</strong> Every response is retrieved from the uploaded RWE datasets
          and a curated pharmaceutical knowledge base before generation. A Confidence Level indicator
          and source citation accompany every response. AI hallucination risk is mitigated via
          Retrieval-Augmented Generation (RAG).
        </div>
        """, unsafe_allow_html=True)

        # Render chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-user">{msg["content"]}</div>',
                                unsafe_allow_html=True)
                else:
                    confidence = msg.get("confidence", "High")
                    source     = msg.get("source", "RWE Dataset + RAG Corpus")
                    conf_class = {"High":"conf-high","Moderate":"conf-med","Low":"conf-low"}.get(confidence,"conf-high")
                    st.markdown(f"""
                    <div class="chat-ai">
                      <span class="chat-confidence {conf_class}">Confidence: {confidence}</span>
                      {msg['content']}
                      <div class="chat-source">Source: {source}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Input bar
        st.markdown("<br>", unsafe_allow_html=True)
        chat_input = st.text_input(
            "Your question",
            placeholder="Ask anything about CagriSema RWE, the US pharma market, payer landscape, patient populations...",
            key="chat_input",
            label_visibility="collapsed"
        )
        c_send, c_clear = st.columns([4, 1])
        with c_send:
            send_btn = st.button("Send", use_container_width=True, key="send_chat")
        with c_clear:
            clear_btn = st.button("Clear", use_container_width=True, key="clear_chat")

        if clear_btn:
            st.session_state.chat_history = []
            st.rerun()

        if send_btn and chat_input.strip():
            st.session_state.chat_history.append({"role":"user","content":chat_input.strip()})
            with st.spinner("Retrieving from knowledge base and generating response..."):
                reply = call_claude(
                    [{"role":m["role"],"content":m["content"]}
                     for m in st.session_state.chat_history]
                )
            conf = "High" if any(k in reply.lower() for k in ["dataset","cohort","patients","pdc","hba1c","icd"]) else "Moderate"
            st.session_state.chat_history.append({
                "role":"assistant","content":reply,
                "confidence":conf,
                "source":"CagriSema RWE Dataset + Pharma Knowledge Base"
            })
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 4 — UPLOAD YOUR DATA
# ─────────────────────────────────────────────────────────────────────────────
def render_upload():
    render_topbar("Upload Your Data")
    st.markdown("<div class='section-header'>Upload Your Data — OMOP CDM Standardization Pipeline</div>",
                unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("""
        <div class="callout">
          Upload CSV, XLSX, JSON, Parquet, or HL7 FHIR R4 files (max 2 GB per file).
          The platform will automatically profile your data, detect coding systems,
          run the OMOP CDM v5.4 transformation pipeline, and display every SQL step
          for your review before proceeding. This is the Human-in-the-Loop (HITL) transparency mechanism.
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drag and drop your real-world data file here, or click to browse",
            type=["csv","xlsx","json","parquet"],
            key="data_uploader",
            help="Supported: CSV, XLSX, JSON, Parquet, HL7 FHIR R4"
        )

        if uploaded:
            st.session_state.upload_done = True
            st.session_state.upload_filename = uploaded.name
            st.markdown(f"""
            <div class="callout-good">
              File received: <strong>{uploaded.name}</strong> ({uploaded.size:,} bytes)<br>
              Running automated data profiling...
            </div>
            """, unsafe_allow_html=True)

            # Simulated profile
            st.markdown("<div class='section-header' style='margin-top:0.8rem;'>Data Profile Report</div>",
                        unsafe_allow_html=True)
            profile_data = {
                "Attribute": ["Total rows","Total columns","Date range detected",
                               "Missing value rate (mean)","Coding systems detected",
                               "Primary coding system","OMOP mapping readiness"],
                "Value": ["124,832","28","2020-01-01 to 2024-12-31",
                           "4.7%","ICD-10, RxNorm, NDC, LOINC",
                           "ICD-10 CM (primary diagnoses)","94.3% auto-mappable"]
            }
            st.dataframe(pd.DataFrame(profile_data), use_container_width=True, hide_index=True)
        else:
            st.info("No file uploaded yet. You can also work with the built-in demo dataset by "
                    "selecting a study type below.")

        # Study type selection
        st.markdown("<div class='section-header'>Study Type Selection — Guided Decision Tree</div>",
                    unsafe_allow_html=True)

        q1 = st.radio("Q1: Is your data already collected (retrospective) or will you collect it going forward (prospective)?",
                       ["Retrospective — data already exists","Prospective — data will be collected"], key="sq1")
        q2 = st.radio("Q2: Is your study hypothesis-driven with pre-specified endpoints, or exploratory?",
                       ["Hypothesis-driven (pre-specified endpoints)","Exploratory / hypothesis-generating"], key="sq2")
        q3 = st.radio("Q3: Does the study involve any intervention or experimental treatment assignment?",
                       ["Observational only — no intervention","Includes an intervention or pragmatic assignment"], key="sq3")

        # Decision logic
        if "Retrospective" in q1 and "Hypothesis-driven" in q2 and "Observational" in q3:
            recommended = "Retrospective Cohort Study"
            rationale   = "Your responses indicate a hypothesis-driven, non-interventional study using existing data — the classic retrospective cohort design. This is appropriate for comparative effectiveness, market analysis, and cost-of-care studies."
        elif "Prospective" in q1 and "Observational" in q3:
            recommended = "Prospective Observational Study"
            rationale   = "Forward-looking, non-interventional data collection is the hallmark of a prospective observational study. Appropriate for longitudinal safety surveillance and patient journey tracking."
        elif "Prospective" in q1 and "intervention" in q3.lower():
            recommended = "Pragmatic Clinical Trial"
            rationale   = "Prospective data collection with a pragmatic treatment assignment fits the Pragmatic Clinical Trial design — real-world clinical questions with minimal protocol constraints."
        elif "Retrospective" in q1 and "Exploratory" in q2:
            recommended = "EHR-Based Exploratory Study"
            rationale   = "Retrospective EHR data used for exploratory hypothesis generation is best framed as an EHR-Based Study, allowing flexible endpoint definition while maintaining data transparency."
        else:
            recommended = "Hybrid Study (RCT + RWD)"
            rationale   = "Your responses suggest a combination of trial and real-world data elements — a Hybrid design allowing you to supplement clinical trial endpoints with real-world outcomes data."

        st.markdown(f"""
        <div class="callout-good">
          <strong>Recommended Study Design: {recommended}</strong><br>
          {rationale}
        </div>
        """, unsafe_allow_html=True)

        study_types_df = pd.DataFrame({
            "Study Type": ["Retrospective Cohort","Prospective Observational","Pragmatic Clinical Trial",
                           "Hybrid (RCT + RWD)","Registry Study","Claims-Based Study",
                           "EHR-Based Study","Chart Review","PRO Study (Survey)",
                           "Digital / Remote Monitoring","Synthetic Control Arm"],
            "Primary Use Case": [
                "Comparative effectiveness; market analysis; cost-of-care; adherence forecasting",
                "Longitudinal safety and effectiveness; patient journey insights",
                "Real-world clinical questions with prospective enrollment",
                "Accelerated evidence; label expansion; risk-benefit refinement",
                "Long-term disease burden surveillance",
                "Large-scale epidemiology; resource utilization; treatment patterns",
                "Biomarker trajectories; comorbidity profiling; clinical variable analysis",
                "Small-N adverse event investigation; case series",
                "Quality of life; treatment satisfaction; adherence barrier identification",
                "CGM, wearable, and connected device continuous data streams",
                "Historical / simulated comparator for single-arm trial supplementation"
            ]
        })
        with st.expander("View all available study types"):
            st.dataframe(study_types_df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("<div class='section-header'>OMOP CDM Pipeline Status</div>", unsafe_allow_html=True)

        steps = [
            ("1","Source code detection","Complete","ICD-10, RxNorm, LOINC detected"),
            ("2","Vocabulary mapping","Complete","94.3% auto-mapped via Athena"),
            ("3","ETL execution","In Progress","DRUG_EXPOSURE: 87% complete"),
            ("4","Data quality report","Pending","DQD will run post-ETL"),
            ("5","SQL audit log","Active","All steps exposed for review"),
        ]
        for num, name, status, detail in steps:
            color = C_GOOD if status=="Complete" else (C_PRIMARY if status=="In Progress" else C_GRAY)
            st.markdown(f"""
            <div style="background:{C_LIGHTGRAY}; border-left:4px solid {color};
                        border-radius:0 4px 4px 0; padding:0.5rem 0.8rem;
                        margin-bottom:0.3rem;">
              <div style="font-size:0.78rem; font-weight:700; color:{color};">{num}. {name} — {status}</div>
              <div style="font-size:0.72rem; color:{C_GRAY};">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:1.2rem;'>SQL Transparency Log</div>",
                    unsafe_allow_html=True)

        sql_steps = [
            ("Step 1", "SELECT DISTINCT coding_system, COUNT(*) as n\nFROM source_data\nGROUP BY coding_system\nORDER BY n DESC;"),
            ("Step 4", "INSERT INTO omop.DRUG_EXPOSURE\n  (drug_exposure_id, person_id,\n   drug_concept_id, drug_exposure_start_date,\n   drug_source_value)\nSELECT\n  NEXTVAL('seq_drug_exp'),\n  p.person_id,\n  vc.standard_concept_id,\n  src.dispense_date,\n  src.medication_name\nFROM source_pharmacy src\nJOIN omop.PERSON p ON src.patient_id = p.person_source_value\nJOIN vocab.concept_relationship vc\n  ON src.rxnorm_code = vc.concept_code\n  AND vc.vocabulary_id = 'RxNorm'\nWHERE vc.standard_concept = 'S';"),
        ]
        for label, sql in sql_steps:
            with st.expander(f"{label} — View SQL"):
                st.markdown(f'<div class="sql-block">{sql}</div>', unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    st.button(f"Approve Step {label[-1]}", key=f"approve_{label}",
                               use_container_width=True)
                with col_b:
                    st.button(f"Edit Step {label[-1]}", key=f"edit_{label}",
                               use_container_width=True)

        # OMOP note
        st.markdown(f"""
        <div class="callout-warn" style="margin-top:0.8rem;">
          <strong>OMOP Standardization Note:</strong><br>
          Hypertension coded as ICD-10 I10 (Site A), SNOMED 38341003 (Site B),
          and free-text flag (Site C) are all mapped to OMOP Concept ID 320128
          (Essential Hypertension) — eliminating the primary source of
          information bias in multi-site RWE.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 5 — PAYER INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────
def render_payer():
    render_topbar("Payer Intelligence")
    st.markdown("<div class='section-header'>Payer Intelligence — Outcome-Based Contract Analytics</div>",
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="callout">
      <strong>Context:</strong> More than 58% of US commercial payers have at least one outcome-based
      contract (OBC) in place. This interface generates the evidence and analytical outputs required
      to engage, negotiate with, and retain pharmacy and medical benefit contracts with US payers.
      All outputs are formatted for payer medical directors and P&T committee submissions.
    </div>
    """, unsafe_allow_html=True)

    payer_tabs = st.tabs([
        "KPI Overview","Budget Impact Model","Real-World Evidence Package",
        "ADR Profile","Competitive Landscape","OBC Simulator"
    ])

    payer_df = generate_payer_data()

    # ── Payer KPIs ──
    with payer_tabs[0]:
        st.markdown("<div class='section-header'>Payer Landscape KPIs</div>", unsafe_allow_html=True)
        p1,p2,p3,p4,p5 = st.columns(5)
        for col, (val, label, sub, trend) in zip(
            [p1,p2,p3,p4,p5],
            [
                ("58%+","Payers with OBC","of US commercial payers","warn"),
                ("67.4%","PA Approval Rate","CagriSema, all payers","warn"),
                ("Tier 3","Modal Formulary Tier","most commercial plans","warn"),
                ("72%","OBC Coverage","payers with CagriSema contract","pos"),
                ("$340","Mean Patient Copay","per 28-day supply","neg"),
            ]
        ):
            cls = "kpi-pos" if trend=="pos" else ("kpi-neg" if trend=="neg" else "kpi-warn")
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value">{val}</div>
                  <div class="{cls}" style="font-size:0.72rem;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(
            payer_df.rename(columns={
                "payer":"Payer","pa_approval_rate":"PA Approval Rate",
                "formulary_tier":"Formulary Tier","step_therapy_required":"Step Therapy",
                "obc_in_place":"OBC in Place"
            }).assign(**{"PA Approval Rate": lambda x: (x["PA Approval Rate"]*100).round(1).astype(str)+"%"}),
            use_container_width=True, hide_index=True
        )

        # PA approval bar
        fig_pa = go.Figure(go.Bar(
            x=payer_df["payer"],
            y=(payer_df["pa_approval_rate"]*100).round(1),
            marker_color=[C_GOOD_LT if v > 0.70 else (C_WARN_LT if v > 0.60 else C_ALERT_LT)
                          for v in payer_df["pa_approval_rate"]],
            marker_line=dict(color="#1A1A1A", width=0.6),
            text=(payer_df["pa_approval_rate"]*100).round(1).astype(str)+"%",
            textposition="outside",
            textfont=dict(color="#1A1A1A"),
        ))
        fig_pa.add_hline(y=70, line_dash="dash", line_color=C_GOOD, line_width=1.5,
                          annotation_text="Target PA Rate: 70%", annotation_font_color="#1A1A1A")
        styled_fig(fig_pa, "Prior Authorization Approval Rate by Payer — CagriSema", 360)
        fig_pa.update_layout(
            xaxis_tickangle=-25,
            xaxis_title=dict(text="Payer", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="PA Approval Rate (%)", font=dict(color="#1A1A1A")),
            yaxis_range=[0,100],
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_pa, use_container_width=True)

        lowest_payer = payer_df.loc[payer_df["pa_approval_rate"].idxmin(), "payer"]
        highest_payer = payer_df.loc[payer_df["pa_approval_rate"].idxmax(), "payer"]
        lowest_rate = payer_df["pa_approval_rate"].min() * 100
        highest_rate = payer_df["pa_approval_rate"].max() * 100
        below_target = payer_df[payer_df["pa_approval_rate"] < 0.70]["payer"].tolist()
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Prior Authorization Approval</div>
          <div class="insight-obs">
            <strong>Observation:</strong> {highest_payer} has the highest PA approval rate ({highest_rate:.1f}%) while
            {lowest_payer} has the lowest ({lowest_rate:.1f}%). {len(below_target)} of {len(payer_df)} payers
            ({', '.join(below_target)}) fall below the 70% target approval rate.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Prioritize medical-director engagement and updated RWE submission
            packages for payers below target — starting with {lowest_payer}, where the approval gap is widest.
            Use the ADR Profile and Real-World Evidence Package tabs in this interface to build the supporting
            clinical package for resubmission.
          </div>
          <div class="insight-kra">
            KRA Impact: Closing the gap to the 70% target across under-performing payers would reduce average
            time-to-therapy-access and directly support the 72% OBC coverage growth target.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Budget Impact Model ──
    with payer_tabs[1]:
        st.markdown("<div class='section-header'>Budget Impact Model — Interactive</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          Adjust the parameters below to model the three-year net budget impact of CagriSema
          for a representative payer population. The model calculates total drug cost, avoided medical
          costs, and net budget impact. The break-even net price is highlighted. Click
          <strong>Generate Insight</strong> after adjusting parameters to refresh the AI commentary below
          the chart for your exact settings.
        </div>
        """, unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            pop_size   = st.slider("Eligible Member Population", 5000, 100000, 25000, 1000,
                                    key="bim_pop")
            uptake_y1  = st.slider("CagriSema Uptake Year 1 (%)", 5, 40, 15, 1, key="bim_y1")
            uptake_y2  = st.slider("CagriSema Uptake Year 2 (%)", 10, 60, 25, 1, key="bim_y2")
            uptake_y3  = st.slider("CagriSema Uptake Year 3 (%)", 15, 80, 38, 1, key="bim_y3")
        with b2:
            wac_monthly = st.slider("WAC per Month (USD)", 800, 2500, 1450, 50, key="bim_wac")
            rebate_pct  = st.slider("Estimated Payer Rebate (%)", 10, 50, 28, 1, key="bim_rebate")
            mace_redux  = st.slider("MACE Event Reduction (%)", 5, 30, 18, 1, key="bim_mace")
            hosp_cost   = st.slider("Avg Hospitalisation Cost Avoided (USD)", 15000, 60000, 32000, 1000, key="bim_hosp")

        net_price = wac_monthly * (1 - rebate_pct/100)
        patients  = [pop_size * r/100 for r in [uptake_y1, uptake_y2, uptake_y3]]
        drug_cost = [p * net_price * 12 for p in patients]
        mace_rate = 0.042  # annual MACE rate in untreated population
        avoided   = [p * mace_rate * mace_redux/100 * hosp_cost for p in patients]
        net_impact = [d - a for d, a in zip(drug_cost, avoided)]
        cumulative_net = np.cumsum(net_impact)
        roi_ratio = [a / d if d else 0 for a, d in zip(avoided, drug_cost)]

        bim_df = pd.DataFrame({
            "Year":               ["Year 1","Year 2","Year 3"],
            "Uptake (%)":         [uptake_y1, uptake_y2, uptake_y3],
            "Treated Patients":   [f"{int(p):,}" for p in patients],
            "Total Drug Cost ($M)": [f"${d/1e6:.2f}M" for d in drug_cost],
            "Avoided Medical Cost ($M)": [f"${a/1e6:.2f}M" for a in avoided],
            "Net Budget Impact ($M)": [f"${n/1e6:.2f}M" for n in net_impact],
            "Cumulative Net Impact ($M)": [f"${c/1e6:.2f}M" for c in cumulative_net],
            "Medical-Cost Offset Ratio": [f"{r*100:.0f}%" for r in roi_ratio],
        })
        st.dataframe(bim_df, use_container_width=True, hide_index=True)

        fig_bim = go.Figure()
        fig_bim.add_trace(go.Bar(name="Drug Cost", x=["Year 1","Year 2","Year 3"],
                                  y=[d/1e6 for d in drug_cost], marker_color=C_WARN,
                                  text=[f"${d/1e6:.1f}M" for d in drug_cost], textposition="outside",
                                  textfont=dict(color="#1A1A1A")))
        fig_bim.add_trace(go.Bar(name="Avoided Medical Cost", x=["Year 1","Year 2","Year 3"],
                                  y=[-a/1e6 for a in avoided], marker_color=C_GOOD,
                                  text=[f"${a/1e6:.1f}M" for a in avoided], textposition="outside",
                                  textfont=dict(color="#1A1A1A")))
        fig_bim.add_trace(go.Scatter(name="Net Budget Impact", x=["Year 1","Year 2","Year 3"],
                                      y=[n/1e6 for n in net_impact],
                                      mode="lines+markers+text",
                                      text=[f"${n/1e6:.1f}M" for n in net_impact],
                                      textposition="top center",
                                      textfont=dict(color="#1A1A1A"),
                                      line=dict(color=C_PRIMARY, width=2.5),
                                      marker=dict(size=8, color=C_PRIMARY)))
        fig_bim.add_trace(go.Scatter(name="Cumulative Net Impact", x=["Year 1","Year 2","Year 3"],
                                      y=[c/1e6 for c in cumulative_net],
                                      mode="lines+markers",
                                      line=dict(color=C_DARK, width=2, dash="dot"),
                                      marker=dict(size=7, symbol="diamond", color=C_DARK)))
        styled_fig(fig_bim, "Three-Year Budget Impact Model (USD Millions)", 420)
        fig_bim.update_layout(
            barmode="overlay",
            xaxis_title=dict(text="Contract Year", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="USD Millions", font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
            legend=dict(orientation="h", x=0, y=-0.2, font=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_bim, use_container_width=True)

        breakeven = net_price * (1 - sum(avoided)/sum(drug_cost))
        st.markdown(f"""
        <div class="callout-good">
          <strong>Break-Even Analysis:</strong> At the current parameter settings, CagriSema
          becomes budget-neutral for this payer population when the net price reaches
          <strong>${breakeven:.0f}/month</strong> — a {((wac_monthly-breakeven)/wac_monthly*100):.0f}%
          discount from WAC. This is the anchor figure for OBC negotiation.
        </div>
        """, unsafe_allow_html=True)

        # ── Reactive AI Insight: regenerates whenever ANY parameter changes ──
        current_params = (pop_size, uptake_y1, uptake_y2, uptake_y3, wac_monthly,
                           rebate_pct, mace_redux, hosp_cost)
        if "bim_insight_params" not in st.session_state:
            st.session_state["bim_insight_params"] = None

        gen_col1, gen_col2 = st.columns([1, 3])
        with gen_col1:
            generate_clicked = st.button("Generate Insight", key="bim_generate_btn", use_container_width=True)
        if generate_clicked:
            st.session_state["bim_insight_params"] = current_params

        # If parameters have drifted from what the cached insight was generated for,
        # show a prompt to regenerate rather than silently displaying stale commentary.
        params_changed = (st.session_state["bim_insight_params"] is not None
                           and st.session_state["bim_insight_params"] != current_params)
        with gen_col2:
            if params_changed:
                st.markdown(f"""<div style="font-size:0.74rem; color:{C_WARN}; padding-top:0.6rem;">
                Parameters changed since the last insight was generated — click <strong>Generate Insight</strong> to refresh.</div>""",
                unsafe_allow_html=True)

        if st.session_state["bim_insight_params"] is not None and not params_changed:
            p1y, p2y, p3y = patients
            cum_total = cumulative_net[-1]
            direction = "a net cost" if cum_total > 0 else "net savings"
            with st.spinner("Analysing current parameters..."):
                bim_prompt = (
                    f"Budget impact model parameters: population {pop_size:,}, uptake Y1/Y2/Y3 "
                    f"{uptake_y1}%/{uptake_y2}%/{uptake_y3}%, WAC ${wac_monthly}/month, rebate {rebate_pct}%, "
                    f"net price ${net_price:.0f}/month, MACE reduction {mace_redux}%, hospitalisation cost avoided "
                    f"${hosp_cost:,}. Year 3 treated patients: {int(p3y):,}. 3-year cumulative net budget impact: "
                    f"${cum_total/1e6:.2f}M ({direction}). Break-even price: ${breakeven:.0f}/month. "
                    f"Explain what this means for payer negotiation and budget impact."
                )
                bim_insight = call_claude([{"role": "user", "content": bim_prompt}])
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-label">AI Insight — Budget Impact Model (current parameters)</div>
              <div class="insight-obs">{bim_insight}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── RWE Evidence Package ──
    with payer_tabs[2]:
        st.markdown("<div class='section-header'>Real-World Performance Evidence Package</div>",
                    unsafe_allow_html=True)
        comparators = ["CagriSema","Tirzepatide","Sema 2.4","Dulaglutide","Liraglutide"]
        metrics = {
            "Weight Reduction (%)":   [15.3, 20.9, 12.4, 5.7,  7.2],
            "HbA1c Reduction (pp)":   [1.84, 2.1,  1.58, 0.82, 0.95],
            "PDC >80% at 12M (%)":    [58,   61,   52,   45,   41],
            "Hospitalisation Rate (%)": [4.2, 4.8,  5.1,  7.3,  8.0],
            "Discontinuation (%)":    [19.4, 22.1, 24.8, 33.2, 38.7],
        }
        ev_df = pd.DataFrame(metrics, index=comparators).T.reset_index()
        ev_df.columns = ["Metric"] + comparators
        st.dataframe(ev_df, use_container_width=True, hide_index=True)

        # Grouped bar
        fig_ev = go.Figure()
        ev_colors = [C_PRIMARY, C_WARN, C_LIGHT, C_GOOD, C_GRAY]
        metric_sel = st.selectbox("Select metric to visualise",
                                   list(metrics.keys()), key="ev_metric")
        for drug, color in zip(comparators, ev_colors):
            fig_ev.add_trace(go.Bar(
                name=drug,
                x=[metric_sel],
                y=[metrics[metric_sel][comparators.index(drug)]],
                marker_color=color,
                text=[f"{metrics[metric_sel][comparators.index(drug)]}"],
                textposition="outside",
            ))
        styled_fig(fig_ev, f"Head-to-Head Comparison — {metric_sel}", 320)
        fig_ev.update_layout(
            barmode="group", showlegend=True,
            xaxis_title=dict(text="Metric", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text=metric_sel, font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
            legend=dict(orientation="h", x=0, y=-0.25, font=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_ev, use_container_width=True)

    # ── ADR Profile ──
    with payer_tabs[3]:
        st.markdown("<div class='section-header'>Adverse Drug Reaction Profile Report</div>",
                    unsafe_allow_html=True)
        adr_data = {
            "Adverse Event Category": [
                "Nausea (any grade)","Nausea Grade 2-3","Vomiting","Diarrhoea",
                "Constipation","Injection-site reaction","Hypoglycaemia",
                "Thyroid C-cell tumour (monitoring)","Pancreatitis","MACE events"
            ],
            # Kept as plain numbers here (not mixed with text) so the table renders
            # cleanly via Arrow — the "(monitoring)"/"(class effect)" annotations live
            # in a separate Note column instead of being inlined into the numeric cells,
            # which previously caused a column dtype crash in st.dataframe.
            "CagriSema (%)": [31.2, 8.4, 6.1, 14.2, 7.8, 2.9, 2.4, 0.3, 0.18, 4.2],
            "GLP-1 Comparator (%)": [38.1, 14.2, 10.8, 18.4, 6.2, 1.8, 3.1, 0.3, 0.21, 5.8],
            "Clinical Trial Rate (%)": [33.0, 10.1, 7.2, 15.8, 8.1, 3.2, 2.8, 0.4, 0.20, 4.5],
            "Note": [
                "","","","","","","","Monitoring endpoint — not a comparative efficacy/safety rate","",""
            ],
            "Assessment": [
                "Consistent with trial","Below trial rate","Below trial rate",
                "Consistent with trial","Consistent with trial","Consistent with trial",
                "Consistent with trial","Consistent — monitor","Consistent with trial",
                "Below comparator — favorable"
            ]
        }
        adr_df = pd.DataFrame(adr_data)
        st.dataframe(adr_df, use_container_width=True, hide_index=True)

        # Detail chart — all rows are numeric now; this guard is kept defensively
        # in case a future data edit reintroduces a non-numeric monitoring-only row.
        numeric_mask = pd.to_numeric(adr_df["CagriSema (%)"], errors="coerce").notna()
        adr_num = adr_df[numeric_mask].copy()
        for c in ["CagriSema (%)", "GLP-1 Comparator (%)", "Clinical Trial Rate (%)"]:
            adr_num[c] = pd.to_numeric(adr_num[c])

        fig_adr = go.Figure()
        fig_adr.add_trace(go.Bar(name="CagriSema (RWD)", x=adr_num["Adverse Event Category"],
                                  y=adr_num["CagriSema (%)"], marker_color=C_PRIMARY))
        fig_adr.add_trace(go.Bar(name="GLP-1 Comparator (RWD)", x=adr_num["Adverse Event Category"],
                                  y=adr_num["GLP-1 Comparator (%)"], marker_color=C_LIGHT))
        fig_adr.add_trace(go.Scatter(name="Clinical Trial Rate", x=adr_num["Adverse Event Category"],
                                      y=adr_num["Clinical Trial Rate (%)"], mode="markers",
                                      marker=dict(symbol="diamond", size=10, color=C_DARK,
                                                  line=dict(color="white", width=1))))
        styled_fig(fig_adr, "Adverse Event Rate — CagriSema vs Comparator vs Clinical Trial Benchmark", 420)
        fig_adr.update_layout(
            barmode="group",
            xaxis_title=dict(text="Adverse Event Category", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="Incidence Rate (%)", font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A"), tickangle=-30),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
            legend=dict(orientation="h", x=0, y=-0.35, font=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_adr, use_container_width=True)

        st.markdown("""
        <div class="callout-good">
          <strong>OBC Implication:</strong> CagriSema's GI adverse event profile (nausea grade 2-3: 8.4% vs 14.2%
          for GLP-1 comparator) and lower discontinuation rate directly support an adherence-linked OBC.
          A contract anchoring the rebate to PDC >80% at 12 months is defensible based on the current RWE.
        </div>
        """, unsafe_allow_html=True)

        favorable = adr_num[adr_num["CagriSema (%)"] < adr_num["GLP-1 Comparator (%)"]]
        worst_event = adr_num.loc[adr_num["CagriSema (%)"].idxmax(), "Adverse Event Category"]
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — ADR Profile</div>
          <div class="insight-obs">
            <strong>Observation:</strong> CagriSema shows a lower real-world incidence than the GLP-1 comparator
            class in {len(favorable)} of {len(adr_num)} tracked adverse event categories, most notably nausea
            (any grade: 31.2% vs 38.1%) and nausea grade 2-3 (8.4% vs 14.2%). The most frequent event overall
            remains {worst_event.lower()}, consistent with the GLP-1/amylin drug class mechanism.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Lead payer and P&amp;T submissions with the nausea grade 2-3 and
            discontinuation comparison, since these are the figures most likely to influence formulary tier
            placement. Pair this profile with the Real-World Evidence Package tab for a complete efficacy + safety
            submission package.
          </div>
          <div class="insight-kra">
            KRA Impact: A favorable tolerability narrative directly supports the adherence-linked OBC structure and
            the 70%+ PA approval rate target tracked in the KPI Overview tab.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Competitive Landscape ──
    with payer_tabs[4]:
        st.markdown("<div class='section-header'>Competitive Landscape — GLP-1 Class Formulary Analysis</div>",
                    unsafe_allow_html=True)
        comp_data = {
            "Drug": ["CagriSema","Wegovy (Sema 2.4)","Zepbound (Tirz)","Trulicity (Dula)","Saxenda (Lira)"],
            "WAC/Month (USD)": [1450, 1349, 1059, 892, 1416],
            "RW Weight Reduction (%)": [15.3, 12.4, 20.9, 5.7, 7.2],
            "PDC >80% (%)": [58, 52, 61, 45, 41],
            "PA Approval Rate (%)": [67, 71, 74, 82, 78],
            "Avg Formulary Tier": [3, 2, 2, 2, 3],
            "OBC Available": ["Yes","Yes","Yes","No","No"],
            "MACE Evidence": ["Phase 3 RWE","FDA-approved","Phase 3 RWE","FDA-approved","FDA-approved"],
        }
        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="callout">
          <strong>How to use this radar chart:</strong> Pick any two drugs below to compare side-by-side across
          six formulary-relevant dimensions (each re-scaled 0–100, where <strong>further from the center is
          better</strong> on every axis — including Cost Index, where a higher score means a more
          <em>favorable</em>, lower relative cost). The dotted gridlines mark 25/50/75/100. A bigger shaded
          shape means a stronger overall competitive position; where one drug's line sits outside the other's
          on a given spoke, it is ahead on that specific dimension.
        </div>
        """, unsafe_allow_html=True)

        radar_metrics = {
            "CagriSema":            {"Weight Reduction": 88, "PDC Adherence": 85, "PA Approval": 67, "Tolerability": 82, "MACE Evidence": 70, "Cost Index": 52},
            "Wegovy (Sema 2.4)":    {"Weight Reduction": 71, "PDC Adherence": 75, "PA Approval": 71, "Tolerability": 76, "MACE Evidence": 88, "Cost Index": 57},
            "Zepbound (Tirz)":      {"Weight Reduction": 99, "PDC Adherence": 88, "PA Approval": 74, "Tolerability": 72, "MACE Evidence": 72, "Cost Index": 72},
            "Trulicity (Dula)":     {"Weight Reduction": 33, "PDC Adherence": 58, "PA Approval": 82, "Tolerability": 80, "MACE Evidence": 85, "Cost Index": 84},
            "Saxenda (Lira)":       {"Weight Reduction": 41, "PDC Adherence": 51, "PA Approval": 78, "Tolerability": 74, "MACE Evidence": 80, "Cost Index": 58},
        }
        radar_colors = {"CagriSema": C_PRIMARY, "Wegovy (Sema 2.4)": C_LIGHT, "Zepbound (Tirz)": C_WARN,
                         "Trulicity (Dula)": C_GOOD, "Saxenda (Lira)": C_GRAY}

        rc1, rc2 = st.columns(2)
        with rc1:
            drug_a = st.selectbox("Compare drug A", list(radar_metrics.keys()), index=0, key="cl_drug_a")
        with rc2:
            drug_b = st.selectbox("Compare drug B", list(radar_metrics.keys()), index=2, key="cl_drug_b")

        dims = list(radar_metrics["CagriSema"].keys())
        fig_cr = go.Figure()
        for name in [drug_a, drug_b]:
            vals = list(radar_metrics[name].values())
            color = radar_colors[name]
            fig_cr.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=dims+[dims[0]],
                fill="toself", name=name,
                fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:],16)},0.18)",
                line=dict(color=color, width=2.5),
                marker=dict(size=6, color=color),
            ))
        fig_cr.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100], showticklabels=True,
                                 tickvals=[25,50,75,100], tickfont=dict(color="#1A1A1A", size=10),
                                 gridcolor=C_GRID),
                angularaxis=dict(tickfont=dict(color="#1A1A1A", size=11)),
            ),
            paper_bgcolor=C_WHITE, font_family="Inter",
            legend=dict(orientation="h", x=0.2, y=-0.12, font=dict(color="#1A1A1A")),
            height=440, margin=dict(l=60,r=60,t=40,b=60),
            title=dict(text=f"{drug_a} vs {drug_b} — Formulary Positioning Radar (0–100, higher = better)",
                       font=dict(size=12, color=C_DARK), x=0)
        )
        st.plotly_chart(fig_cr, use_container_width=True)

        a_vals, b_vals = radar_metrics[drug_a], radar_metrics[drug_b]
        a_wins = [d for d in dims if a_vals[d] > b_vals[d]]
        b_wins = [d for d in dims if b_vals[d] > a_vals[d]]
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Competitive Positioning</div>
          <div class="insight-obs">
            <strong>Observation:</strong> {drug_a} leads on {', '.join(a_wins) if a_wins else 'no dimensions'};
            {drug_b} leads on {', '.join(b_wins) if b_wins else 'no dimensions'}. The widest gap is on
            "{max(dims, key=lambda d: abs(a_vals[d]-b_vals[d]))}", where the two drugs differ most.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Lead payer conversations with {drug_a}'s strongest dimension(s)
            above and proactively address the dimension(s) where {drug_b} currently leads, using the ADR Profile
            and Real-World Evidence Package tabs in this interface to support the counter-narrative.
          </div>
          <div class="insight-kra">
            KRA Impact: A clear, dimension-by-dimension competitive narrative directly supports P&amp;T committee
            submissions and OBC negotiation positioning.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── OBC Simulator ──
    with payer_tabs[5]:
        st.markdown("<div class='section-header'>Outcome-Based Contract Simulator</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          Configure OBC contract terms and the simulator models financial outcomes for both
          payer and manufacturer under three scenarios, using Monte Carlo simulation (1,000 iterations).
        </div>
        """, unsafe_allow_html=True)

        oc1, oc2 = st.columns(2)
        with oc1:
            perf_threshold = st.slider("Performance Threshold — Mean Weight Reduction (%)",
                                        8.0, 18.0, 12.0, 0.5, key="obc_thresh")
            rebate_no_obc  = st.slider("Rebate: No OBC (%)", 15, 35, 22, 1, key="obc_r0")
            rebate_mod_obc = st.slider("Rebate: Moderate OBC (%)", 25, 50, 32, 1, key="obc_r1")
            rebate_agg_obc = st.slider("Rebate: Aggressive OBC (%)", 35, 65, 45, 1, key="obc_r2")
        with oc2:
            reconcile = st.selectbox("Reconciliation Timing", ["Annual","Semi-Annual"], key="obc_rec")
            measure   = st.selectbox("Measurement Methodology",
                                      ["Claims-derived PDC","EHR lab values (HbA1c)","Blended"], key="obc_meth")
            patients_obc = st.number_input("Contracted Patient Population", 1000, 50000, 8500, key="obc_pts")

        wac_obc = 1450  # fixed
        base_costs = {
            "No OBC":         wac_obc * (1 - rebate_no_obc/100) * patients_obc * 12 / 1e6,
            "Moderate OBC":   wac_obc * (1 - rebate_mod_obc/100) * patients_obc * 12 / 1e6,
            "Aggressive OBC": wac_obc * (1 - rebate_agg_obc/100) * patients_obc * 12 / 1e6,
        }

        # Monte Carlo
        np.random.seed(77)
        n_mc = 1000
        mc_results = {}
        for scenario, base_cost in base_costs.items():
            performance_outcomes = np.random.normal(15.3, 3.8, n_mc)
            # If performance misses threshold, payer gets additional rebate
            rebate_multiplier = np.where(performance_outcomes < perf_threshold, 1.08, 1.0)
            mc_costs = base_cost * rebate_multiplier
            mc_results[scenario] = mc_costs

        fig_mc = go.Figure()
        mc_colors = [C_ALERT, C_WARN, C_GOOD]
        for (scen, mc_vals), color in zip(mc_results.items(), mc_colors):
            fig_mc.add_trace(go.Violin(
                y=mc_vals, name=scen,
                fillcolor=color,
                box_visible=True,
                meanline_visible=True,
                line_color=C_DARK,
                opacity=0.7,
                points="outliers",
            ))
        styled_fig(fig_mc, f"OBC Monte Carlo Simulation — Annual Net Cost to Payer ($M, n=1,000 iterations)", 420)
        fig_mc.update_layout(
            xaxis_title=dict(text="Contract Scenario", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="Annual Net Drug Cost ($M)", font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
            showlegend=True,
            legend=dict(font=dict(color="#1A1A1A")),
            violinmode="group"
        )
        st.plotly_chart(fig_mc, use_container_width=True)

        obc_table = pd.DataFrame({
            "Scenario": list(base_costs.keys()),
            "Base Net Price/Month": [f"${wac_obc*(1-r/100):.0f}" for r in [rebate_no_obc, rebate_mod_obc, rebate_agg_obc]],
            "Annual Cost ($M, mean)": [f"${v:.2f}M" for v in base_costs.values()],
            "P10 Cost ($M)":  [f"${np.percentile(v,10):.2f}M" for v in mc_results.values()],
            "P90 Cost ($M)":  [f"${np.percentile(v,90):.2f}M" for v in mc_results.values()],
            "Rebate Trigger": ["None", f"Weight reduction < {perf_threshold}%", f"Weight reduction < {perf_threshold}%"],
        })
        st.dataframe(obc_table, use_container_width=True, hide_index=True)

        # Manufacturer-side revenue view, for the same three scenarios — gives the full
        # two-sided picture the original chart was missing (payer cost only).
        mfr_revenue = {scen: patients_obc * wac_obc * (1 - r/100) * 12 / 1e6
                       for scen, r in zip(base_costs.keys(), [rebate_no_obc, rebate_mod_obc, rebate_agg_obc])}
        fig_mfr = go.Figure(go.Bar(
            x=list(mfr_revenue.keys()), y=list(mfr_revenue.values()),
            marker_color=[C_ALERT_LT, C_WARN_LT, C_GOOD_LT],
            marker_line=dict(color="#1A1A1A", width=0.6),
            text=[f"${v:.1f}M" for v in mfr_revenue.values()], textposition="outside",
            textfont=dict(color="#1A1A1A"),
        ))
        styled_fig(fig_mfr, "Manufacturer Net Revenue by OBC Scenario ($M, mean case)", 320)
        fig_mfr.update_layout(
            xaxis_title=dict(text="Contract Scenario", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="Annual Net Revenue ($M)", font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_mfr, use_container_width=True)

        best_payer_scenario = min(base_costs, key=base_costs.get)
        spread_pct = (max(base_costs.values()) - min(base_costs.values())) / max(base_costs.values()) * 100
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — OBC Simulator</div>
          <div class="insight-obs">
            <strong>Observation:</strong> At the current settings, {best_payer_scenario} offers the lowest mean
            annual cost to the payer (${base_costs[best_payer_scenario]:.2f}M), a {spread_pct:.0f}% spread versus
            the highest-cost scenario. With the performance threshold set at {perf_threshold:.1f}% mean weight
            reduction, roughly {(np.random.normal(15.3,3.8,1000) < perf_threshold).mean()*100:.0f}% of simulated
            patient cohorts would miss the bar and trigger the additional rebate under Moderate/Aggressive OBC terms.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> If the manufacturer's revenue tolerance under {best_payer_scenario}
            is acceptable (see manufacturer revenue chart above), this is the strongest opening position for payer
            negotiation. Pair the {measure} measurement methodology with {reconcile.lower()} reconciliation to limit
            administrative burden while preserving the performance link.
          </div>
          <div class="insight-kra">
            KRA Impact: Locking in an OBC at or above {best_payer_scenario.lower()} terms directly supports the 72%
            OBC-coverage target tracked in the KPI Overview tab.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE 6 — SIGNAL LAB
# ─────────────────────────────────────────────────────────────────────────────
def render_signal_lab():
    render_topbar("Signal Lab")
    st.markdown("<div class='section-header'>Signal Lab — Advanced AI Workbench</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="callout">
      Signal Lab houses the platform's most advanced analytical capabilities:
      Indication Expansion, Causal Inference (DML/TMLE), Federated Learning,
      Continuous CGM Data Feed, and Predictive Analytics. Each module represents
      a frontier capability not yet standard in commercial RWE platforms.
    </div>
    """, unsafe_allow_html=True)

    sl_tabs = st.tabs([
        "Indication Expansion","Causal Inference (DML/TMLE)",
        "Federated Learning","CGM Data Feed","Predictive Analytics","Custom Chart Generator"
    ])

    # ── TAB A: Indication Expansion ──
    with sl_tabs[0]:
        st.markdown("<div class='section-header'>Indication Expansion Analysis — Off-Label Signal Detection</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          The AI scans the uploaded RWD for signals that CagriSema may be effective beyond its
          current approved indication (obesity + T2DM). Signals are organized into the
          Pre-Clinical → Phase 3 Support → Post-Clinical framework.
        </div>
        """, unsafe_allow_html=True)

        signals = [
            {
                "stage": "Pre-Clinical Signal",
                "indication": "Non-Alcoholic Steatohepatitis (NASH / MAFLD)",
                "icd": "K75.81",
                "effect_size": "ALT reduction of 38% in CagriSema-treated patients vs 14% in comparator arm",
                "p_value": "p = 0.0018",
                "mechanism": "Amylin's hepatic lipid metabolism effect + GLP-1 reduction of hepatic steatosis",
                "sample": "n = 1,240 patients with documented NASH diagnosis in EHR",
                "stage_color": C_WARN,
                "recommendation": "Flag for scientific affairs review. Submit pre-IND meeting request to FDA. Cross-reference NASH RWE literature.",
            },
            {
                "stage": "Pre-Clinical Signal",
                "indication": "Polycystic Ovary Syndrome (PCOS) + Metabolic Syndrome",
                "icd": "E28.2 + E88.81",
                "effect_size": "Free testosterone reduction 22%; menstrual regularity improvement in 61% of PCOS patients",
                "p_value": "p = 0.031",
                "mechanism": "GLP-1-mediated insulin resistance reduction; weight loss-driven androgen normalization",
                "sample": "n = 892 female patients aged 18-45 with PCOS + obesity co-diagnosis",
                "stage_color": C_WARN,
                "recommendation": "Design prospective sub-study within existing WEIGHT-FORWARD observational cohort.",
            },
            {
                "stage": "Phase 3 Clinical Support",
                "indication": "Obesity-Related Heart Failure with Preserved Ejection Fraction (HFpEF)",
                "icd": "I50.3 + E66",
                "effect_size": "NT-proBNP reduction 31% at 12M; 6-minute walk test improvement 48m vs 12m comparator",
                "p_value": "p < 0.001",
                "mechanism": "Weight loss + reduced cardiac pre-load; GLP-1 direct myocardial effect (SGLT2i-additive signal)",
                "sample": "n = 3,480 patients with HFpEF + obesity; RWD signal strength sufficient for Phase 3 design",
                "stage_color": C_PRIMARY,
                "recommendation": "Generate Phase 3 trial synopsis. Identify optimal cohort via Cohort Builder (Interface 1). Map to FDA guidance on HFpEF endpoints.",
            },
        ]

        for sig in signals:
            with st.expander(f"[{sig['stage']}] {sig['indication']} — ICD-10: {sig['icd']}"):
                a1, a2 = st.columns([3,1])
                with a1:
                    st.markdown(f"""
                    <div style="font-size:0.82rem; line-height:1.7;">
                      <strong>Effect Size:</strong> {sig['effect_size']}<br>
                      <strong>Statistical Significance:</strong> {sig['p_value']}<br>
                      <strong>Biological Mechanism:</strong> {sig['mechanism']}<br>
                      <strong>Sample:</strong> {sig['sample']}<br>
                      <strong>Recommended Action:</strong> {sig['recommendation']}
                    </div>
                    """, unsafe_allow_html=True)
                with a2:
                    st.markdown(f"""
                    <div style="background:{sig['stage_color']}; color:white;
                                border-radius:6px; padding:0.8rem; text-align:center;
                                font-size:0.75rem; font-weight:700; line-height:1.5;">
                      {sig['stage']}<br>
                      <span style="font-size:1.3rem;">{sig['p_value'].split('=')[1].strip() if '=' in sig['p_value'] else sig['p_value']}</span>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:1rem;'>Development Stage Framework</div>",
                    unsafe_allow_html=True)
        stage_df = pd.DataFrame({
            "Stage": ["Pre-Clinical Signal","Phase 3 Clinical Support","Post-Clinical Confirmation"],
            "Criteria": [
                "p<0.05 statistical association in RWD + biologically plausible mechanism",
                "Effect size >10%, adequate sample, covariate-adjusted — sufficient for Phase 3 design",
                "RWD confirms trial efficacy in broader unselected real-world population"
            ],
            "Action": [
                "Flag for scientific affairs. Cross-reference mechanism literature.",
                "Generate study synopsis. Map to FDA guidance. Engage clinical team.",
                "Prepare FDA label supplement (21 CFR 314.70). Brief payer team on OBC opportunity."
            ]
        })
        st.dataframe(stage_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Indication Expansion</div>
          <div class="insight-obs">
            <strong>Observation:</strong> The HFpEF signal (NT-proBNP reduction 31% at 12M, p&lt;0.001, n=3,480) is
            the most mature of the three detected signals — it already meets Phase 3 Clinical Support criteria
            (effect size &gt;10%, adequate sample, covariate-adjusted). The NASH and PCOS signals remain
            pre-clinical (p&lt;0.05 but smaller samples, n=1,240 and n=892 respectively).
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Prioritize the HFpEF signal for Phase 3 trial synopsis
            development and FDA guidance mapping now. Route the NASH and PCOS signals to scientific affairs for
            mechanism-literature review and consider designing prospective sub-studies within the existing
            WEIGHT-FORWARD observational cohort to mature them faster.
          </div>
          <div class="insight-kra">
            KRA Impact: Advancing the HFpEF signal to Phase 3 design could open a second indication and
            materially expand the addressable patient population beyond the current obesity + T2DM label.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB B: Causal Inference ──
    with sl_tabs[1]:
        st.markdown("<div class='section-header'>Causal Inference Engine — Double Machine Learning and TMLE</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout-warn">
          <strong>Confounding by Indication Alert:</strong> CagriSema is more likely to be prescribed
          to patients at higher metabolic risk. This would make the drug appear less effective than it
          truly is if not statistically adjusted. The panel below shows the pre-adjustment vs
          post-adjustment treatment effect estimate.
        </div>
        """, unsafe_allow_html=True)

        ci1, ci2 = st.columns(2)
        with ci1:
            st.markdown("""
            <div class="kpi-card">
              <div class="kpi-label">Unadjusted Treatment Effect (Naive)</div>
              <div class="kpi-value" style="font-size:1.5rem;">-12.1%</div>
              <div class="kpi-sub">Weight reduction — raw comparison</div>
              <div class="kpi-warn">Confounding by indication present — underestimate</div>
            </div>
            """, unsafe_allow_html=True)
        with ci2:
            st.markdown("""
            <div class="kpi-card">
              <div class="kpi-label">DML/TMLE Adjusted ATE</div>
              <div class="kpi-value" style="font-size:1.5rem; color:#1A7C4F;">-15.3%</div>
              <div class="kpi-sub">Average Treatment Effect (doubly robust)</div>
              <div class="kpi-pos">95% CI: -14.1% to -16.5%  |  Bias correction: +3.2 pp</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='section-header' style='margin-top:1rem;'>SHAP Feature Importance — DML Model</div>",
                    unsafe_allow_html=True)

        features = ["GI History (K21/K58)","Age (65+)","BMI Baseline","HbA1c Baseline",
                    "eGFR","Prior GLP-1 Use","Insurance: Medicaid","SDOH ADI Score",
                    "Specialist Distance","Race: Asian","Sex: Female","Comorbidity Index"]
        shap_vals = [0.41, 0.38, 0.29, 0.26, 0.22, 0.19, 0.17, 0.15, 0.13, -0.11, -0.08, 0.12]
        shap_colors = [C_ALERT if v > 0 else C_GOOD for v in shap_vals]
        shap_sorted = sorted(zip(features, shap_vals, shap_colors), key=lambda x: abs(x[1]), reverse=True)
        f_s, v_s, c_s = zip(*shap_sorted)

        fig_shap = go.Figure(go.Bar(
            x=list(v_s), y=list(f_s),
            orientation="h",
            marker_color=list(c_s),
            marker_line_width=0,
            hovertemplate="%{y}: SHAP = %{x:.3f}<extra></extra>"
        ))
        fig_shap.add_vline(x=0, line_color=C_BORDER, line_width=1)
        styled_fig(fig_shap, "SHAP Values — Predictors of CagriSema Discontinuation (DML Model)", 420)
        fig_shap.update_layout(
            yaxis=dict(autorange="reversed", tickfont=dict(color="#1A1A1A")),
            xaxis_title=dict(text="SHAP Value (positive = increases discontinuation risk)", font=dict(color="#1A1A1A")),
            xaxis=dict(tickfont=dict(color="#1A1A1A")),
        )
        st.plotly_chart(fig_shap, use_container_width=True)

        st.markdown("""
        <div class="callout">
          <strong>DML Methodology:</strong> Stage 1 — XGBoost predicts (a) probability of CagriSema
          prescription (propensity model) and (b) expected outcome under no treatment (outcome model).
          Stage 2 — the residuals from both models are used to estimate the causal ATE,
          removing the influence of all observed confounders. The result is a doubly-robust estimate:
          consistent even if one of the two Stage 1 models is misspecified.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Causal Inference</div>
          <div class="insight-obs">
            <strong>Observation:</strong> The naive (unadjusted) treatment effect of -12.1% understates CagriSema's
            true causal effect by 3.2 percentage points versus the doubly-robust DML/TMLE estimate of -15.3% —
            confounding by indication was masking part of the drug's real benefit. GI history (K21/K58) and age
            65+ are the two strongest SHAP-ranked predictors of discontinuation, both increasing risk.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Use the adjusted -15.3% ATE, not the naive -12.1% figure, in any
            payer or KOL-facing materials. Target proactive GI-symptom management protocols at patients flagged
            by the top two SHAP features, since they account for the largest share of preventable discontinuation.
          </div>
          <div class="insight-kra">
            KRA Impact: Presenting the bias-corrected effect size strengthens the clinical evidence package, while
            targeting the top SHAP-ranked risk factors directly supports the discontinuation-reduction KRA.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB C: Federated Learning ──
    with sl_tabs[2]:
        st.markdown("<div class='section-header'>Federated Learning Network — Multi-Site Model Training</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout">
          Model training occurs locally at each hospital node. Only model weights (mathematical
          gradient updates) travel between sites — raw patient data never leaves the originating
          institution. This eliminates the need for Data Use Agreements for raw data transfer.
        </div>
        """, unsafe_allow_html=True)

        fn1, fn2, fn3, fn4 = st.columns(4)
        nodes = [
            (fn1, "Mayo Clinic", "Rochester, MN", 4200, "Training", C_PRIMARY, "Round 7 of 10"),
            (fn2, "Cleveland Clinic", "Cleveland, OH", 3850, "Weights Transmitted", C_GOOD, "Round 7 complete"),
            (fn3, "Johns Hopkins", "Baltimore, MD", 3600, "Training", C_PRIMARY, "Round 7 of 10"),
            (fn4, "UCSF Medical Center", "San Francisco, CA", 3350, "Awaiting Aggregation", C_WARN, "Idle"),
        ]
        for col, name, loc, pts, status, color, detail in nodes:
            dot = "status-dot-green" if color==C_GOOD else ("status-dot-amber" if color==C_WARN else "status-dot-blue")
            with col:
                st.markdown(f"""
                <div class="fed-node">
                  <div class="fed-node-name">{name}</div>
                  <div style="font-size:0.7rem; color:{C_GRAY};">{loc}</div>
                  <div class="fed-node-pts">{pts:,}</div>
                  <div style="font-size:0.7rem; color:{C_GRAY};">patients</div>
                  <div class="fed-node-stat">
                    <span class="{dot}"></span>{status}
                  </div>
                  <div style="font-size:0.68rem; color:{C_GRAY};">{detail}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Training progress
        round_num = st.session_state.fed_round
        st.markdown(f"**Federated Training Progress — Round {round_num} of 10**")
        st.progress(round_num / 10)
        col_prog1, col_prog2 = st.columns(2)
        with col_prog1:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">Global Model AUC</div>
              <div class="kpi-value">0.847</div>
              <div class="kpi-sub">Discontinuation prediction</div>
              <div class="kpi-pos">+0.034 improvement from Round 1</div>
            </div>
            """, unsafe_allow_html=True)
        with col_prog2:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-label">Global Model F1 Score</div>
              <div class="kpi-value">0.781</div>
              <div class="kpi-sub">Combined 15,000 patient cohort</div>
              <div class="kpi-pos">+0.028 improvement from Round 1</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Advance Training Round", key="fed_advance"):
            if st.session_state.fed_round < 10:
                st.session_state.fed_round += 1
            else:
                st.session_state.fed_round = 1
            st.rerun()

        # AUC improvement curve
        rounds = list(range(1, round_num+1))
        auc_curve = [0.721 + i * 0.0139 for i in range(round_num)]
        fig_fl = go.Figure()
        fig_fl.add_trace(go.Scatter(x=rounds, y=auc_curve, mode="lines+markers",
                                     line=dict(color=C_PRIMARY, width=2.5),
                                     marker=dict(size=8, color=C_PRIMARY),
                                     name="Global Model AUC"))
        fig_fl.add_hline(y=0.85, line_dash="dash", line_color=C_GOOD, line_width=1.5,
                          annotation_text="Target AUC: 0.85")
        styled_fig(fig_fl, "Federated Learning — Global Model AUC by Training Round", 320)
        fig_fl.update_layout(
            xaxis_title=dict(text="Training Round", font=dict(color="#1A1A1A")),
            yaxis_title=dict(text="AUC", font=dict(color="#1A1A1A")),
            xaxis=dict(tickvals=list(range(1, 11)), tickfont=dict(color="#1A1A1A")),
            yaxis=dict(tickfont=dict(color="#1A1A1A")),
            yaxis_range=[0.70, 0.92])
        st.plotly_chart(fig_fl, use_container_width=True)

        rounds_to_target = max(0, int(np.ceil((0.85 - auc_curve[-1]) / 0.0139))) if auc_curve[-1] < 0.85 else 0
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Federated Learning</div>
          <div class="insight-obs">
            <strong>Observation:</strong> The global model has reached AUC {auc_curve[-1]:.3f} after round
            {round_num} of 10, a gain of {auc_curve[-1]-auc_curve[0]:.3f} since round 1.
            {"It has already passed the 0.85 target." if auc_curve[-1] >= 0.85 else f"At the current improvement rate, it is projected to reach the 0.85 target AUC in approximately {rounds_to_target} more round(s)."}
            UCSF Medical Center is currently idle awaiting aggregation while the other three nodes continue training.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Trigger aggregation for UCSF's pending round to avoid bottlenecking
            the global update, and continue training through round 10 to lock in the AUC gain before deploying the
            discontinuation-prediction model into the Cohort Builder and Predictive Analytics modules.
          </div>
          <div class="insight-kra">
            KRA Impact: A validated AUC ≥0.85 discontinuation model can be operationalized directly into the
            patient-support targeting workflow referenced in the Causal Inference and Predictive Analytics tabs.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB D: CGM Feed ──
    with sl_tabs[3]:
        st.markdown("<div class='section-header'>Continuous CGM and Wearable Data Feed</div>",
                    unsafe_allow_html=True)
        wear_df = generate_wearable_data()

        wm1,wm2,wm3,wm4 = st.columns(4)
        for col, (val, label, sub, trend) in zip(
            [wm1,wm2,wm3,wm4],
            [
                ("68.3%","Time-in-Range (70-180)","Up 11.2 pp from baseline","pos"),
                ("28.4%","Glucose CV% (Variability)","Down 22% from baseline","pos"),
                ("87.3%","Injection Adherence","App-confirmed doses","pos"),
                ("1.6 / 10","GI Symptom Score","Week 12 — improved from 2.8","pos"),
            ]
        ):
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                  <div class="kpi-label">{label}</div>
                  <div class="kpi-value">{val}</div>
                  <div class="kpi-pos" style="font-size:0.72rem;">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        fig_cgm = make_subplots(rows=2, cols=2,
                                 subplot_titles=["Time-in-Range (%) by Week",
                                                  "Glucose Variability CV% by Week",
                                                  "Mean Body Weight (kg) by Week",
                                                  "GI Symptom Score (0-10) by Week"],
                                 vertical_spacing=0.18, horizontal_spacing=0.1)
        w = wear_df["week"]
        fig_cgm.add_trace(go.Scatter(x=w, y=wear_df["tir_pct"],
                                      line=dict(color=C_PRIMARY, width=2.5),
                                      mode="lines+markers", showlegend=False), row=1, col=1)
        fig_cgm.add_trace(go.Scatter(x=w, y=wear_df["cv_pct"],
                                      line=dict(color=C_WARN, width=2.5),
                                      mode="lines+markers", showlegend=False), row=1, col=2)
        fig_cgm.add_trace(go.Scatter(x=w, y=wear_df["weight_kg"],
                                      line=dict(color=C_GOOD, width=2.5),
                                      mode="lines+markers", showlegend=False), row=2, col=1)
        fig_cgm.add_trace(go.Scatter(x=w, y=wear_df["gi_score"],
                                      line=dict(color=C_ALERT, width=2.5),
                                      mode="lines+markers", showlegend=False), row=2, col=2)
        fig_cgm.add_hline(y=70, row=1, col=1, line_dash="dash", line_color=C_GOOD,
                           annotation_text="Target >70%")
        fig_cgm.add_hline(y=36, row=1, col=2, line_dash="dash", line_color=C_ALERT,
                           annotation_text="Max CV% 36 (ATTD)")
        fig_cgm.update_layout(
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
            font_family="Inter, Arial", height=520,
            margin=dict(l=20, r=20, t=60, b=20),
            title=dict(text="CGM + Wearable Data Feed — 892 Enrolled Patients (Rolling 12-Week)", font_size=12)
        )
        for i in range(1,3):
            for j in range(1,3):
                fig_cgm.update_xaxes(showgrid=True, gridcolor=C_GRID, row=i, col=j)
                fig_cgm.update_yaxes(showgrid=True, gridcolor=C_GRID, row=i, col=j)
        st.plotly_chart(fig_cgm, use_container_width=True)

        st.markdown(f"""
        <div class="callout-good">
          <strong>Key Finding:</strong> GI symptom score declined from 2.8 at Week 4 to 1.6 at Week 12,
          confirming that early GI intolerance resolves for most patients — consistent with the
          tolerability hypothesis. This data supports the payer OBC claim that 12-month adherence
          will exceed the comparator class rate. Glucose time-in-range is tracking toward the
          70% ATTD consensus target (currently 68.3%, up 11.2 pp from baseline).
        </div>
        """, unsafe_allow_html=True)

        tir_trend = wear_df["tir_pct"].iloc[-1] - wear_df["tir_pct"].iloc[0]
        gi_trend = wear_df["gi_score"].iloc[0] - wear_df["gi_score"].iloc[-1]
        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — CGM / Wearable Data Feed</div>
          <div class="insight-obs">
            <strong>Observation:</strong> Across the 12-week rolling window, time-in-range improved by
            {tir_trend:.1f} percentage points and GI symptom score fell by {gi_trend:.1f} points, while glucose
            variability (CV%) trended down — three independent signals moving in the favorable direction
            simultaneously across {len(wear_df)} weekly cohorts of the 892 enrolled patients.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Use the Week 8-12 GI symptom resolution curve as direct evidence
            in patient counseling materials and specialty-pharmacy onboarding scripts — early nausea is the
            top discontinuation driver, and this data shows it is time-limited rather than persistent.
          </div>
          <div class="insight-kra">
            KRA Impact: Sustaining the time-in-range trajectory toward the 70% ATTD target strengthens the
            CGM-based RWE package supporting both the OBC negotiation and the Signal Lab predictive
            adherence model.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB E: Predictive Analytics ──
    with sl_tabs[4]:
        st.markdown("<div class='section-header'>Predictive Analytics — 12-Month XGBoost Forecast</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="callout-warn">
          All outputs below are model estimates — not certain outcomes. Confidence intervals reflect
          the XGBoost model's uncertainty range across 500 bootstrap iterations. These projections
          are intended to inform commercial and medical strategy, not to replace clinical judgment.
        </div>
        """, unsafe_allow_html=True)

        pred_data = {
            "Predictive Output": [
                "CagriSema Market Share at 12M","Predicted Adherence Rate (PDC>80%)",
                "High-Risk Discontinuation Probability","Top Discontinuation Driver",
                "Predicted MACE Event Reduction","New-to-Brand Patients Year 1"
            ],
            "Current Value": ["12.3%","41% (GLP-1 class avg)","34% (age 65+, GI history)",
                               "GI AE (nausea grade 2-3)","—","—"],
            "12-Month Prediction": ["18% – 24%","58% (CagriSema)","34% if unaddressed",
                                     "SHAP rank 1 of 14 features","18% RRR (CI: 11%–24%)","42,000–58,000 new patients"],
            "Model Confidence": ["High","High","High","High","Moderate","Moderate"],
        }
        st.dataframe(pd.DataFrame(pred_data), use_container_width=True, hide_index=True)

        # Market share forecast
        np.random.seed(88)
        months = list(range(0, 13))
        ms_mean  = [12.3 + m * 0.98 + np.random.normal(0, 0.3) for m in months]
        ms_lo    = [v - 2.1 for v in ms_mean]
        ms_hi    = [v + 2.3 for v in ms_mean]
        adh_mean = [41 + m * 1.42 + np.random.normal(0, 0.5) for m in months]

        fig_pred = make_subplots(rows=1, cols=2,
                                  subplot_titles=["CagriSema Market Share Forecast (%)",
                                                   "Predicted Adherence Rate Trajectory (%)"])
        fig_pred.add_trace(go.Scatter(
            x=months+months[::-1], y=ms_hi+ms_lo[::-1],
            fill="toself", fillcolor="rgba(17,113,185,0.1)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False
        ), row=1, col=1)
        fig_pred.add_trace(go.Scatter(x=months, y=ms_mean,
                                       line=dict(color=C_PRIMARY, width=2.5), mode="lines",
                                       name="Market Share"), row=1, col=1)
        fig_pred.add_trace(go.Scatter(x=months, y=adh_mean,
                                       line=dict(color=C_GOOD, width=2.5), mode="lines+markers",
                                       name="Adherence Rate"), row=1, col=2)
        fig_pred.add_hline(y=58, row=1, col=2, line_dash="dash", line_color=C_GOOD, line_width=1,
                            annotation_text="Predicted 12M target: 58%")
        fig_pred.update_layout(
            paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE, font_family="Inter",
            height=360, margin=dict(l=20,r=20,t=60,b=20),
            legend=dict(font=dict(color="#1A1A1A")),
        )
        for j in [1,2]:
            fig_pred.update_xaxes(title_text="Month", title_font=dict(color="#1A1A1A"),
                                   tickfont=dict(color="#1A1A1A"), showgrid=True, gridcolor=C_GRID, row=1, col=j)
            fig_pred.update_yaxes(tickfont=dict(color="#1A1A1A"), showgrid=True, gridcolor=C_GRID, row=1, col=j)
        st.plotly_chart(fig_pred, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
          <div class="insight-label">AI Insight — Predictive Analytics</div>
          <div class="insight-obs">
            <strong>Observation:</strong> The model projects CagriSema market share climbing from 12.3% to the
            18-24% range within 12 months, while predicted adherence rises from 41% to 58% — both High-confidence
            projections. The 34% high-risk discontinuation probability for the age-65+/GI-history segment remains
            the single largest threat to the adherence forecast if left unaddressed.
          </div>
          <div class="insight-action">
            <strong>Recommended Action:</strong> Stand up the proactive GI-history monitoring programme referenced
            in Causal Inference and Your Projects AI Insights now, before the next forecast window, since the
            top discontinuation driver (GI AE) is addressable with a Day 14/Day 42 outreach protocol.
          </div>
          <div class="insight-kra">
            KRA Impact: Hitting the 58% adherence prediction would close most of the gap to CagriSema's
            12-month persistence target and materially de-risk the 42,000-58,000 new-patient Year 1 forecast.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB F: Custom Chart Generator ──
    with sl_tabs[5]:
        st.markdown("<div class='section-header'>Custom Visual Output Generator (Veradigm-Inspired)</div>",
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="callout">
          Describe the visualization you need in plain English. The AI selects the appropriate chart type,
          queries the underlying OMOP-standardized dataset, and generates the chart.
          Use cases: medical affairs KOL decks, payer P&T submissions, sales territory reports,
          marketing HCP materials — all from the same underlying data.
        </div>
        """, unsafe_allow_html=True)

        chart_input = st.text_area(
            "Describe the visualization you need:",
            placeholder="Examples:\n"
                        "• Show me a comparison of HbA1c reduction by insurance type for female patients under 60\n"
                        "• Create a chart showing adherence rates by race and age group\n"
                        "• Plot the geographic distribution of CagriSema prescriptions by state\n"
                        "• Show discontinuation rates over time segmented by prior GI history",
            height=100,
            key="custom_chart_input"
        )

        col_gen, col_team = st.columns([2, 1])
        with col_team:
            target_team = st.selectbox("Target Team / Audience",
                                        ["Medical Affairs","Commercial / Marketing","Payer / Market Access",
                                         "Sales","Regulatory Affairs","Executive Leadership"],
                                        key="chart_team")
        with col_gen:
            gen_chart_btn = st.button("Generate Chart", use_container_width=True, key="gen_chart_btn")

        # Display previous custom charts
        for prev in st.session_state.custom_chart_history:
            st.markdown(f"""
            <div style="background:{C_LIGHTGRAY}; border-radius:6px; padding:0.5rem 0.8rem;
                        margin-bottom:0.3rem; font-size:0.78rem; color:{C_GRAY};">
              <strong>Previous:</strong> {prev}
            </div>
            """, unsafe_allow_html=True)

        if gen_chart_btn and chart_input.strip():
            st.session_state.custom_chart_history.append(chart_input.strip())
            df = generate_ehr_data()

            # AI determines chart type and generates SQL + reasoning
            with st.spinner("Analysing request, selecting chart type, and generating visualization..."):
                ai_chart_prompt = (
                    f"Target team: {target_team}. "
                    f"Visualization request: {chart_input.strip()}. "
                    "Respond with:\n"
                    "1. Recommended chart type and why\n"
                    "2. Key data insight this chart will reveal\n"
                    "3. A sample SQL query (using OMOP CDM table names) that would produce this data\n"
                    "4. One alternative chart type suggestion if applicable\n"
                    "Keep response under 200 words. Be specific to CagriSema RWE data."
                )
                ai_chart_resp = call_claude([{"role":"user","content":ai_chart_prompt}])

            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-label">AI Chart Recommendation — {target_team}</div>
              <div class="insight-obs">{ai_chart_resp}</div>
            </div>
            """, unsafe_allow_html=True)

            # Determine which chart to render based on keywords
            req = chart_input.lower()
            if any(k in req for k in ["race","demographic","ethnicity","ethnic"]):
                chart_df = df.groupby("race")["weight_reduction_pct"].agg(["mean","count"]).reset_index()
                chart_df.columns = ["race","weight_reduction_pct","n_patients"]
                fig_cc = px.bar(
                    chart_df, x="race", y="weight_reduction_pct",
                    title=f"Mean Weight Reduction (%) by Race — {target_team} View",
                    color="race",
                    color_discrete_sequence=[C_PRIMARY,C_LIGHT,C_GOOD,C_WARN,C_GRAY],
                    text="n_patients",
                    labels={"race":"Race / Ethnicity","weight_reduction_pct":"Mean Weight Reduction (%)","n_patients":"n patients"}
                )
                fig_cc.update_traces(texttemplate="n=%{text}", textposition="outside")
            elif any(k in req for k in ["insurance","payer","coverage"]):
                chart_df = df[["insurance","weight_reduction_pct"]].copy()
                fig_cc = px.box(
                    chart_df, x="insurance", y="weight_reduction_pct",
                    title=f"Weight Reduction Distribution by Insurance Type — {target_team} View",
                    color="insurance",
                    color_discrete_sequence=[C_PRIMARY,C_LIGHT,C_GOOD,C_WARN],
                    points="all" if target_team == "Payer / Market Access" else "outliers",
                    labels={"insurance":"Insurance Type","weight_reduction_pct":"Weight Reduction (%)"}
                )
            elif any(k in req for k in ["state","geographic","map","region"]):
                chart_df = generate_claims_summary()
                fig_cc = px.choropleth(
                    chart_df,
                    locations="state_abbr",
                    locationmode="USA-states",
                    color="rx_count",
                    scope="usa",
                    title=f"CagriSema Prescription Volume by State — {target_team} View",
                    color_continuous_scale=[[0,C_LIGHTGRAY],[0.5,C_LIGHT],[1.0,C_DARK]],
                    labels={"rx_count":"Rx Count"},
                    hover_data=["opportunity_score"] if target_team in ("Sales","Commercial / Marketing") else None,
                )
            elif any(k in req for k in ["age","band","group"]):
                df["age_band"] = pd.cut(df["age"], bins=[17,40,55,70,89],
                                         labels=["18-40","41-55","56-70","71+"])
                chart_df = df[["age_band","hba1c_reduction"]].copy()
                fig_cc = px.violin(
                    chart_df, x="age_band", y="hba1c_reduction",
                    title=f"HbA1c Reduction Distribution by Age Band — {target_team} View",
                    color="age_band",
                    color_discrete_sequence=[C_PRIMARY,C_LIGHT,C_GOOD,C_WARN],
                    box=True, points="all" if target_team == "Regulatory Affairs" else False,
                    labels={"age_band":"Age Band","hba1c_reduction":"HbA1c Reduction (pp)"}
                )
            elif any(k in req for k in ["sex","gender","female","male"]):
                chart_df = df[["weight_reduction_pct","sex"]].copy()
                fig_cc = px.histogram(
                    chart_df, x="weight_reduction_pct", color="sex",
                    title=f"Weight Reduction Distribution by Sex — {target_team} View",
                    barmode="overlay",
                    color_discrete_map={"Female":C_PRIMARY,"Male":C_LIGHT,"Non-binary":C_WARN},
                    nbins=30,
                    labels={"weight_reduction_pct":"Weight Reduction (%)","sex":"Sex"}
                )
            else:
                # Default: treatment comparison
                chart_df = df.sample(200, random_state=1)[["treatment","weight_reduction_pct"]].copy()
                fig_cc = px.strip(
                    chart_df, x="treatment", y="weight_reduction_pct",
                    title=f"Weight Reduction by Treatment Arm — {target_team} View",
                    color="treatment",
                    color_discrete_sequence=[C_PRIMARY,C_WARN,C_LIGHT,C_GOOD,C_GRAY],
                    labels={"treatment":"Treatment","weight_reduction_pct":"Weight Reduction (%)"}
                )

            fig_cc.update_layout(
                paper_bgcolor=C_WHITE, plot_bgcolor=C_WHITE,
                font_family="Inter, Arial", height=420,
                margin=dict(l=20,r=20,t=50,b=40),
                showlegend=False,
                xaxis=dict(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A")),
                yaxis=dict(tickfont=dict(color="#1A1A1A"), title_font=dict(color="#1A1A1A")),
            )
            st.plotly_chart(fig_cc, use_container_width=True)

            # SQL transparency
            with st.expander("View underlying SQL query (HITL Transparency)"):
                sample_sql = f"""-- Custom chart query — {target_team} — {datetime.now().strftime('%Y-%m-%d %H:%M')}
-- Request: {chart_input[:80]}...

SELECT
    p.race_concept_id,
    c.concept_name         AS race_ethnicity,
    AVG(m.value_as_number) AS mean_outcome,
    COUNT(DISTINCT p.person_id) AS n_patients
FROM   omop.PERSON p
JOIN   omop.MEASUREMENT m
         ON p.person_id = m.person_id
        AND m.measurement_concept_id = 3004410  -- Body weight
JOIN   omop.CONCEPT c
         ON p.race_concept_id = c.concept_id
JOIN   omop.DRUG_EXPOSURE de
         ON p.person_id = de.person_id
        AND de.drug_concept_id = 2395492        -- CagriSema (RxNorm)
WHERE  m.measurement_date >= de.drug_exposure_start_date
  AND  m.measurement_date <= de.drug_exposure_start_date + INTERVAL '12 months'
GROUP  BY p.race_concept_id, c.concept_name
ORDER  BY mean_outcome DESC;"""
                st.markdown(f'<div class="sql-block">{sample_sql}</div>', unsafe_allow_html=True)

            col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
            with col_dl1:
                st.button("Save to Evidence Package", key="save_ep", use_container_width=True)
            with col_dl2:
                st.button("Add to Medical Affairs Deck", key="add_ma", use_container_width=True)
            with col_dl3:
                st.button("Export SQL + Data Extract", key="exp_sql", use_container_width=True)
            with col_dl4:
                st.download_button(
                    "Download Chart Data (CSV)",
                    data=chart_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"custom_chart_{target_team.lower().replace(' / ','_').replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_chart_csv",
                    use_container_width=True,
                )



# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:0.8rem 0; border-bottom:1px solid {C_BORDER}; margin-bottom:0.8rem;">
          <div style="font-size:1rem; font-weight:800; color:{C_PRIMARY};">RWE Command Center</div>
          <div style="font-size:0.7rem; color:{C_GRAY};">CagriSema | US Market</div>
        </div>
        """, unsafe_allow_html=True)

        pages = [
            ("landing",    "Home / Landing"),
            ("cohort",     "Cohort Builder"),
            ("projects",   "Your Projects"),
            ("chat",       "Ask Anything"),
            ("upload",     "Upload Your Data"),
            ("payer",      "Payer Intelligence"),
            ("signal_lab", "Signal Lab"),
        ]
        for page_key, page_name in pages:
            is_active = st.session_state.current_page == page_key
            if st.button(
                f"{'> ' if is_active else '   '}{page_name}",
                key=f"sidebar_{page_key}",
                use_container_width=True
            ):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown(f"""
        <hr style="border-color:{C_BORDER};">
        <div style="font-size:0.7rem; color:{C_GRAY}; line-height:1.7;">
          <strong>Bias Mitigation Active</strong><br>
          <span class="bias-badge">Selection</span>
          <span class="bias-badge">Information</span>
          <span class="bias-badge">Confounding</span>
          <span class="bias-badge">AI Hallucination</span>
          <span class="bias-badge">Demographic</span>
        </div>
        <hr style="border-color:{C_BORDER};">
        <div style="font-size:0.7rem; color:{C_GRAY};">
          OMOP CDM v5.4 Active<br>
          HIPAA Safe Harbor Compliant<br>
          21 CFR Part 11 Audit Trail<br>
          FDA RWE Framework Aligned
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", key="signout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────────────────────
inject_css()

if not st.session_state.logged_in:
    render_login()
else:
    render_sidebar()
    page = st.session_state.current_page
    if   page == "landing":    render_landing()
    elif page == "cohort":     render_cohort()
    elif page == "projects":   render_projects()
    elif page == "chat":       render_chat()
    elif page == "upload":     render_upload()
    elif page == "payer":      render_payer()
    elif page == "signal_lab": render_signal_lab()
    else:                      render_landing()
