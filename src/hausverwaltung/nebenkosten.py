from models import Nebenkostenabrechnung
from mietvertrag_repository import MietvertragRepository
from db import get_kostenstellen, get_kosten_pro_kostenstelle

def berechne_nebenkosten(mietvertrag_id, jahr, vorauszahlungen):
    """
    Berechnet die Nebenkosten für einen gegebenen Mietvertrag in einem bestimmten Jahr.
    """
    # Mietvertrag über das Repository holen
    mietvertrag_repo = MietvertragRepository()
    mietvertrag = mietvertrag_repo.get_mietvertrag_by_id(mietvertrag_id)
    
    # Zugehörige Wohnung und Haus sind bereits im Mietvertrag-Objekt enthalten
    wohnung = mietvertrag.wohnung
    haus = mietvertrag.haus
    
    # Quadratmeter der Wohnung und Nebenkosten-Größe der Wohnung
    wohnung_qm = wohnung.groesse
    wohnung_nebenkosten_qm = wohnung.nebenkosten_groesse
    
    # Quadratmeter des gesamten Hauses und Nebenkosten-Größe des Hauses
    haus_qm = haus.groesse
    haus_nebenkosten_qm = haus.nebenkosten_groesse
    
    # Anteil der Wohnung am Haus (in Bezug auf die Nebenkosten)
    wohnungs_anteil = wohnung_nebenkosten_qm / haus_nebenkosten_qm if haus_nebenkosten_qm > 0 else 0
    
    # Mietzeitraum im Jahr berechnen
    mietbeginn = max(mietvertrag.startdatum, f"{jahr}-01-01")
    mietende = min(mietvertrag.enddatum, f"{jahr}-12-31") if mietvertrag.enddatum else f"{jahr}-12-31"
    miettage = (mietende - mietbeginn).days + 1
    anteil_am_jahr = miettage / 365
    
    # Nebenkosten pro Kostenstelle berechnen
    kostenstellen = get_kostenstellen(haus.haus_id, jahr)
    kosten_details = []
    gesamtkosten = 0
    
    for kostenstelle in kostenstellen:
        gesamtkosten_kostenstelle = get_kosten_pro_kostenstelle(kostenstelle['KostenstelleID'])
        mietanteil = gesamtkosten_kostenstelle * wohnungs_anteil * anteil_am_jahr
        kosten_details.append({
            'Kostenstelle': kostenstelle['Name'],
            'Gesamtkosten': gesamtkosten_kostenstelle,
            'Mieteranteil': mietanteil
        })
        gesamtkosten += mietanteil
    
    # Berechnung der Nachzahlung oder Rückerstattung
    nachzahlung = gesamtkosten - vorauszahlungen

    # Nebenkostenabrechnung-Objekt erstellen
    abrechnung = Nebenkostenabrechnung(
        jahr=jahr,
        mietvertrag=mietvertrag,  # Hier wird der Mietvertrag als Ganzes übergeben
        mieter=mietvertrag.mieter,  # Mieter aus dem Mietvertrag
        wohnung=wohnung,  # Wohnung-Objekt aus dem Mietvertrag
        haus=haus,  # Haus-Objekt aus dem Mietvertrag
        kosten_details=kosten_details,  # Auflistung der Kosten pro Kostenstelle
        gesamtkosten=gesamtkosten,  # Gesamtkosten des Mieters
        anzahl_wochentage=miettage,  # Anzahl der Wochentage im Abrechnungsjahr
        vorauszahlungen=vorauszahlungen,  # Vorauszahlungen des Mieters
        nachzahlung=nachzahlung  # Berechnete Nachzahlung oder Rückerstattung
    )
    
    return abrechnung
