import pyodbc
from hausverwaltung.config import load_config

from hausverwaltung.models import Mietvertrag, Mieter, Wohnung, Haus, Raum

def get_database_config():
    """
    Lädt die Datenbank-Konfigurationsdaten aus der config.ini.
    """
    config = load_config()
    db_config = config["database"]
    
    return {
        "server": db_config.get("server", "localhost"),
        "database": db_config.get("database", ""),
        "user": db_config.get("user", ""),
        "password": db_config.get("password", "")
    }

def get_connection(): 
    """
    Stellt eine Verbindung zur SQL Server-Datenbank her, basierend auf den Daten aus der config.ini.
    """
    db_config = get_database_config()
    
    connection_string = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"Trusted_Connection=yes;"  # Aktiviert Windows Authentication
    )
    
    try:
        connection = pyodbc.connect(connection_string)
        # print("Datenbankverbindung erfolgreich hergestellt!")
        return connection
    except pyodbc.Error as e:
        print(f"Fehler beim Verbinden zur Datenbank: {e}")
        return None



def get_wohnungen():
    """
    Gibt eine Liste aller Wohnungen in der Datenbank zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT WohnungID, HausID, Etage, LageImHaus FROM Wohnung")
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_wohnungen_pro_haus(haus_id):
    """
    Gibt eine Liste von Wohnungen zurück, die zu einem bestimmten Haus gehören.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT WohnungID, Etage, LageImHaus FROM Wohnung WHERE HausID = ?", (haus_id,))
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_haeuser():
    """
    Gibt eine Liste aller Häuser zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT HausID, Strasse, Hausnummer, PLZ, Stadt FROM Haus")
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_alle_mieter():
    """
    Gibt eine Liste aller Mieter zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT MieterID, Anrede, Vorname, Nachname, Geschlecht, KontaktInfo FROM Mieter")
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_raeume():
    """
    Gibt eine Liste aller Räume zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT RaumID, EinheitID, TypID, Groesse, AnteilNebenkosten FROM Raum")
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_raeume_per_wohnung(wohnung_id):
    """
    Gibt eine Liste der Räume zurück, die zu einer bestimmten Wohnung gehören.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT RaumID, WohnungID, TypID, Groesse, AnteilNebenkosten FROM Raum WHERE WohnungID = ?", (wohnung_id,))
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_mietvertraege_per_haus(haus_id):
    """
    Gibt eine Liste aller Mietverträge für Wohnungen in einem bestimmten Haus zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT mv.MietverhaeltnisID, mv.MieterID, mv.Mietbeginn, mv.Mietende
            FROM Mietvertrag mv
            INNER JOIN Wohnung w ON mv.EinheitID = w.EinheitID
            WHERE w.HausID = ?
        """, (haus_id,))
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_mietvertraege_per_mieter(mieter_id):
    """
    Gibt eine Liste aller Mietverträge eines bestimmten Mieters zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT mv.MietverhaeltnisID, mv.EinheitID, mv.Mietbeginn, mv.Mietende
            FROM Mietvertrag mv
            WHERE mv.MieterID = ?
        """, (mieter_id,))
        result = cursor.fetchall()
        connection.close()
        return result
    return []

def get_mietvertrag(mietvertrag_id):
    """
    Gibt die Daten eines Mietvertrags anhand seiner ID zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT MietvertragID, MieterID, WohnungID, Mietbeginn, Mietende FROM Mietvertrag WHERE MietverhaeltnisID = ?", (mietvertrag_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None

def get_mieter(mieter_id):
    """
    Gibt die Daten eines Mieters anhand seiner ID zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Anrede, Vorname, Name, Geschlecht, KontaktInfo FROM Mieter WHERE MieterID = ?", (mieter_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None

def get_wohnung(wohnung_id):
    """
    Gibt die Daten einer Wohnung anhand ihrer ID zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT WohnungId, HausID, Etage, LageImHaus FROM Wohnung WHERE WohnungID = ?", (wohnung_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None

def get_haus(haus_id):
    """
    Gibt die Daten eines Hauses anhand seiner ID zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT HausID, Strasse, Hausnummer, PLZ, Stadt FROM Haus WHERE HausID = ?", (haus_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None

def get_raum(raum_id):
    """
    Gibt die Daten eines Raums anhand seiner ID zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT RaumID, WohnungID, TypID, Groesse, NebenkostenGroesse FROM Raum WHERE RaumID = ?", (raum_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None



def add_mieter_to_db(vorname, nachname):
    """Fügt einen neuen Mieter in die Datenbank hinzu."""
    
    # Erhalte die DB-Verbindung
    connection = get_connection()
    if connection is None:
        return
    
    cursor = connection.cursor()

    # SQL-Statement, um den neuen Mieter hinzuzufügen
    sql = """
            INSERT INTO Mieter (Vorname, Nachname)
            OUTPUT INSERTED.MieterID
            VALUES (?, ?);
    """
    
    try:
        # Ausführen des SQL-Statements mit den übergebenen Parametern
        cursor.execute(sql, (vorname, nachname))
              
        # Änderungen speichern (commit)
        result=cursor.fetchone()
        mieter_id = result.MieterID  # Holt sich die ID der eingefügten Zeile
        
        cursor.commit()
        print(f"Mieter {vorname} {nachname} (MieterID: {mieter_id}) wurde erfolgreich hinzugefügt.")    
    
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Mieters: {e}")
    
    finally:
        # Cursor und Verbindung schließen
        cursor.close()
        connection.close()

def get_kostenstellen():
    """
    Gibt eine Liste aller Kostenstellen zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT KostenstelleID, Name FROM Kostenstelle")
        result = cursor.fetchall()
        connection.close()
        return result
    return []  

def get_kosten_pro_kostenstelle(kostenstelle_id):
    """
    Gibt die Kosten für eine bestimmte Kostenstelle zurück.
    """
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Betrag FROM Kosten WHERE KostenstelleID = ?", (kostenstelle_id,))
        result = cursor.fetchone()
        connection.close()
        return result
    return None    
