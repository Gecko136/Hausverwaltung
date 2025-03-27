from hausverwaltung.db import get_wohnungen_pro_haus, get_haeuser, get_raeume, get_raeume_per_wohnung
from hausverwaltung.config import load_config

def show_haus_options():
    """
    Zeigt dem Benutzer eine Liste von Häusern an, die aus der Datenbank abgerufen wurden.
    Der Benutzer wird gebeten, ein Haus auszuwählen.
    """
    haeuser = get_haeuser()

    if not haeuser:
        print("Es sind keine Häuser in der Datenbank vorhanden.")
        return None

    print("Bitte wählen Sie ein Haus aus:")
    for idx, haus in enumerate(haeuser, start=1):
        print(f"{idx}. {haus[1]} {haus[2]} ({haus[3]} {haus[4]})")  # Strasse Hausnummer PLZ Stadt

    while True:
        try:
            haus_choice = int(input("Bitte Hausnummer eingeben: "))
            if 1 <= haus_choice <= len(haeuser):
                return haeuser[haus_choice - 1][0]  # HausID
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

def show_wohnung_options(haus_id):
    """
    Zeigt dem Benutzer eine Liste von Wohnungen an, die zum gewählten Haus gehören.
    Der Benutzer wird gebeten, eine Wohnung auszuwählen.
    """
    wohnungen = get_wohnungen_pro_haus(haus_id)

    if not wohnungen:
        print(f"Es sind keine Wohnungen für Haus {haus_id} vorhanden.")
        return None

    print(f"Bitte wählen Sie eine Wohnung aus (HausID: {haus_id}):")
    for idx, wohnung in enumerate(wohnungen, start=1):
        print(f"{idx}. Etage: {wohnung[1]}, Lage: {wohnung[2]}")  # Etage, Lage

    while True:
        try:
            wohnung_choice = int(input("Bitte Wohnung Nummer eingeben: "))
            if 1 <= wohnung_choice <= len(wohnungen):
                return wohnungen[wohnung_choice - 1][0]  # EinheitID der Wohnung
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

def show_raum_details():
    """
    Fragt den Benutzer nach den Details des Raums, den er anlegen möchte.
    """
    groesse = input("Aktuelle Größe des Raumes (in m²): ")
    try:
        groesse = float(groesse)
    except ValueError:
        print("Ungültige Größe. Bitte eine Zahl eingeben.")
        return None

    anteil_nebenkosten = input("Effektiver Anteil an den Nebenkosten (%): ")
    try:
        anteil_nebenkosten = float(anteil_nebenkosten)
    except ValueError:
        print("Ungültiger Anteil. Bitte eine Zahl eingeben.")
        return None

    return groesse, anteil_nebenkosten

def create_raum_dialog():
    """
    Der Hauptdialog zur Erstellung eines Raums, der den Benutzer durch die Auswahl der Wohnung und die Eingabe von Rauminformationen führt.
    """
    print("Erstellen eines neuen Raumes:\n")
    
    # 1. Haus auswählen
    haus_id = show_haus_options()
    if not haus_id:
        print("Fehler: Kein Haus ausgewählt. Abbruch.")
        return
    
    # 2. Wohnung im ausgewählten Haus auswählen
    wohnung_id = show_wohnung_options(haus_id)
    if not wohnung_id:
        print("Fehler: Keine Wohnung ausgewählt. Abbruch.")
        return

    # 3. Raum Details (Größe und Anteil Nebenkosten)
    raum_details = show_raum_details()
    if not raum_details:
        print("Fehler: Ungültige Rauminformationen. Abbruch.")
        return

    groesse, anteil_nebenkosten = raum_details

    # Hier kannst du den Raum jetzt in der Datenbank anlegen
    print(f"\nRaum angelegt:\nWohnungID: {wohnung_id}, Größe: {groesse} m², Anteil Nebenkosten: {anteil_nebenkosten}%")

    # Nachfolgend kannst du die Funktion für die Raumerstellung in der Datenbank aufrufen (falls nötig)
    # db.create_raum(wohnung_id, groesse, anteil_nebenkosten)

def main():
    """
    Der Einstiegspunkt für das Dialog-Modul.
    """
    while True:
        print("\nWillkommen zum Immobilien-Management-System!")
        print("1. Raum erstellen")
        print("2. Beenden")
        
        choice = input("Bitte eine Auswahl treffen: ")

        if choice == "1":
            create_raum_dialog()
        elif choice == "2":
            print("Beenden...")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()
