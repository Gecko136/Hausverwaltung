from datetime import date

from hausverwaltung.models import Nebenkostenabrechnung, Mietvertrag, Mieter, Wohnung, Haus, Kostenstelle, Kosten, Raum
from hausverwaltung.mietvertrag_repository import MietvertragRepository
from hausverwaltung.db import get_kostenstellen, get_kosten_pro_kostenstelle

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

def get_test_nebenkosten() -> Nebenkostenabrechnung:
    # Beispielwerte für Mieter, Wohnung, Haus, etc.
    mieter = Mieter(mieter_id=1, anrede='Herr', vorname='Max', nachname='Mustermann')

    raeume = [ Raum(raum_id=1, typ_id=1, groesse=20, nebenkosten_groesse=20) ]
 
    wohnung = Wohnung(wohnung_id=1, etage= "Parterre", lage_im_haus='1. OG', groesse=80, nebenkosten_groesse=80, raeume=raeume)
    haus = Haus(haus_id=1, strasse='Musterstraße', hausnummer=1, plz = '22339', stadt="Hamburg", groesse=1000, nebenkosten_groesse=1000, wohnungen= [wohnung])
    
    # Beispielhafte Kostenstellen und Kosten
    kostenstelle = Kostenstelle(kostenstelle_id=1, name='Heizung')
    kosten_details = [
        Kosten(kosten_id = 1, kostenstelle= kostenstelle, betrag=120),
        Kosten(kosten_id = 2, kostenstelle= kostenstelle, betrag=80),
        Kosten(kosten_id = 3, kostenstelle= kostenstelle, betrag=100),
    ]
    
    # Gesamtkosten berechnen
    gesamtkosten = sum(kosten.betrag for kosten in kosten_details)
    
    # Beispiel-Mietvertrag
    mietvertrag = Mietvertrag(
        mietvertrag_id=1,
        mieter=mieter,
        wohnung=wohnung,
        haus=haus,
        startdatum=date(2024, 1, 1),
        enddatum=date(2024, 12, 31)
    )
    
    # Nebenkostenabrechnung erstellen
    abrechnung = Nebenkostenabrechnung(
        jahr=2023,
        mietvertrag=mietvertrag,
        mieter=mieter,
        wohnung=wohnung,
        haus=haus,
        kosten_details=kosten_details,
        gesamtkosten=gesamtkosten,
        anzahl_wochentage=365,
        vorauszahlungen=420,  # Beispielhafte Vorauszahlungen
        nachzahlung=gesamtkosten - 420  # Differenz zwischen Gesamtkosten und Vorauszahlungen
    )
    
    return abrechnung