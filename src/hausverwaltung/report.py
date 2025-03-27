from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from datetime import datetime

def create_pdf_nebenkosten_report(nebenkosten, filename="nebenkostenabrechnung.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Titel
    title = Paragraph("<b>Nebenkostenabrechnung für das Jahr {}<b>".format(nebenkosten.jahr), styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Mieter-Informationen
    mieter_info = (
        f"<b>Mieter:</b> {nebenkosten.mieter.vorname} {nebenkosten.mieter.nachname}<br/>"
        f"<b>Adresse:</b> {nebenkosten.wohnung.lage_im_haus}, {nebenkosten.haus.strasse}, {nebenkosten.haus.plz} {nebenkosten.haus.stadt}"
    )
    elements.append(Paragraph(mieter_info, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Abrechnungszeitraum
    abrechnungszeitraum = f"<b>Abrechnungszeitraum:</b> {nebenkosten.mietvertrag.startdatum.strftime('%d.%m.%Y')} - {nebenkosten.mietvertrag.enddatum.strftime('%d.%m.%Y')}"
    elements.append(Paragraph(abrechnungszeitraum, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Tabelle mit Nebenkosten
    table_data = [["Kostenart", "Gesamtkosten Haus", "Umlageschlüssel", "Ihr Anteil"]]
    for kosten in nebenkosten.kosten_details:
        table_data.append([
            kosten.kostenstelle,
            f"{kosten.gesamtkosten:.2f} €",
            f"{kosten.umlageschluessel:.2%}",
            f"{kosten.mieteranteil:.2f} €"
        ])
    
    # Tabelle formatieren
    table = Table(table_data, colWidths=[150, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Gesamtkosten & Vorauszahlungen
    gesamtkosten = f"<b>✅ Gesamtkostenanteil:</b> {nebenkosten.gesamtkosten:.2f} €"
    vorauszahlungen = f"<b>✅ Ihre geleisteten Vorauszahlungen:</b> {nebenkosten.vorauszahlungen:.2f} €"
    elements.append(Paragraph(gesamtkosten, styles["Normal"]))
    elements.append(Paragraph(vorauszahlungen, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Nachzahlung oder Guthaben
    if nebenkosten.nachzahlung > 0:
        nachzahlung = f"<b>🔴 Nachzahlung zu Ihren Lasten:</b> {nebenkosten.nachzahlung:.2f} €"
    else:
        nachzahlung = f"<b>🟢 Ihr Guthaben:</b> {abs(nebenkosten.nachzahlung):.2f} € (wird Ihnen erstattet)"
    elements.append(Paragraph(nachzahlung, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Zahlungsinformationen
    zahlung_info = (
        "<b>📌 Zahlungsinformation:</b><br/>"
        "Bitte überweisen Sie den Nachzahlungsbetrag bis spätestens 30.04.{} auf folgendes Konto:<br/>"
        "<b>IBAN:</b> DE12 3456 7890 1234 5678 90<br/>"
        "<b>BIC:</b> XYZBANK123<br/>"
        "<b>Verwendungszweck:</b> Nebenkosten {} – {} {}"
    ).format(nebenkosten.jahr + 1, nebenkosten.jahr, nebenkosten.mieter.vorname, nebenkosten.mieter.nachname)
    elements.append(Paragraph(zahlung_info, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Hinweise
    hinweise = (
        "<b>ℹ️ Wichtige Hinweise:</b><br/>"
        "Der Umlageschlüssel berechnet sich aus dem Verhältnis Ihrer Wohnfläche zur Gesamtwohnfläche des Hauses.<br/>"
        "Etwaige Einwände oder Rückfragen zur Abrechnung teilen Sie uns bitte innerhalb von 14 Tagen schriftlich mit.<br/>"
        "Diese Abrechnung erfolgt gemäß §§ 556 ff. BGB."
    )
    elements.append(Paragraph(hinweise, styles["Normal"]))

    # PDF erzeugen
    doc.build(elements)
