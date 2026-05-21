import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from icalendar import Calendar, Event

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(
    page_title="Sailing Calendar 2026",
    layout="wide",
    page_icon="⛵",
    initial_sidebar_state="expanded" 
)

# 2. Custom CSS — Flashscore Dark Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Barlow', sans-serif;
        background-color: #1a1a2e;
        color: #e0e0e0;
    }
    .main .block-container {
        background-color: #1a1a2e;
        padding: 1.5rem 2rem;
    }
    .fs-header {
        background: linear-gradient(90deg, #0d0d1a 0%, #1a1a2e 100%);
        border-bottom: 2px solid #ff6600;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        border-radius: 6px 6px 0 0;
    }
    .fs-header h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .fs-badge {
        background-color: #28a745;
        color: #fff;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .fs-section-header {
        background: linear-gradient(90deg, #252540 0%, #1e1e35 100%);
        border-left: 3px solid #ff6600;
        padding: 8px 14px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #ff9944;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 2px;
        border-radius: 0 4px 4px 0;
    }
    .fs-row {
        display: flex;
        align-items: center;
        background-color: #1e1e35;
        border-bottom: 1px solid #2a2a45;
        padding: 10px 14px;
        transition: background 0.15s ease;
        cursor: pointer;
        font-size: 0.88rem;
    }
    .fs-row:hover {
        background-color: #26264a;
    }
    .fs-row-time {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #ff9944;
        min-width: 70px;
    }
    .fs-row-hour {
        font-size: 0.85rem;
        color: #a0a0b0;
        min-width: 50px;
    }
    .fs-row-name {
        flex: 1;
        font-weight: 600;
        color: #f0f0f0;
        padding-left: 10px;
    }
    .fs-row-club {
        color: #8888aa;
        font-size: 0.8rem;
        min-width: 80px;
        text-align: center;
    }
    .fs-row-route {
        color: #aaaacc;
        font-size: 0.8rem;
        min-width: 160px;
        text-align: center;
    }
    .fs-row-miles {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #66ccff;
        min-width: 60px;
        text-align: right;
    }
    .fs-miles-label {
        font-size: 0.7rem;
        color: #556677;
        font-weight: 400;
    }
    .fs-metric-card {
        background: linear-gradient(135deg, #1e1e35, #252548);
        border: 1px solid #2e2e55;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .fs-metric-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #ff6600;
        line-height: 1;
    }
    .fs-metric-label {
        font-size: 0.75rem;
        color: #8888aa;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    section[data-testid="stSidebar"] {
        background-color: #12121f !important;
        border-right: 1px solid #2a2a45;
    }
    section[data-testid="stSidebar"] p {
        color: #aaaacc !important;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .stRadio label {
        cursor: pointer !important;
        font-size: 1.05rem !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
    }
    .stRadio > div {
        gap: 8px;
    }
    .stTextInput > div > div > input {
        background-color: #252540 !important;
        border: 1px solid #3a3a60 !important;
        color: #e0e0e0 !important;
    }
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(90deg, #ff6600, #ff8800) !important;
        color: #fff !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        opacity: 0.85 !important;
    }
    .fs-footer {
        margin-top: 30px;
        padding: 10px 0;
        border-top: 1px solid #2a2a45;
        font-size: 0.75rem;
        color: #555577;
        text-align: center;
        letter-spacing: 0.8px;
    }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)


# 3. Backend: Το πραγματικό XML Parsing της ΕΑΘ
@st.cache_data(ttl=3600)
def get_sailing_events():
    url = "https://offshore.org.gr/index.php?mx=Race_Schedule_2026&x=Program.xsl"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return pd.DataFrame()
            
        # Χρησιμοποιούμε τη βιβλιοθήκη ElementTree της Python
        root = ET.fromstring(response.content)
        data = []
        
        # 1. Βρίσκουμε όλες τις περιφέρειες
        for district in root.findall('.//DISTRICT'):
            region_name = district.get('Name', 'ΛΟΙΠΟΙ ΑΓΩΝΕΣ')
            
            # 2. Βρίσκουμε τους αγώνες μέσα στην περιφέρεια
            for regatta in district.findall('REGATTA'):
                regatta_name = regatta.get('Name', '-')
                
                club_el = regatta.find('CLUB')
                club = club_el.text if club_el is not None else '-'
                
                # 3. Βρίσκουμε τα σκέλη (διαδρομές) του αγώνα
                for race in regatta.findall('RACE'):
                    course = race.get('Name', '-')
                    
                    length_el = race.find('LENGTH')
                    distance = length_el.text if length_el is not None else '0'
                    if not distance:
                        distance = '0'
                    
                    stdate_el = race.find('STDATE')
                    stdate_text = stdate_el.text if stdate_el is not None else ''
                    
                    # 4. Αποκωδικοποίηση της τρελής ημερομηνίας της ΕΑΘ (π.χ. 20260228110000000)
                    date_str = "-"
                    time_str = "-"
                    if stdate_text and len(stdate_text) >= 12:
                        yyyy = stdate_text[0:4]
                        mm = stdate_text[4:6]
                        dd = stdate_text[6:8]
                        hh = stdate_text[8:10]
                        mins = stdate_text[10:12]
                        
                        date_str = f"{dd}/{mm}/{yyyy}"
                        time_str = f"{hh}:{mins}"

                    data.append({
                        "Ημερομηνία": date_str,
                        "Ώρα": time_str,
                        "Αγώνας": regatta_name,
                        "Όμιλος": club,
                        "Περιφέρεια": region_name,
                        "Διαδρομή": course,
                        "Μίλια": distance
                    })
                    
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"Σφάλμα κατά το scraping: {e}")
        return pd.DataFrame()

def create_ics_file(df):
    cal = Calendar()
    cal.add('prodid', '-//Εργασία ΕΑΠ - Ημερολόγιο Ιστιοπλοΐας//')
    cal.add('version', '2.0')
    
    for _, row in df.iterrows():
        if row['Ημερομηνία'] != "-":
            try:
                dt_str = row['Ημερομηνία']
                if row['Ώρα'] != "-":
                    dt_str += f" {row['Ώρα']}"
                    dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
                else:
                    dt = datetime.strptime(dt_str, "%d/%m/%Y")

                event = Event()
                event.add('summary', row['Αγώνας'])
                event.add('description', f"Όμιλος: {row['Όμιλος']}\nΔιαδρομή: {row['Διαδρομή']}\nΑπόσταση: {row['Μίλια']} nm")
                event.add('dtstart', dt) 
                cal.add_component(event)
            except Exception:
                pass
                
    return cal.to_ical()


# 4. Φόρτωση Δεδομένων
with st.spinner('Γίνεται άντληση πραγματικών δεδομένων από την ΕΑΘ...'):
    df = get_sailing_events()

# --- Υπολογισμοί για το μενού ---
if not df.empty:
    region_counts = df["Περιφέρεια"].value_counts().to_dict()
    total_races = len(df)
    region_options = ["Όλες"] + sorted(list(df["Περιφέρεια"].unique()))
else:
    region_counts = {}
    total_races = 0
    region_options = ["Όλες"]

def format_region(option):
    if option == "Όλες":
        return f"📍 Όλες ({total_races})"
    else:
        return f"⚓ {option} ({region_counts.get(option, 0)})"

# ── Sidebar ──────────────────────────────────────────────
st.sidebar.markdown("## ⛵ SAILING CALENDAR")
st.sidebar.markdown("---")

selected_region = st.sidebar.radio(
    "ΠΕΡΙΦΕΡΕΙΕΣ",
    options=region_options,
    format_func=format_region
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
search_term = st.sidebar.text_input("Αναζήτηση αγώνα")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.7rem;color:#555577;text-align:center;'>ΠΛΗΠΡΟ · Ομαδική Εργασία<br>Έκδοση 1.0</div>",
    unsafe_allow_html=True
)

# ── Filters ──────────────────────────────────────────────
df_filtered = df.copy()
if not df_filtered.empty:
    if selected_region != "Όλες":
        df_filtered = df_filtered[df_filtered["Περιφέρεια"] == selected_region]
    if search_term:
        df_filtered = df_filtered[df_filtered["Αγώνας"].str.contains(search_term, case=False, na=False)]

# ── Header ───────────────────────────────────────────────
st.markdown("""
    <div class="fs-header">
        <span style="font-size:1.5rem">⛵</span>
        <h1>Sailing Calendar 2026</h1>
        <span class="fs-badge">LIVE DATA</span>
    </div>
""", unsafe_allow_html=True)

# ── Metrics ──────────────────────────────────────────────
def safe_int(val):
    try:
        # Αντικαθιστούμε τα κόμματα με τελείες σε περίπτωση δεκαδικών π.χ. "15,5"
        clean_val = str(val).replace(',', '.')
        # Αν έχει πράξεις πχ "2*4/10" που είδαμε στο XML, θα πάρει το 0 για ασφάλεια
        return int(float(clean_val))
    except:
        return 0

c1, c2, c3, c4 = st.columns(4)
regions_count = df_filtered["Περιφέρεια"].nunique() if not df_filtered.empty else 0
clubs_count = df_filtered["Όμιλος"].nunique() if not df_filtered.empty else 0
total_miles = sum(safe_int(x) for x in df_filtered["Μίλια"]) if not df_filtered.empty else 0

with c1:
    st.markdown(f"""
        <div class="fs-metric-card">
            <div class="fs-metric-value">{len(df_filtered)}</div>
            <div class="fs-metric-label">Αγώνες</div>
        </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="fs-metric-card">
            <div class="fs-metric-value">{regions_count}</div>
            <div class="fs-metric-label">Περιφέρειες</div>
        </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="fs-metric-card">
            <div class="fs-metric-value">{clubs_count}</div>
            <div class="fs-metric-label">Όμιλοι</div>
        </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
        <div class="fs-metric-card">
            <div class="fs-metric-value">{total_miles}</div>
            <div class="fs-metric-label">Σύνολο Μιλίων</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Race Table ────────────────────
if df_filtered.empty:
    st.markdown("""
        <div style="text-align:center; padding:40px; color:#555577; font-size:0.9rem; letter-spacing:1px;">
            ⚓ ΔΕΝ ΒΡΕΘΗΚΑΝ ΑΓΩΝΕΣ ΑΠΟ ΤΟ EATH
        </div>
    """, unsafe_allow_html=True)
else:
    grouped = df_filtered.groupby("Περιφέρεια")
    for region, group in grouped:
        st.markdown(f"""
            <div class="fs-section-header">
                🌊 &nbsp; ΕΛΛΑΔΑ · {region.upper()}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="fs-row" style="font-size:0.72rem; color:#555577; text-transform:uppercase; letter-spacing:0.8px; padding:6px 14px; background:#14142a; cursor:default;">
                <span style="min-width:70px;">Ημ/νία</span>
                <span style="min-width:50px;">Ώρα</span>
                <span style="flex:1; padding-left:10px;">Αγώνας</span>
                <span style="min-width:80px; text-align:center;">Όμιλος</span>
                <span style="min-width:160px; text-align:center;">Διαδρομή</span>
                <span style="min-width:60px; text-align:right;">Απόσταση</span>
            </div>
        """, unsafe_allow_html=True)

        for _, row in group.iterrows():
            st.markdown(f"""
                <div class="fs-row">
                    <span class="fs-row-time">{row['Ημερομηνία']}</span>
                    <span class="fs-row-hour">{row['Ώρα']}</span>
                    <span class="fs-row-name">{row['Αγώνας']}</span>
                    <span class="fs-row-club">{row['Όμιλος']}</span>
                    <span class="fs-row-route">{row['Διαδρομή']}</span>
                    <span class="fs-row-miles">{row['Μίλια']} <span class="fs-miles-label">nm</span></span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:16px;'></div>", unsafe_allow_html=True)

# ── Export Button ─────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_btn, col_empty = st.columns([1, 3])
with col_btn:
    if not df_filtered.empty:
        ics_data = create_ics_file(df_filtered)
        st.download_button(
            label="⬇ ΕΞΑΓΩΓΗ .ICS",
            data=ics_data,
            file_name="sailing_calendar_2026.ics",
            mime="text/calendar"
        )

# ── Footer ────────────────────────────────────────────────
st.markdown("""
    <div class="fs-footer">
        ΠΛΗΠΡΟ · ΟΜΑΔΙΚΗ ΕΡΓΑΣΙΑ · 2026
    </div>
""", unsafe_allow_html=True)