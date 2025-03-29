from hausverwaltung.db import get_wohnungen_pro_haus, get_haeuser, get_raeume, get_raeume_per_wohnung, get_alle_mieter, get_wohnungen 

from hausverwaltung.config import load_config

def list_haus():
    """
    Listet alle Häuser aus der Datenbank auf.
    """
    return list_auswahl(get_haeuser, print_haus, "Haus")

def list_wohnung(haus_id=None):
    """
    Listet alle Wohnungen auf. Falls eine Haus-ID angegeben wird, 
    werden nur die Wohnungen dieses Hauses aufgelistet.

    :param haus_id: Optionale ID eines Hauses, um die Wohnungen dieses Hauses zu filtern.
    """
    # Wenn eine haus_id angegeben wird, nutzen wir get_wohnungen_pro_haus(haus_id)
    if haus_id:
        get_methode = lambda: get_wohnungen_pro_haus(haus_id)
    else:
        get_methode = get_wohnungen  # Wenn keine haus_id, dann alle Wohnungen

    return list_auswahl(get_methode, print_wohnung, "Wohnung")



def list_alle_mieter():
    """
    Listet alle Mieter aus der Datenbank auf.
    """
    return list_auswahl(get_alle_mieter, print_mieter, "Mieter")

 
def get_mieter_auswahl():
    """
    Lässt den Benutzer einen Mieter aus der Datenbank auswählen.
    
    :return: Der ausgewählte Mieter oder None, falls keine Auswahl getroffen wurde.
    """
    return get_auswahl(get_alle_mieter, print_mieter, "Mieter")
    
def get_haus_option():
    """
    Lässt den Benutzer ein Haus aus der Datenbank auswählen.
    
    :return: Das ausgewählte Haus oder None, falls keine Auswahl getroffen wurde.
    """
    return get_auswahl(get_haeuser, print_haus, "Haus")

def get_wohnung_option(haus_id):
    """
    Lässt den Benutzer eine Wohnung aus einem bestimmten Haus auswählen.
    
    :param haus_id: ID des Hauses, dessen Wohnungen angezeigt werden sollen.
    :return: Die ausgewählte Wohnung oder None, falls keine Auswahl getroffen wurde.
    """

    return get_auswahl(lambda: get_wohnungen_pro_haus(haus_id), print_wohnung, "Wohnung")


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
    haus = get_haus_option()
    if not haus:
        print("Fehler: Kein Haus ausgewählt. Abbruch.")
        return
    
    # 2. Wohnung im ausgewählten Haus auswählen
    wohnung_id = get_wohnung_option(haus.haus_id)
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


def print_mieter(mieter):
    """
    Gibt die Daten eines einzelnen Mieters formatiert aus.
    """
    print(f"{mieter[1]} {mieter[2]} {mieter[3]}") 

def print_wohnung(wohnung):
    """
    Gibt die Daten einer einzelnen Wohnung formatiert aus.
    """
    print(f"WohnungID: {wohnung[0]}, Etage: {wohnung[1]}, Lage: {wohnung[2]}")  # EinheitID, Etage, Lage

def print_raum(raum):
    """
    Gibt die Daten eines einzelnen Raums formatiert aus.
    """
    print(f"RaumID: {raum[0]}, WohnungID: {raum[1]}, TypID: {raum[2]}, Größe: {raum[3]} m², Anteil Nebenkosten: {raum[4]}%")  # RaumID, WohnungID, TypID, Groesse, AnteilNebenkosten

def print_haus(haus):
    """
    Gibt die Daten eines einzelnen Hauses formatiert aus.
    """
    print(f"HausID: {haus[0]}, Straße: {haus[1]}, Hausnummer: {haus[2]}, PLZ: {haus[3]}, Stadt: {haus[4]}")  # HausID, Strasse, Hausnummer, PLZ, Stadt

def print_mietvertrag(mietvertrag):
    """
    Gibt die Daten eines einzelnen Mietvertrags formatiert aus.
    """
    print(f"MietvertragID: {mietvertrag[0]}, MieterID: {mietvertrag[1]}, WohnungID: {mietvertrag[2]}, Mietbeginn: {mietvertrag[3]}, Mietende: {mietvertrag[4]}")  # MietvertragID, MieterID, WohnungID, Mietbeginn, Mietende    



def list_auswahl(get_methode, print_methode, objekt_typ="Eintrag"):
    """
    Listet die Einträge aus der get_methode auf.
    
    :param get_methode: Funktion, die die Liste der Einträge liefert.
    :param print_methode: Funktion, die einen einzelnen Eintrag ausgibt.
    :param objekt_typ: Name des Objekttyps für die Benutzerausgabe.
    """
    eintraege = get_methode()

    if not eintraege:
        print(f"Es sind keine {objekt_typ}e in der Datenbank vorhanden.")
        return

    print(f"Verfügbare {objekt_typ}e:")
    for idx, eintrag in enumerate(eintraege, start=1):
        print(f"{idx}.", end=" ")
        print_methode(eintrag)


def get_auswahl(get_methode, print_methode, objekt_typ="Eintrag"):
    """
    Fragt den Benutzer nach einer Auswahl aus einer Liste von Einträgen.
    
    :param get_methode: Funktion, die die Liste der Einträge liefert.
    :param print_methode: Funktion, die einen einzelnen Eintrag ausgibt.
    :param objekt_typ: Name des Objekttyps für die Benutzerausgabe.
    :return: Der ausgewählte Datensatz oder None, falls keine Auswahl getroffen wurde.
    """
    eintraege = get_methode()

    if not eintraege:
        print(f"Es sind keine {objekt_typ}e in der Datenbank vorhanden.")
        return None

    list_auswahl(get_methode, print_methode, objekt_typ)

    while True:
        try:
            auswahl = int(input(f"Bitte {objekt_typ}-Nummer eingeben: "))
            if 1 <= auswahl <= len(eintraege):
                return eintraege[auswahl - 1]
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")



if __name__ == "__main__":
    main()
