import reversion  # Importiere reversion für Versionskontrolle
from django.db import models

@reversion.register  # Registriere das Modell für Versionskontrolle
class Mieter(models.Model):
    anrede = models.CharField(max_length=20, null=True, blank=True)
    nachname = models.CharField(max_length=100, null=True)
    kontakt_info = models.CharField(max_length=100, null=True, blank=True)
    vorname = models.CharField(max_length=100, null=True, blank=True)
    strasse = models.CharField(max_length=100, null=True, blank=True)
    hausnummer = models.CharField(max_length=10, null=True, blank=True)
    plz = models.CharField(max_length=10, null=True, blank=True)
    stadt = models.CharField(max_length=100, null=True, blank=True)
    telefon = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Mieter"  # Setze den Pluralnamen für das Modell
        verbose_name = "Mieter"  # Setze den Singularnamen für das Modell

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Haus(models.Model):
    strasse = models.CharField(max_length=100, null=True)
    hausnummer = models.CharField(max_length=10, null=True)
    plz = models.CharField(max_length=10, null=True)
    stadt = models.CharField(max_length=100, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "Häuser"  # Setze den Pluralnamen für das Modell
        verbose_name = "Haus"
    def __str__(self):
        return f"{self.strasse} {self.hausnummer}, {self.stadt}"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Wohnung(models.Model):
    haus = models.ForeignKey(Haus, on_delete=models.CASCADE)
    etage = models.CharField(max_length=50, null=True)
    lage_im_haus = models.CharField(max_length=50, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "Wohnungen"  # Setze den Pluralnamen für das Modell
        verbose_name = "Wohnung"

    def __str__(self):
        return f"Wohnung {self.etage}, {self.haus}"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Raumtypen(models.Model):
    typname = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = "Raumtypen"  # Setze den Pluralnamen für das Modell
        verbose_name = "Raumtyp"

    def __str__(self):
        return self.typname

class Raum(models.Model):
    wohnung = models.ForeignKey(Wohnung, on_delete=models.CASCADE)
    typ = models.ForeignKey(Raumtypen, on_delete=models.CASCADE)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "Räume"  # Setze den Pluralnamen für das Modell
        verbose_name = "Raum"
    def __str__(self):
        return f"Raum in {self.wohnung} - {self.typ}"


@reversion.register  # Registriere das Modell für Versionskontrolle
class Mietvertrag(models.Model):
    mieter = models.ForeignKey(Mieter, on_delete=models.CASCADE)
    wohnung = models.ForeignKey(Wohnung, on_delete=models.CASCADE)
    mietbeginn = models.DateField(null=True)
    mietende = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "Mietverträge"  # Setze den Pluralnamen für das Modell
        verbose_name = "Mietvertrag"

    def __str__(self):
        return f"Mietvertrag {self.id} - {self.mieter} in {self.wohnung}"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Kostenstelle(models.Model):
    bezeichnung = models.CharField(max_length=100, null=True)
    gnucash_path = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "Kostenstellen"  # Setze den Pluralnamen für das Modell
        verbose_name = "Kostenstelle"

    def __str__(self):
        return self.name

@reversion.register  # Registriere das Modell für Versionskontrolle
class Kosten(models.Model):
    kostenstelle = models.ForeignKey(Kostenstelle, on_delete=models.CASCADE)
    betrag = models.DecimalField(max_digits=8, decimal_places=2)
    buchungsdatum = models.DateField()
    beschreibung = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Kosten"  # Setze den Pluralnamen für das Modell
        verbose_name = "Kosten"

    def __str__(self):
        return f"Kosten {self.id} - {self.betrag} EUR"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Kostensplit(models.Model):
    kostenstelle = models.ForeignKey(Kostenstelle, on_delete=models.CASCADE)
    komplex = models.ForeignKey('Komplex', null=True, blank=True, on_delete=models.CASCADE)
    haus = models.ForeignKey(Haus, null=True, blank=True, on_delete=models.CASCADE)
    wohnung = models.ForeignKey(Wohnung, null=True, blank=True, on_delete=models.CASCADE)
    anteil = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "Kostensplits"  # Setze den Pluralnamen für das Modell
        verbose_name = "Kostensplit"

    def __str__(self):
        return f"Kostensplit {self.id} - {self.anteil}%"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Komplex(models.Model):
    name = models.CharField(max_length=50, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = "Komplexe"  # Setze den Pluralnamen für das Modell
        verbose_name = "Komplex"

    def __str__(self):
        return self.name

@reversion.register  # Registriere das Modell für Versionskontrolle
class Komplexteile(models.Model):
    komplex = models.ForeignKey(Komplex, on_delete=models.CASCADE)
    beschreibung = models.CharField(max_length=50, null=True)
    wohnung = models.ForeignKey(Wohnung, null=True, blank=True, on_delete=models.CASCADE)
    haus = models.ForeignKey(Haus, null=True, blank=True, on_delete=models.CASCADE)
    typ = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name_plural = "Komplexteile"
        verbose_name = "Komplexteil"

    def __str__(self):
        return f"Komplexteil {self.id} - {self.beschreibung}"


class Forderung(models.Model):
    kostensplit = models.ForeignKey(Kostensplit, on_delete=models.CASCADE)
    mietvertrag = models.ForeignKey(Mietvertrag, on_delete=models.CASCADE)
    berechnungsdatum = models.DateField()
    bezeichnung = models.CharField(max_length=200)
    gesamtbetrag = models.DecimalField(max_digits=8, decimal_places=2)
    split_anteil = models.IntegerField()
    umlageschluesselQM = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    umlageschluesselMietdauer = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    umlageschluesselVerbrauch = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gesamtwohnflaeche = models.DecimalField(max_digits=10, decimal_places=2)
    anteilwohnflaeche = models.DecimalField(max_digits=10, decimal_places=2)
    anteilbetrag = models.DecimalField(max_digits=8, decimal_places=2)
    miettage = models.IntegerField(null=True)
    tageimjahr = models.IntegerField(null=True)

    def __str__(self):
        return f"Forderung {self.id} - {self.bezeichnung}"

@reversion.register  # Registriere das Modell für Versionskontrolle
class Einheitstypen(models.Model):
    typname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.typname
