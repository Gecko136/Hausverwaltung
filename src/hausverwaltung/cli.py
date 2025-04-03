import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hausverwaltung.settings")
django.setup()

import click
from django.db import IntegrityError
from hausverwaltung.models import Mieter, Haus, Wohnung, Raum, Mietvertrag, Komplex, Kostenstelle, Kostensplit, Komplexteile, Forderung


@click.group()
def cli():
    """Hausverwaltung CLI"""
    pass


# Add Commands
@cli.group()
def add():
    """Füge neue Datensätze hinzu"""
    pass


@add.command('mieter')
@click.option('--vorname', prompt='Vorname', help='Vorname des Mieters')
@click.option('--nachname', prompt='Nachname', help='Nachname des Mieters')
@click.option('--kontakt_info', prompt='Kontaktinfo', help='Kontaktinformationen des Mieters')
def add_mieter(vorname, nachname, kontakt_info):
    """Fügt einen neuen Mieter hinzu"""
    try:
        mieter = Mieter.objects.create(vorname=vorname, nachname=nachname, kontakt_info=kontakt_info)
        click.echo(f"Mieter {mieter.vorname} {mieter.nachname} erfolgreich hinzugefügt.")
    except IntegrityError:
        click.echo(f"Fehler beim Hinzufügen des Mieters {vorname} {nachname}.")


@add.command('haus')
@click.option('--strasse', prompt='Straße', help='Straße des Hauses')
@click.option('--hausnummer', prompt='Hausnummer', help='Hausnummer des Hauses')
@click.option('--plz', prompt='Postleitzahl', help='Postleitzahl des Hauses')
@click.option('--stadt', prompt='Stadt', help='Stadt des Hauses')
def add_haus(strasse, hausnummer, plz, stadt):
    """Fügt ein neues Haus hinzu"""
    haus = Haus.objects.create(strasse=strasse, hausnummer=hausnummer, plz=plz, stadt=stadt)
    click.echo(f"Haus {haus.strasse} {haus.hausnummer} in {haus.stadt} erfolgreich hinzugefügt.")


@add.command('wohnung')
@click.option('--haus_id', type=int, prompt='Haus ID', help='ID des Hauses')
@click.option('--etage', prompt='Etage', help='Etage der Wohnung')
@click.option('--lage_im_haus', prompt='Lage im Haus', help='Lage der Wohnung im Haus')
@click.option('--groesse', prompt='Größe der Wohnung', type=float, help='Größe der Wohnung')
def add_wohnung(haus_id, etage, lage_im_haus, groesse):
    """Fügt eine neue Wohnung hinzu"""
    haus = Haus.objects.get(id=haus_id)
    wohnung = Wohnung.objects.create(haus=haus, etage=etage, lage_im_haus=lage_im_haus, groesse=groesse)
    click.echo(f"Wohnung {wohnung.etage} in Haus {wohnung.haus} erfolgreich hinzugefügt.")


@add.command('mietvertrag')
@click.option('--mieter_id', type=int, prompt='Mieter ID', help='ID des Mieters')
@click.option('--wohnung_id', type=int, prompt='Wohnung ID', help='ID der Wohnung')
@click.option('--startdatum', prompt='Startdatum (YYYY-MM-DD)', help='Startdatum des Mietvertrags')
@click.option('--enddatum', prompt='Enddatum (YYYY-MM-DD)', help='Enddatum des Mietvertrags')
@click.option('--mietpreis', type=float, prompt='Mietpreis', help='Monatlicher Mietpreis')
def add_mietvertrag(mieter_id, wohnung_id, startdatum, enddatum, mietpreis):
    """Fügt einen neuen Mietvertrag hinzu"""
    mieter = Mieter.objects.get(id=mieter_id)
    wohnung = Wohnung.objects.get(id=wohnung_id)
    mietvertrag = Mietvertrag.objects.create(
        mieter=mieter,
        wohnung=wohnung,
        startdatum=startdatum,
        enddatum=enddatum,
        mietpreis=mietpreis
    )
    click.echo(f"Mietvertrag für Mieter {mieter.vorname} {mieter.nachname} in Wohnung {wohnung.etage} erfolgreich hinzugefügt.")


@add.command('komplex')
@click.option('--name', prompt='Name des Komplexes', help='Name des Komplexes')
@click.option('--beschreibung', prompt='Beschreibung', help='Beschreibung des Komplexes')
def add_komplex(name, beschreibung):
    """Fügt einen neuen Komplex hinzu"""
    komplex = Komplex.objects.create(name=name, beschreibung=beschreibung)
    click.echo(f"Komplex {komplex.name} erfolgreich hinzugefügt.")


@add.command('kostenstelle')
@click.option('--name', prompt='Name der Kostenstelle', help='Name der Kostenstelle')
@click.option('--beschreibung', prompt='Beschreibung', help='Beschreibung der Kostenstelle')
def add_kostenstelle(name, beschreibung):
    """Fügt eine neue Kostenstelle hinzu"""
    kostenstelle = Kostenstelle.objects.create(name=name, beschreibung=beschreibung)
    click.echo(f"Kostenstelle {kostenstelle.name} erfolgreich hinzugefügt.")


