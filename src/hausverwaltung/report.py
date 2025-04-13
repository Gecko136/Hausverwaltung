from hausverwaltung.models import Mietvertrag, Forderung, Haus, Wohnung, Mieter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from decimal import Decimal
from datetime import datetime
import re

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def create_report(mietvertrag_id, jahr):
    # Prüfen, ob es Forderungen für den Mietvertrag in diesem Jahr gibt
    try:
        mietvertrag = Mietvertrag.objects.get(id=mietvertrag_id)
    except Mietvertrag.DoesNotExist:
        print(f"Mietvertrag mit ID {mietvertrag_id} existiert nicht.")
        return

    # Suche die Forderungen, die zu diesem Mietvertrag gehören und für das angegebene Jahr relevant sind
    forderungen = Forderung.objects.filter(mietvertrag=mietvertrag, berechnungsdatum__year=jahr)

    if not forderungen.exists():
        print(f"Es gibt keine Forderungen für Mietvertrag {mietvertrag_id} im Jahr {jahr}.")
        return

    # Erstelle den Report
    mieter = mietvertrag.mieter
    wohnung = mietvertrag.wohnung
    haus = wohnung.haus

    # Erstelle den Dateinamen
    filename = f"nebenkostenabrechnung_{jahr}_{mieter.id}_{mieter.vorname}_{mieter.nachname}"
    filename = sanitize_filename(filename)+".pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Titel
    title = Paragraph(f"<b>Nebenkostenabrechnung für das Jahr {jahr}</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Mieter-Informationen
    mieter_info = (
        f"<b>Mieter:</b> {mieter.vorname} {mieter.nachname}<br/>"
        f"<b>Adresse:</b> {mieter.vorname} {mieter.nachname}<br/>"
        f"{wohnung.etage}, {haus.strasse}, {haus.plz} {haus.stadt}"
    )
    elements.append(Paragraph(mieter_info, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Abrechnungszeitraum
    abrechnungszeitraum = f"<b>Abrechnungszeitraum:</b> 01.01.{jahr} - 31.12.{jahr}"
    mietzeitraum  = f"<b>Mietzeitraum:</b>" + mietvertrag.mietbeginn.strftime("%d.%m.%Y") + " bis " + (mietvertrag.mietende.strftime("%d.%m.%Y") if mietvertrag.mietende else f"31.12.{jahr}")
    elements.append(Paragraph(abrechnungszeitraum, styles["Normal"]))
    elements.append(Paragraph(mietzeitraum, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Tabelle mit Nebenkosten
    table_data = [["Kostenart", "Gesamtkosten", "Flächenschlüssel", "Mietschlüssel", "Ihr Anteil"]]
    total_kosten = Decimal(0)

    for forderung in forderungen:
        # Berechnung des Umlageschlüssels
        umlageschluesselQM = f"{Decimal(forderung.umlageschluesselQM)*100:.2f}%" if forderung.umlageschluesselQM != 1 else ""
        mieteranteil = Decimal(forderung.anteilbetrag)
        total_kosten += Decimal(mieteranteil)

        umlagefaktormiete = Decimal(forderung.umlageschluesselMietdauer) * 100;  # Umlageschlüssel Mietdauer in Prozent
        umlagemiete = f"{umlagefaktormiete:.2f}%({forderung.miettage}/{forderung.tageimjahr})" if umlagefaktormiete != 100 else ""

        # Kosten in die Tabelle einfügen
        table_data.append([ 
            f"{forderung.bezeichnung}" + (f"({forderung.split_anteil}%)" if forderung.split_anteil != 100 else "") ,  # Kostenart mit Split-Anteil
            f"{Decimal(forderung.gesamtbetrag):.2f} €",  # Gesamtkosten als Decimal formatiert
            umlageschluesselQM,  # Umlageschlüssel als Prozent
            umlagemiete,  
            f"{mieteranteil:.2f} €"  # Mieteranteil als Decimal formatiert
        ])

    # Tabelle formatieren
    table = Table(table_data, colWidths=[120, 90, 90, 100, 60 ] ) 
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Gesamtkosten & Vorauszahlungen
    vorauszahlungen = Decimal(200.00)  # Temporärer Wert für Vorauszahlungen als Decimal
    gesamtkosten = f"<b>✅ Gesamtkostenanteil:</b> {total_kosten:.2f} €"
    elements.append(Paragraph(gesamtkosten, styles["Normal"]))

    vorauszahlungen_text = f"<b>✅ Ihre geleisteten Vorauszahlungen:</b> {vorauszahlungen:.2f} €"
    elements.append(Paragraph(vorauszahlungen_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Nachzahlung oder Guthaben
    nachzahlung = total_kosten - vorauszahlungen
    if nachzahlung > 0:
        nachzahlung_text = f"<b>🔴 Nachzahlung zu Ihren Lasten:</b> {nachzahlung:.2f} €"
    else:
        nachzahlung_text = f"<b>🟢 Ihr Guthaben:</b> {abs(nachzahlung):.2f} € (wird Ihnen erstattet)"
    elements.append(Paragraph(nachzahlung_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Zahlungsinformationen
    zahlung_info = (
        "<b>📌 Zahlungsinformation:</b><br/>"
        "Bitte überweisen Sie den Nachzahlungsbetrag bis spätestens 30.04.{0} auf folgendes Konto:<br/>"
        "<b>IBAN:</b> DE12 3456 7890 1234 5678 90<br/>"
        "<b>BIC:</b> XYZBANK123<br/>"
        "<b>Verwendungszweck:</b> Nebenkosten {0} – {1} {2}"
    ).format(jahr + 1, mietvertrag.mieter.vorname, mietvertrag.mieter.nachname)
    elements.append(Paragraph(zahlung_info, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Fußnote
    footnote = "<i>Bei Positionen mit einem Prozentsatz wird nur der anteilige Betrag berechnet.</i>"
    elements.append(Paragraph(footnote, styles["Normal"]))

    # PDF erzeugen
    doc.build(elements)

    print(f"Report für Mietvertrag {mietvertrag_id} im Jahr {jahr} wurde als {filename} gespeichert.")




def create_reports_for_all_mietvertraege(jahr):
    """Erstellt Nebenkostenabrechnungen für alle aktiven Mietverträge im angegebenen Jahr."""
    mietvertraege = Mietvertrag.objects.filter(
        mietbeginn__lte=datetime(jahr, 12, 31),
        mietende__isnull=True  # Mietende ist NULL (noch aktiv)
    ) | Mietvertrag.objects.filter(
        mietbeginn__lte=datetime(jahr, 12, 31),
        mietende__gte=datetime(jahr, 1, 1)  # Mietende ist nach dem 1.1. des Jahres
    )

    if not mietvertraege.exists():
        print(f"⚠️ Keine aktiven Mietverträge im Jahr {jahr} gefunden.")
        return

    print(f"📄 Generiere Nebenkostenabrechnungen für {mietvertraege.count()} Mietverträge...")
    
    for mietvertrag in mietvertraege:
        create_report(mietvertrag.id, jahr)

    print(f"✅ Alle Nebenkostenabrechnungen für {jahr} wurden erstellt.")