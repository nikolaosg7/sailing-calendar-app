import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from icalendar import Calendar, Event

st.set_page_config(
    page_title="Sailing Calendar 2026",
    layout="wide",
    page_icon="⛵",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Barlow', sans-serif !important;
        background-color: #ffffff !important;
        color: #1a2a40 !important;
    }
    .main .block-container {
        background-color: #ffffff !important;
        padding: 1.5rem 2rem;
    }
    .fs-header {
        background: #ffffff !important;
        border-bottom: 4px solid #0056b3 !important;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    .fs-header h1 {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #0056b3 !important;
        margin: 0 !important;
        text-transform: uppercase !important;
    }
    .fs-badge {
        background-color: #0056b3 !important;
        color: #ffffff !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        padding: 4px 10px !important;
        border-radius: 4px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    .fs-section-header {
        background: #0056b3 !important;
        padding: 12px 14px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 0px !important;
        border-radius: 4px 4px 0 0 !important;
        text-align: center !important;
    }
    .fs-row-header {
        display: grid !important;
        grid-template-columns: 1fr 1fr 3fr 2.5fr 2.5fr 1fr !important;
        align-items: center !important;
        text-align: center !important;
        background: #e9ecef !important;
        border-bottom: 2px solid #ced4da !important;
        padding: 12px 10px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #1a2a40 !important;
        text-transform: uppercase !important;
    }
    .fs-row {
        display: grid !important;
        grid-template-columns: 1fr 1fr 3fr 2.5fr 2.5fr 1fr !important;
        align-items: center !important;
        text-align: center !important;
        background-color: #ffffff !important;
        border-bottom: 1px solid #dee2e6 !important;
        border-left: 1px solid #dee2e6 !important;
        border-right: 1px solid #dee2e6 !important;
        padding: 12px 10px !important;
        transition: background 0.15s ease !important;
        font-size: 1rem;
    }
    .fs-row:hover { background-color: #f1f3f5 !important; }
    .fs-row-time  { font-family:'Barlow Condensed',sans-serif !important; font-size:1.1rem !important; font-weight:700 !important; color:#0056b3 !important; }
    .fs-row-hour  { font-size:0.95rem !important; color:#495057 !important; font-weight:600 !important; }
    .fs-row-name  { font-weight:700 !important; color:#000000 !important; }
    .fs-row-club  { color:#0056b3 !important; font-size:0.95rem !important; font-weight:700 !important; }
    .fs-row-route { color:#495057 !important; font-size:0.95rem !important; font-weight:600 !important; }
    .fs-row-miles { font-family:'Barlow Condensed',sans-serif !important; font-size:1.2rem !important; font-weight:700 !important; color:#0056b3 !important; }
    .fs-miles-label { font-size:0.8rem !important; color:#6c757d !important; font-weight:600 !important; }
    .fs-metric-card {
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        text-align: center !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    .fs-metric-value { font-family:'Barlow Condensed',sans-serif !important; font-size:2.8rem !important; font-weight:700 !important; color:#0056b3 !important; line-height:1 !important; }
    .fs-metric-label { font-size:0.9rem !important; font-weight:700 !important; color:#495057 !important; text-transform:uppercase !important; letter-spacing:0.5px !important; margin-top:4px !important; }

    /* SIDEBAR FIX */
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div:first-child {
        background-color: #f0f6ff !important;
        border-right: 2px solid #0056b3 !important;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #0056b3 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] .stRadio label, section[data-testid="stSidebar"] .stRadio label p,
    section[data-testid="stSidebar"] .stRadio label span, section[data-testid="stSidebar"] [data-baseweb="radio"] label,
    section[data-testid="stSidebar"] [data-baseweb="radio"] span, section[data-testid="stSidebar"] [role="radiogroup"] label,
    section[data-testid="stSidebar"] [role="radiogroup"] span {
        color: #0056b3 !important;
        font-size: 1.0rem !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] span,
    section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] label {
        color: #003d80 !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input, section[data-testid="stSidebar"] input[type="text"] {
        background-color: #ffffff !important;
        border: 2px solid #0056b3 !important;
        color: #0056b3 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }
    section[data-testid="stSidebar"] .stTextInput input::placeholder {
        color: #6aabee !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2, section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #0056b3 !important;
        font-weight: 700 !important;
    }

    .stButton > button, .stDownloadButton > button {
        background: #0056b3 !important; color: #ffffff !important;
        font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important;
        font-size: 1.1rem !important; letter-spacing: 1px !important; text-transform: uppercase !important;
        border: none !important; border-radius: 6px !important; padding: 12px 20px !important; width: 100% !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { background: #004494 !important; }

    #MainMenu, footer { visibility: hidden !important; }
    header { background: transparent !important; }

    /* FIX: Απόκρυψη κουμπιού sidebar (πιο ασφαλές) */
    button[kind="header"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── XML Parsing (FIX: πιο ανθεκτικό parsing ημερομηνιών) ──
@st.cache_data(ttl=86400)  # FIX: 24 ώρες αντί 1 ώρα
def get_sailing_events():
    url = "https://offshore.org.gr/index.php?mx=Race_Schedule_2026&x=Program.xsl"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return pd.DataFrame()
        root = ET.fromstring(response.content)
        data = []
        for district in root.findall('.//DISTRICT'):
            region_name = district.get('Name', 'ΛΟΙΠΟΙ ΑΓΩΝΕΣ')
            for regatta in district.findall('REGATTA'):
                regatta_name = regatta.get('Name', '-')
                clubname_el = regatta.find('CLUBNAME')
                club = clubname_el.text.strip() if clubname_el is not None and clubname_el.text else "-"
                races = regatta.findall('RACE')
                if races:
                    for race in races:
                        course = race.get('Name', '-')
                        length_el = race.find('LENGTH')
                        distance = length_el.text.strip() if length_el is not None and length_el.text else '0'
                        stdate_el = race.find('STDATE')
                        stdate_text = stdate_el.text if stdate_el is not None and stdate_el.text else ''
                        date_str, time_str = parse_date(stdate_text)
                        data.append({
                            "Ημερομηνία": date_str, "Ώρα": time_str, "Αγώνας": regatta_name,
                            "Όμιλος": club, "Περιφέρεια": region_name, "Διαδρομή": course, "Μίλια": distance
                        })
                else:
                    course_el = regatta.find('COURSE')
                    course = course_el.text.strip() if course_el is not None and course_el.text else '-'
                    length_el = regatta.find('LENGTH')
                    distance = length_el.text.strip() if length_el is not None and length_el.text else '0'
                    frdate_el = regatta.find('FRDATE')
                    frdate_text = frdate_el.text if frdate_el is not None and frdate_el.text else ''
                    date_str, time_str = parse_date(frdate_text)
                    data.append({
                        "Ημερομηνία": date_str, "Ώρα": time_str, "Αγώνας": regatta_name,
                        "Όμιλος": club, "Περιφέρεια": region_name, "Διαδρομή": course, "Μίλια": distance
                    })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Σφάλμα κατά το scraping: {e}")
        return pd.DataFrame()

# FIX: parse_date με έλεγχο μήκους για 8,12 ή περισσότερους χαρακτήρες
def parse_date(stdate_text):
    """Μετατρέπει '20260419110000000' → ('19/04/2026', '11:00')
       και '20260419' → ('19/04/2026', '-')
    """
    if not stdate_text or len(stdate_text) < 8:
        return "-", "-"
    yyyy = stdate_text[0:4]
    mm = stdate_text[4:6]
    dd = stdate_text[6:8]
    if len(stdate_text) >= 12:
        hh = stdate_text[8:10]
        mins = stdate_text[10:12]
        return f"{dd}/{mm}/{yyyy}", f"{hh}:{mins}"
    else:
        return f"{dd}/{mm}/{yyyy}", "-"

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
                # FIX: προσθήκη dtend (προαιρετικά) - αν θέλεις ολόκληρη μέρα, μην το βάλεις
                # Αλλά για ολόημερο event, το icalendar χρειάζεται dtend = dt + 1 ημέρα;
                # Θα το αφήσω χωρίς dtend, όπως ήταν.
                cal.add_component(event)
            except Exception:
                pass
    return cal.to_ical()

# ── Φόρτωση Δεδομένων ──
with st.spinner('Γίνεται άντληση πραγματικών δεδομένων...'):
    df = get_sailing_events()

if not df.empty:
    region_counts = df["Περιφέρεια"].value_counts().to_dict()
    total_races = len(df)
    region_options = ["Όλες"] + sorted(df["Περιφέρεια"].unique().tolist())
else:
    region_counts = {}
    total_races = 0
    region_options = ["Όλες"]

def format_region(option):
    if option == "Όλες":
        return f"📍 Όλες ({total_races})"
    # FIX: αν region_counts δεν έχει το κλειδί, δίνει 0
    return f"⚓ {option} ({region_counts.get(option, 0)})"

# ── Sidebar ──
st.sidebar.markdown("## ⛵ SAILING CALENDAR")
st.sidebar.markdown("---")

selected_region = st.sidebar.radio(
    "ΠΕΡΙΦΕΡΕΙΕΣ",
    options=region_options,
    format_func=format_region,
    label_visibility="collapsed"
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
search_term = st.sidebar.text_input(
    "Αναζήτηση αγώνα...",
    label_visibility="collapsed",
    placeholder="🔍 Αναζήτηση αγώνα..."
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.85rem;color:#0056b3;text-align:center;font-weight:700;'>ΠΛΗΠΡΟ · Ομαδική Εργασία<br>Έκδοση 1.2</div>",
    unsafe_allow_html=True
)

# ── Filters ──
df_filtered = df.copy()

if not df_filtered.empty:
    current_date = datetime.now().date()
    keep = []
    for _, row in df_filtered.iterrows():
        try:
            # FIX: αν η ημερομηνία είναι "-" την προσπερνάμε (δεν την κρατάμε)
            if row['Ημερομηνία'] == "-":
                keep.append(False)
                continue
            race_date = datetime.strptime(row['Ημερομηνία'], "%d/%m/%Y").date()
            keep.append(race_date >= current_date)
        except:
            keep.append(False)  # FIX: αν αποτύχει, μην το συμπεριλάβεις
    df_filtered = df_filtered[keep]

    if selected_region != "Όλες":
        df_filtered = df_filtered[df_filtered["Περιφέρεια"] == selected_region]
    if search_term:
        df_filtered = df_filtered[df_filtered["Αγώνας"].str.contains(search_term, case=False, na=False)]

# ── Header ──
st.markdown("""
    <div class="fs-header">
        <span style="font-size:2.2rem">⛵</span>
        <h1>Sailing Calendar 2026</h1>
        <span class="fs-badge">LIVE DATA</span>
    </div>
""", unsafe_allow_html=True)

# ── Metrics (FIX: safe_int απλοποιημένο) ──
def safe_int(val):
    try:
        # Αν είναι string, αφαιρούμε κόμμα και μετατρέπουμε
        if isinstance(val, str):
            val = val.replace(',', '.')
        return int(float(val))
    except:
        return 0

c1, c2, c3, c4 = st.columns(4)
total_miles = sum(safe_int(x) for x in df_filtered["Μίλια"]) if not df_filtered.empty else 0
regions_cnt = df_filtered["Περιφέρεια"].nunique() if not df_filtered.empty else 0
clubs_cnt   = df_filtered["Όμιλος"].nunique()     if not df_filtered.empty else 0

with c1:
    st.markdown(f'<div class="fs-metric-card"><div class="fs-metric-value">{len(df_filtered)}</div><div class="fs-metric-label">Αγώνες</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="fs-metric-card"><div class="fs-metric-value">{regions_cnt}</div><div class="fs-metric-label">Περιφέρειες</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="fs-metric-card"><div class="fs-metric-value">{clubs_cnt}</div><div class="fs-metric-label">Όμιλοι</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="fs-metric-card"><div class="fs-metric-value">{total_miles}</div><div class="fs-metric-label">Σύνολο Μιλίων</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Race Table ──
if df_filtered.empty:
    st.markdown('<div style="text-align:center;padding:40px;color:#495057;font-size:1.1rem;font-weight:700;">⚓ ΔΕΝ ΒΡΕΘΗΚΑΝ ΑΓΩΝΕΣ</div>', unsafe_allow_html=True)
else:
    for region, group in df_filtered.groupby("Περιφέρεια"):
        st.markdown(f'<div class="fs-section-header">🌊 &nbsp; ΕΛΛΑΔΑ · {region.upper()}</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="fs-row-header">
                <span>Ημ/νία</span>
                <span>Ώρα</span>
                <span>Αγώνας</span>
                <span>Όμιλος</span>
                <span>Διαδρομή</span>
                <span>Απόσταση</span>
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
        st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)

# ── Export ──
st.markdown("<br>", unsafe_allow_html=True)
col_btn, _ = st.columns([1, 3])
with col_btn:
    if not df_filtered.empty:
        ics_data = create_ics_file(df_filtered)
        st.download_button(
            label="⬇ ΕΞΑΓΩΓΗ .ICS",
            data=ics_data,
            file_name="sailing_calendar_2026.ics",
            mime="text/calendar"
        )