@add.command('kostensplit')
@click.option('--kostenstelle_id', type=int, prompt='Kostenstelle ID', help='ID der Kostenstelle')
@click.option('--anteil', type=float, prompt='Kostenanteil', help='Anteil der Kosten')
def add_kostensplit(kostenstelle_id, anteil):
    """Fügt einen neuen Kostensplit hinzu"""
    kostenstelle = Kostenstelle.objects.get(id=kostenstelle_id)
    kostensplit = Kostensplit.objects.create(kostenstelle=kostenstelle, anteil=anteil)
    click.echo(f"Kostensplit für Kostenstelle {kostenstelle.name} erfolgreich hinzugefügt.")


@add.command('komplexteile')
@click.option('--komplex_id', type=int, prompt='Komplex ID', help='ID des Komplexes')
@click.option('--beschreibung', prompt='Beschreibung des Teils', help='Beschreibung des Teils')
def add_komplexteile(komplex_id, beschreibung):
    """Fügt ein neues Teil eines Komplexes hinzu"""
    komplex = Komplex.objects.get(id=komplex_id)
    komplexteil = Komplexteile.objects.create(komplex=komplex, beschreibung=beschreibung)
    click.echo(f"Teil des Komplexes {komplex.name} erfolgreich hinzugefügt.")


# Edit Commands
@cli.group()
def edit():
    """Bearbeite bestehende Datensätze"""
    pass


@edit.command('mieter')
@click.argument('mieter_id', type=int)
@click.option('--vorname', help='Vorname des Mieters')
@click.option('--nachname', help='Nachname des Mieters')
@click.option('--kontakt_info', help='Kontaktinformationen des Mieters')
def edit_mieter(mieter_id, vorname, nachname, kontakt_info):
    """Bearbeite einen bestehenden Mieter"""
    mieter = Mieter.objects.get(id=mieter_id)
    if vorname:
        mieter.vorname = vorname
    if nachname:
        mieter.nachname = nachname
    if kontakt_info:
        mieter.kontakt_info = kontakt_info
    mieter.save()
    click.echo(f"Mieter {mieter_id} wurde erfolgreich bearbeitet.")


@edit.command('mietvertrag')
@click.argument('mietvertrag_id', type=int)
@click.option('--startdatum', help='Startdatum des Mietvertrags')
@click.option('--enddatum', help='Enddatum des Mietvertrags')
@click.option('--mietpreis', type=float, help='Monatlicher Mietpreis')
def edit_mietvertrag(mietvertrag_id, startdatum, enddatum, mietpreis):
    """Bearbeite einen bestehenden Mietvertrag"""
    mietvertrag = Mietvertrag.objects.get(id=mietvertrag_id)
    if startdatum:
        mietvertrag.startdatum = startdatum
    if enddatum:
        mietvertrag.enddatum = enddatum
    if mietpreis:
        mietvertrag.mietpreis = mietpreis
    mietvertrag.save()
    click.echo(f"Mietvertrag {mietvertrag_id} wurde erfolgreich bearbeitet.")


# List Commands
@cli.group()
def list():
    """Listet verschiedene Datensätze auf"""
    pass


@list.command('mieter')
def list_mieter():
    """Listet alle Mieter auf"""
    mieter_list = Mieter.objects.all()
    click.echo("Mieter-Liste:")
    for mieter in mieter_list:
        click.echo(f"{mieter.id}: {mieter.vorname} {mieter.nachname}")


@list.command('mietvertrag')
def list_mietvertrag():
    """Listet alle Mietverträge auf"""
    mietvertrag_list = Mietvertrag.objects.all()
    click.echo("Mietvertrag-Liste:")
    for mietvertrag in mietvertrag_list:
        click.echo(f"{mietvertrag.id}: Mieter {mietvertrag.mieter.vorname} {mietvertrag.mieter.nachname}, Wohnung {mietvertrag.wohnung.etage}, Mietpreis {mietvertrag.mietpreis} EUR")


@list.command('komplex')
def list_komplex():
    """Listet alle Komplexe auf"""
    komplex_list = Komplex.objects.all()
    click.echo("Komplex-Liste:")
    for komplex in komplex_list:
        click.echo(f"{komplex.id}: {komplex.name} - {komplex.beschreibung}")


# Delete Commands
@cli.group()
def delete():
    """Lösche bestehende Datensätze"""
    pass


@delete.command('mieter')
@click.argument('mieter_id', type=int)
def delete_mieter(mieter_id):
    """Lösche einen Mieter"""
    try:
        mieter = Mieter.objects.get(id=mieter_id)
        mieter.delete()
        click.echo(f"Mieter {mieter_id} wurde erfolgreich gelöscht.")
    except Mieter.DoesNotExist:
        click.echo(f"Mieter mit ID {mieter_id} wurde nicht gefunden.")


@delete.command('mietvertrag')
@click.argument('mietvertrag_id', type=int)
def delete_mietvertrag(mietvertrag_id):
    """Lösche einen Mietvertrag"""
    try:
        mietvertrag = Mietvertrag.objects.get(id=mietvertrag_id)
        mietvertrag.delete()
        click.echo(f"Mietvertrag {mietvertrag_id} wurde erfolgreich gelöscht.")
    except Mietvertrag.DoesNotExist:
        click.echo(f"Mietvertrag mit ID {mietvertrag_id} wurde nicht gefunden.")


if __name__ == '__main__':
    cli()
