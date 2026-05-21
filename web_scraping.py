import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import pandas as pd

def get_sailing_events():
    """Κατεβάζει τα δεδομένα και τα επιστρέφει ως Pandas DataFrame για το Streamlit"""
    url = "https://offshore.org.gr/index.php?mx=Race_Schedule_2026&x=Program.xsl"
    
    try:
        response = requests.get(url)
        # Αν υπάρξει πρόβλημα, επιστρέφουμε ένα άδειο DataFrame
        if response.status_code != 200:
            return pd.DataFrame(columns=["Ημερομηνία", "Αγώνας", "Όμιλος", "Περιφέρεια", "Διαδρομή", "Μίλια"])
            
        soup = BeautifulSoup(response.content, 'xml')
        races = soup.find_all('ROW')
        
        data = []
        for row in races:
            name = row.find('REGATTA').text if row.find('REGATTA') else 'Άγνωστος Αγώνας'
            start_date = row.find('FRDATE').text if row.find('FRDATE') else '-'
            club = row.find('CLUB').text if row.find('CLUB') else '-'
            course = row.find('COURSE').text if row.find('COURSE') else '-'
            
            # Προσθήκη χρονιάς (2026)
            if start_date != "-":
                full_date_str = f"{start_date}/2026" 
            else:
                full_date_str = "-"

            data.append({
                "Ημερομηνία": full_date_str,
                "Αγώνας": name,
                "Όμιλος": club,
                "Περιφέρεια": "Πανελλαδικά",  # Σταθερό κείμενο για το UI, αφού δεν υπάρχει στο XML
                "Διαδρομή": course,
                "Μίλια": "0"                  # Σταθερό κείμενο για το UI
            })
            
        return pd.DataFrame(data, columns=["Ημερομηνία", "Αγώνας", "Όμιλος", "Περιφέρεια", "Διαδρομή", "Μίλια"])
        
    except Exception as e:
        print(f"Σφάλμα κατά το scraping: {e}")
        return pd.DataFrame(columns=["Ημερομηνία", "Αγώνας", "Όμιλος", "Περιφέρεια", "Διαδρομή", "Μίλια"])


def create_ics_file(df):
    """Παίρνει το DataFrame και επιστρέφει το αρχείο .ics έτοιμο για κατέβασμα"""
    cal = Calendar()
    cal.add('prodid', '-//Εργασία ΕΑΠ - Ημερολόγιο Ιστιοπλοΐας//')
    cal.add('version', '2.0')
    
    for _, row in df.iterrows():
        if row['Ημερομηνία'] != "-":
            try:
                dt = datetime.strptime(row['Ημερομηνία'], "%d/%m/%Y")
                event = Event()
                event.add('summary', row['Αγώνας'])
                event.add('description', f"Όμιλος: {row['Όμιλος']}\nΔιαδρομή: {row['Διαδρομή']}")
                event.add('dtstart', dt.date()) # Χρησιμοποιούμε μόνο την ημερομηνία
                cal.add_component(event)
            except Exception:
                pass
                
    return cal.to_ical()