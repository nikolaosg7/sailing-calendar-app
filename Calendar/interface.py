import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import io

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Sailing Calendar Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_status_code=True)

@st.cache_data
def get_data():
    url = "https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        races = []
        for row in soup.find_all('ROW'):
            races.append({
                'Ημερομηνία': row.find('FRDATE').text if row.find('FRDATE') else '-',
                'Αγώνας': row.find('REGATTA').text if row.find('REGATTA') else '-',
                'Όμιλος': row.find('CLUB').text if row.find('CLUB') else '-',
                'Διαδρομή': row.find('COURSE').text if row.find('COURSE') else '-',
                'Μίλια': row.find('DISTANCE').text if row.find('DISTANCE') else '-'
            })
        return pd.DataFrame(races)
    except:
        return pd.DataFrame()

def create_ical(df):
    cal = Calendar()
    for _, row in df.iterrows():
        if row['Ημερομηνία'] != '-':
            event = Event()
            event.add('summary', row['Αγώνας'])
            try:
                dt = datetime.strptime(f"{row['Ημερομηνία']}/2022", "%d/%m/%Y")
                event.add('dtstart', dt)
                cal.add_component(event)
            except: continue
    return cal.to_ical()

# --- UI ---
st.title("⛵ Sailing Calendar Pro v1.0")
st.info("Συγχρονισμένα δεδομένα από ΕΑΘ/ΕΙΟ")

df = get_data()

if not df.empty:
    # Sidebar Φίλτρα
    st.sidebar.header("🔍 Αναζήτηση")
    search = st.sidebar.text_input("Αναζήτηση Αγώνα ή Ομίλου:")
    
    if search:
        df_display = df[df['Αγώνας'].str.contains(search, case=False) | df['Όμιλος'].str.contains(search, case=False)]
    else:
        df_display = df

    # Display Data
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Export Button
    ics_data = create_ical(df_display)
    st.download_button(
        label="📅 Εξαγωγή Επιλεγμένων σε iCalendar (.ics)",
        data=ics_data,
        file_name="my_sailing_calendar.ics",
        mime="text/calendar"
    )
else:
    st.error("Δεν βρέθηκαν δεδομένα. Ελέγξτε τη σύνδεση.")