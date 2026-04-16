import streamlit as st
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime

# 1. Ρυθμίσεις Σελίδας (UI/UX)
st.set_page_config(page_title="TEST MODE - Sailing Calendar", layout="wide", page_icon="🧪")

# Custom CSS για να το κάνουμε να φαίνεται "Pro"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stDataFrame { border: 1px solid #e6e9ef; }
    </style>
    """, unsafe_allow_html=True)

# 2. Δημιουργία Ενδεικτικών Δεδομένων (Mock Data)
# Αυτά τα δεδομένα προσομοιώνουν το Web Scraping
def get_mock_data():
    data = [
        {"Ημερομηνία": "15/05/2026", "Αγώνας": "Ράλλυ Αιγαίου", "Όμιλος": "ΠΟΙΑΘ", "Περιφέρεια": "Αττική", "Διαδρομή": "Φάληρο-Πάτμος", "Μίλια": "150"},
        {"Ημερομηνία": "20/06/2026", "Αγώνας": "Κύπελλο Ευρίπου", "Όμιλος": "ΝΟΧ", "Περιφέρεια": "Εύβοια", "Διαδρομή": "Χαλκίδα-Ερέτρια", "Μίλια": "25"},
        {"Ημερομηνία": "05/07/2026", "Αγώνας": "North Aegean Cup", "Όμιλος": "ΝΟΘ", "Περιφέρεια": "Θεσσαλονίκη", "Διαδρομή": "Θερμαϊκός", "Μίλια": "40"},
        {"Ημερομηνία": "12/08/2026", "Αγώνας": "Ionian Regatta", "Όμιλος": "ΝΟΙ", "Περιφέρεια": "Ιόνιο", "Διαδρομή": "Κέρκυρα-Παξοί", "Μίλια": "35"},
        {"Ημερομηνία": "15/09/2026", "Αγώνας": "Κύπελλο Σαρωνικού", "Όμιλος": "ΝΟΕ", "Περιφέρεια": "Αττική", "Διαδρομή": "Φάληρο-Αίγινα", "Μίλια": "18"},
    ]
    return pd.DataFrame(data)

# --- Main Interface Logic ---
st.title("🧪 Περιβάλλον Δοκιμών Interface")
st.info("Αυτή η σελίδα χρησιμοποιεί **εικονικά δεδομένα** για δοκιμή του UI.")

df = get_mock_data()

# --- Sidebar: Φίλτρα (Δοκιμή λειτουργικότητας) ---
st.sidebar.header("⚙️ Ρυθμίσεις Δοκιμής")
selected_region = st.sidebar.selectbox("Δοκιμή Φίλτρου Περιφέρειας:", ["Όλες"] + list(df['Περιφέρεια'].unique()))
search_term = st.sidebar.text_input("Δοκιμή Αναζήτησης:")

# Εφαρμογή Φίλτρων στα Mock Data
df_filtered = df.copy()
if selected_region != "Όλες":
    df_filtered = df_filtered[df_filtered['Περιφέρεια'] == selected_region]
if search_term:
    df_filtered = df_filtered[df_filtered['Αγώνας'].str.contains(search_term, case=False)]

# --- Εμφάνιση Αποτελεσμάτων ---
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Πίνακας Αγώνων")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Ενέργειες")
    if st.button("Προσομοίωση Εξαγωγής .ics"):
        st.success("Το αρχείο δημιουργήθηκε επιτυχώς (Test Mode)")
    
    st.write("---")
    st.metric(label="Σύνολο Αγώνων", value=len(df_filtered))

# --- Footer ---
st.write("---")
st.caption("Development Mode | ΠΛΗΠΡΟ Ομαδική Εργασία")