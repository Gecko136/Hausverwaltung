# mietvertrag_repository.py

from db import get_mietvertrag, get_mieter, get_wohnungen_pro_haus, get_haus, get_raeume_per_wohnung, get_wohnung
from models import Mietvertrag, Mieter, Wohnung, Haus, Raum

class MietvertragRepository:
    
    def get_mietvertrag_by_id(self, mietvertrag_id: int) -> Mietvertrag:
        """Holt einen Mietvertrag und verwandelt ihn in ein Mietvertrag-Objekt."""
        
        # Holen der rohen Mietvertragsdaten aus der DB
        mietvertrag_data = get_mietvertrag(mietvertrag_id)
        if not mietvertrag_data:
            raise ValueError(f"Mietvertrag mit ID {mietvertrag_id} nicht gefunden.")
        
        mietvertrag_id, mieter_id, wohnung_id, startdatum, enddatum = mietvertrag_data
        
        # Holen der Wohnung
        wohnung_data = get_wohnung(wohnung_id)
        if not wohnung_data:
            raise ValueError(f"Wohnung mit ID {wohnung_id} nicht gefunden.")
        
        wohnung_id, haus_id, etage, lage_im_haus = wohnung_data

        # Holen des Mieters
        mieter_data = get_mieter(mieter_id)
        if not mieter_data:
            raise ValueError(f"Mieter mit ID {mieter_id} nicht gefunden.")
        
        mieter_id, anrede, vorname, nachname = mieter_data
        mieter = Mieter(mieter_id, anrede, vorname, nachname)
        
        # Holen des Hauses zur Wohnung
        haus_data = get_haus(haus_id)
        if not haus_data:
            raise ValueError(f"Haus mit ID {haus_id} nicht gefunden.")
        
        haus_id, strasse, hausnummer, plz, stadt = haus_data
        haus = Haus(haus_id, strasse, hausnummer, plz, stadt, 0, 0, [])  # Quadratmeterzahl initial auf 0 setzen

        # Holen aller Wohnungen im Haus
        wohnungen_data = get_wohnungen_pro_haus(haus_id)
        if not wohnungen_data:
            raise ValueError(f"Keine Wohnungen im Haus mit ID {haus_id} gefunden.")
        
        wohnungen = []
        gesamt_groesse_haus = 0  # Variable für die tatsächliche Quadratmeter des Hauses
        gesamt_nebenkosten_groesse_haus = 0  # Variable für Nebenkosten-Größe des Hauses
        for wohnung_data in wohnungen_data:
            wohnung_id, haus_id, etage, lage_im_haus = wohnung_data
            raeume_data = get_raeume_per_wohnung(wohnung_id)
            raeume = []
            gesamt_groesse_wohnung = 0  # Variable für die tatsächliche Quadratmeter der Wohnung
            gesamt_nebenkosten_groesse_wohnung = 0  # Variable für Nebenkosten-Größe der Wohnung
            for raum_data in raeume_data:
                raum_id, typ_id, groesse, nebenkosten_groesse = raum_data
                raum = Raum(raum_id, typ_id, groesse, nebenkosten_groesse)
                raeume.append(raum)
                gesamt_groesse_wohnung += groesse  # Quadratmeter der Wohnung berechnen
                gesamt_nebenkosten_groesse_wohnung += nebenkosten_groesse  # Nebenkosten-Größe der Wohnung berechnen

            # Wohnung wird mit den berechneten Größen gefüllt
            wohnung = Wohnung(wohnung_id, etage, lage_im_haus, gesamt_groesse_wohnung, gesamt_nebenkosten_groesse_wohnung, raeume)

            # Hinzufügen der Wohnung zum Haus
            haus.wohnungen.append(wohnung)

            # Addiere die Quadratmeter der Wohnung zum Gesamt-Groesse des Hauses
            gesamt_groesse_haus += gesamt_groesse_wohnung
            gesamt_nebenkosten_groesse_haus += gesamt_nebenkosten_groesse_wohnung

        # Setzen der berechneten Größen des Hauses
        haus.groesse = gesamt_groesse_haus
        haus.nebenkosten_groesse = gesamt_nebenkosten_groesse_haus

        # Rückgabe des vollständig gefüllten Mietvertrags
        return Mietvertrag(mietvertrag_id, mieter, wohnung, haus, startdatum, enddatum)
