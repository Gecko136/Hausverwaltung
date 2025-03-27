import click
from hausverwaltung.config import set_gnucash_path, set_db_path, get_gnucash_path, get_db_path, set_config
from hausverwaltung.db import add_mieter_to_db


@click.group()
def cli():
    """Hausverwaltung CLI"""
    pass

@click.command()
@click.option('--file', type=click.Path(exists=True), help='Pfad zur GnuCash-Datei.')
def import_gnucash(file):
    """Importiert GnuCash-Daten."""
    click.echo(f"Importiere GnuCash-Daten aus {file if file else 'der Standarddatei'}...")

@click.command()
@click.option('--haus', type=int, help='ID des Hauses')
@click.option('--mieter', type=int, help='ID des Mieters')
@click.option('--all', is_flag=True, help='Bericht für alle Mieter des Hauses')
@click.option('--pdf', is_flag=True, help='Bericht im PDF-Format')
@click.option('--txt', is_flag=True, help='Bericht als Textausgabe')
def report(haus, mieter, all, pdf, txt):
    """Erstellt einen Nebenkostenbericht."""
    click.echo(f"Erstelle Bericht für Haus {haus} und Mieter {mieter}...")
    if all:
        click.echo("Bericht für alle Mieter...")
    if pdf:
        click.echo("Bericht im PDF-Format...")
    if txt:
        click.echo("Bericht als Textausgabe...")

@click.command()
@click.option('--haus', is_flag=True, help='Listet alle Häuser auf.')
@click.option('--mieter', is_flag=True, help='Listet alle Mieter auf.')
def list(haus, mieter):
    """Listet Häuser oder Mieter auf."""
    if haus:
        click.echo("Liste aller Häuser...")
    if mieter:
        click.echo("Liste aller Mieter...")

@click.command()
@click.option('--set', is_flag=True, help='Setzt neue Konfigurationseinstellungen.')
@click.option('--db', type=click.Path(), help='Pfad zur Datenbankdatei.')
@click.option('--gnucash', type=click.Path(), help='Pfad zur GnuCash-Datei.')
@click.option('--get', is_flag=True, help='Zeigt aktuelle Konfigurationseinstellungen.')
def config(set, db, gnucash, get):
    """Verwaltet Konfigurationseinstellungen."""

    if set:
        if db:
            set_db_path(db)
        if gnucash:
            set_gnucash_path(gnucash)       

    if get:
        click.echo(f"GnuCash-Pfad: {get_gnucash_path()}")
        click.echo(f"DB-Pfad: {get_db_path()}")

# Add Commands
@cli.group()
def add():
    """Addiere neue Datensätze"""
    pass

@add.command('mieter')
@click.option('--vorname', default='', prompt='Vorname', help='Vorname des Mieters')
@click.option('--nachname', default='', prompt='Nachname', help='Nachname des Mieters')
def add_mieter(vorname, nachname):
    """Füge einen neuen Mieter hinzu"""
    
    # Standardwert setzen, falls nichts eingegeben wurde
    if not vorname:
        vorname = "Nicht angegeben"
    if not nachname:
        nachname = "Nicht angegeben"
    
    click.echo(f"Neuer Mieter: {vorname} {nachname}")
    
    # Den Mieter in die Datenbank speichern
    add_mieter_to_db(vorname, nachname)

@add.command('wohnung')
@click.argument('adresse')
@click.argument('zimmeranzahl')
def add_wohnung(adresse, zimmeranzahl):
    """Füge eine neue Wohnung hinzu"""
    click.echo(f"Neue Wohnung {adresse} mit {zimmeranzahl} Zimmern wurde hinzugefügt.")

@add.command('raum')
@click.argument('name')
@click.argument('typ')
def add_raum(name, typ):
    """Füge einen neuen Raum hinzu"""
    click.echo(f"Neuer Raum {name} vom Typ {typ} wurde hinzugefügt.")

# Edit Commands
@cli.group()
def edit():
    """Bearbeite bestehende Datensätze"""
    pass

@edit.command('mieter')
@click.argument('mieter_id')
@click.argument('name')
@click.argument('email')
def edit_mieter(mieter_id, name, email):
    """Bearbeite einen bestehenden Mieter"""
    click.echo(f"Mieter {mieter_id} wurde zu {name} mit der Email {email} bearbeitet.")

@edit.command('wohnung')
@click.argument('wohnung_id')
@click.argument('adresse')
@click.argument('zimmeranzahl')
def edit_wohnung(wohnung_id, adresse, zimmeranzahl):
    """Bearbeite eine bestehende Wohnung"""
    click.echo(f"Die Wohnung {wohnung_id} wurde zu {adresse} mit {zimmeranzahl} Zimmern bearbeitet.")

@edit.command('raum')
@click.argument('raum_id')
@click.argument('name')
@click.argument('typ')
def edit_raum(raum_id, name, typ):
    """Bearbeite einen bestehenden Raum"""
    click.echo(f"Der Raum {raum_id} wurde zu {name} vom Typ {typ} bearbeitet.")

# Delete Commands
@cli.group()
def delete():
    """Lösche bestehende Datensätze"""
    pass

@delete.command('mieter')
@click.argument('mieter_id')
def delete_mieter(mieter_id):
    """Lösche einen Mieter"""
    click.echo(f"Mieter {mieter_id} wurde gelöscht.")

@delete.command('wohnung')
@click.argument('wohnung_id')
def delete_wohnung(wohnung_id):
    """Lösche eine Wohnung"""
    click.echo(f"Die Wohnung {wohnung_id} wurde gelöscht.")

@delete.command('raum')
@click.argument('raum_id')
def delete_raum(raum_id):
    """Lösche einen Raum"""
    click.echo(f"Der Raum {raum_id} wurde gelöscht.")
# Weitere ähnliche Befehle für Wohnungen, Räume und Mietverhältnisse

# Registrierung der Befehle bei der CLI
cli.add_command(import_gnucash)
cli.add_command(report)
cli.add_command(list)
cli.add_command(config)
cli.add_command(add_mieter)
cli.add_command(delete_mieter)
cli.add_command(edit_mieter)

if __name__ == '__main__':
    cli()
