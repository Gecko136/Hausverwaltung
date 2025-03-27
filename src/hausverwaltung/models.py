from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Raum:
    raum_id: int
    typ_id: int
    groesse: float  # tatsächliche Größe des Raums
    nebenkosten_groesse: float  # Größe des Raums, die für Nebenkosten relevant ist

@dataclass
class Wohnung:
    einheit_id: int
    etage: int
    lage_im_haus: str
    groesse: float  # tatsächliche Quadratmeter der Wohnung
    nebenkosten_groesse: float  # Quadratmeter der Wohnung, die für Nebenkosten relevant sind
    Raeume: List[Raum]  # Liste von Raum-Objekten

@dataclass
class Haus:
    haus_id: int
    strasse: str
    hausnummer: str
    plz: str
    stadt: str
    groesse: float  # tatsächliche Quadratmeter des Hauses
    nebenkosten_groesse: float  # Quadratmeter des Hauses, die für Nebenkosten relevant sind
    wohnungen: List[Wohnung]  # Liste von Wohnung-Objekten

@dataclass
class Mieter:
    mieter_id: int
    anrede: str
    vorname: str
    nachname: str

@dataclass
class Mietvertrag:
    mietvertrag_id: int
    mieter: Mieter
    wohnung: Wohnung
    haus: Haus
    startdatum: str
    enddatum: str

@dataclass
class Kostenstelle:
    kostenstelle_id: int
    name: str

@dataclass
class Kosten:
    kosten_id: int
    kostenstelle: Kostenstelle
    betrag: float

@dataclass
class Nebenkostenabrechnung:
    jahr: int
    mietvertrag: Mietvertrag
    mieter: Mieter
    wohnung: Wohnung
    haus: Haus
    kosten_details: List[Kosten]
    gesamtkosten: float
    anzahl_wochentage: int  # Anzahl der Tage im Abrechnungsjahr
    vorauszahlungen: float
    nachzahlung: float

