import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Sailing Calendar Pro", layout="wide", page_icon="⛵")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_data():
    # Το ζωντανό link για το τρέχον έτος (2026)
    url = "https://www.offshore.org.gr/index.php?mx=Race_Schedule_2026&x=Program.xsl"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame()
            
        soup = BeautifulSoup(response.content, 'xml')
        races = []
        for row in soup.find_all('ROW'):
            races.append({
                'Ημερομηνία': row.find('FRDATE').text if row.find('FRDATE') else '-',
                'Αγώνας': row.find('REGATTA').text if row.find('REGATTA') else '-',
                'Όμιλος': row.find('CLUB').text if row.find('CLUB') else '-',
                'Περιφέρεια': row.find('DISTRICT').text if row.find('DISTRICT') else 'Άγνωστη', # Νέο πεδίο!
                'Διαδρομή': row.find('COURSE').text if row.find('COURSE') else '-',
                'Μίλια': row.find('DISTANCE').text if row.find('DISTANCE') else '-'
            })
        return pd.DataFrame(races)
    except:
        return pd.DataFrame()

# --- Main App ---
st.title("⛵ Sailing Calendar Pro")
st.write("Επίσημο Ημερολόγιο Αγώνων ΕΑΘ/ΕΙΟ (2026)")
st.write("---")

df = get_data()

if not df.empty:
    # --- Sidebar: Φίλτρα ---
    st.sidebar.header("🔍 Φίλτρα")
    
    # 1. Φίλτρο Περιφέρειας (Βάσει Εκφώνησης)
    regions = ["Όλες"] + sorted(df['Περιφέρεια'].unique().tolist())
    selected_region = st.sidebar.selectbox("Επιλογή Περιφέρειας:", regions)
    
    # 2. Αναζήτηση Κειμένου
    search = st.sidebar.text_input("Αναζήτηση (Αγώνας/Όμιλος):")
    
    # Εφαρμογή Φίλτρων
    df_display = df.copy()
    if selected_region != "Όλες":
        df_display = df_display[df_display['Περιφέρεια'] == selected_region]
        
    if search:
        df_display = df_display[df_display['Αγώνας'].str.contains(search, case=False) | df_display['Όμιλος'].str.contains(search, case=False)]

    # --- Εμφάνιση Πίνακα ---
    st.subheader(f"📅 Βρέθηκαν {len(df_display)} Αγώνες")
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # --- iCalendar Logic ---
    cal = Calendar()
    for _, r in df_display.iterrows():
        if r['Ημερομηνία'] != '-':
            try:
                event = Event()
                event.add('summary', r['Αγώνας'])
                event.add('description', f"Όμιλος: {r['Όμιλος']}\nΠεριφέρεια: {r['Περιφέρεια']}\nΔιαδρομή: {r['Διαδρομή']}")
                
                # Εδώ πλέον βάζουμε το 2026!
                dt = datetime.strptime(f"{r['Ημερομηνία']}/2026", "%d/%m/%Y")
                event.add('dtstart', dt)
                cal.add_component(event)
            except: continue

    # --- Κουμπί Εξαγωγής ---
    st.download_button(
        label="📥 Λήψη Ημερολογίου (.ics)",
        data=cal.to_ical(),
        file_name=f"sailing_calendar_{selected_region if selected_region != 'Όλες' else 'All'}.ics",
        mime="text/calendar",
        help="Κατεβάστε το αρχείο για να το εισάγετε σε Google Calendar ή Outlook."
    )
else:
    st.error("❌ Δεν βρέθηκαν δεδομένα. Η Ομοσπονδία ίσως να μην έχει αναρτήσει το ημερολόγιο ή η σύνδεση απέτυχε.")