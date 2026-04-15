import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime

def scrape_and_export_xml():
    # Το link που έχει ΠΑΝΤΑ τα δεδομένα σε δομημένη μορφή XML
    url = "https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl"
    
    print("🌍 Γίνεται λήψη δεδομένων από το XML της Ομοσπονδίας...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Σφάλμα σύνδεσης: {response.status_code}")
        return
        
    # Διαβάζουμε το XML
    soup = BeautifulSoup(response.content, 'xml')
    races = soup.find_all('ROW') # Στο XML κάθε αγώνας είναι μέσα σε ένα tag <ROW>
    
    if not races:
        print("⚠️ Η σελίδα κατέβηκε, αλλά δεν βρέθηκαν δεδομένα αγώνων.")
        return
        
    print(f"✅ Βρέθηκαν {len(races)} αγώνες! Ξεκινάει η δημιουργία του Ημερολογίου...\n")
    print("-" * 40)
    
    # Προετοιμασία του iCalendar
    cal = Calendar()
    cal.add('prodid', '-//Εργασία ΕΑΠ - Ημερολόγιο Ιστιοπλοΐας//')
    cal.add('version', '2.0')
    
    for row in races:
        # Τραβάμε τα στοιχεία (αν δεν υπάρχει κάτι, βάζουμε παύλα)
        name = row.find('REGATTA').text if row.find('REGATTA') else 'Άγνωστος Αγώνας'
        start_date = row.find('FRDATE').text if row.find('FRDATE') else ''
        club = row.find('CLUB').text if row.find('CLUB') else '-'
        course = row.find('COURSE').text if row.find('COURSE') else '-'
        
        # Τυπώνουμε στην οθόνη για να βλέπουμε τι γίνεται
        print(f"⛵ {start_date:<6} | {name} ({club})")
        
        # Προσθήκη στο iCalendar
        if start_date and start_date != "-":
            try:
                # Μετατρέπουμε το "14/05" σε "14/05/2022" για να το καταλάβει το ημερολόγιο
                full_date_str = f"{start_date}/2022" 
                dt = datetime.strptime(full_date_str, "%d/%m/%Y")
                
                event = Event()
                event.add('summary', name) # Τίτλος στο ημερολόγιο
                event.add('description', f"Όμιλος: {club}\nΔιαδρομή: {course}") # Περιγραφή
                event.add('dtstart', dt) # Ημερομηνία
                
                cal.add_component(event)
            except Exception as e:
                # Αν η ημερομηνία έχει περίεργη μορφή, απλά την προσπερνάμε σιωπηλά
                pass

    print("-" * 40)
    
    # Αποθήκευση του αρχείου
    filename = "sailing_calendar.ics"
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
        
    print(f"\n💾 ΤΕΛΟΣ! Το αρχείο '{filename}' δημιουργήθηκε επιτυχώς στον φάκελό σου!")

# Εκτέλεση
if __name__ == "__main__":
    scrape_and_export_xml()