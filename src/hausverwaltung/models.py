from django.db import models

class Mieter(models.Model):
    anrede = models.CharField(max_length=20, null=True)
    nachname = models.CharField(max_length=100, null=True)
    kontakt_info = models.CharField(max_length=100, null=True)
    vorname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.vorname} {self.nachname}"

class Haus(models.Model):
    strasse = models.CharField(max_length=100, null=True)
    hausnummer = models.CharField(max_length=10, null=True)
    plz = models.CharField(max_length=10, null=True)
    stadt = models.CharField(max_length=100, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.strasse} {self.hausnummer}, {self.stadt}"

class Wohnung(models.Model):
    haus = models.ForeignKey(Haus, on_delete=models.CASCADE)
    etage = models.CharField(max_length=50, null=True)
    lage_im_haus = models.CharField(max_length=50, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Wohnung {self.etage}, {self.haus}"

class Raumtypen(models.Model):
    typname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.typname

class Raum(models.Model):
    wohnung = models.ForeignKey(Wohnung, on_delete=models.CASCADE)
    typ = models.ForeignKey(Raumtypen, on_delete=models.CASCADE)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"Raum in {self.wohnung} - {self.typ}"

class Mietvertrag(models.Model):
    mieter = models.ForeignKey(Mieter, on_delete=models.CASCADE)
    wohnung = models.ForeignKey(Wohnung, on_delete=models.CASCADE)
    mietbeginn = models.DateField(null=True)
    mietende = models.DateField(null=True)

    def __str__(self):
        return f"Mietvertrag {self.id} - {self.mieter} in {self.wohnung}"

class Kostenstelle(models.Model):
    bezeichnung = models.CharField(max_length=100, null=True)
    gnucash_path = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Kosten(models.Model):
    kostenstelle = models.ForeignKey(Kostenstelle, on_delete=models.CASCADE)
    betrag = models.DecimalField(max_digits=8, decimal_places=2)
    buchungsdatum = models.DateField()
    beschreibung = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Kosten {self.id} - {self.betrag} EUR"

class Kostensplit(models.Model):
    kostenstelle = models.ForeignKey(Kostenstelle, on_delete=models.CASCADE)
    komplex = models.ForeignKey('Komplex', null=True, blank=True, on_delete=models.CASCADE)
    haus = models.ForeignKey(Haus, null=True, blank=True, on_delete=models.CASCADE)
    wohnung = models.ForeignKey(Wohnung, null=True, blank=True, on_delete=models.CASCADE)
    anteil = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"Kostensplit {self.id} - {self.anteil}%"

class Komplex(models.Model):
    name = models.CharField(max_length=50, null=True)
    groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    nebenkosten_groesse = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name

class Komplexteile(models.Model):
    komplex = models.ForeignKey(Komplex, on_delete=models.CASCADE)
    beschreibung = models.CharField(max_length=50, null=True)
    wohnung = models.ForeignKey(Wohnung, null=True, blank=True, on_delete=models.CASCADE)
    haus = models.ForeignKey(Haus, null=True, blank=True, on_delete=models.CASCADE)
    typ = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Komplexteil {self.id} - {self.beschreibung}"

class Forderung(models.Model):
    kostensplit = models.ForeignKey(Kostensplit, on_delete=models.CASCADE)
    mietvertrag = models.ForeignKey(Mietvertrag, on_delete=models.CASCADE)
    berechnungsdatum = models.DateField()
    bezeichnung = models.CharField(max_length=200)
    gesamtbetrag = models.DecimalField(max_digits=8, decimal_places=2)
    split_anteil = models.IntegerField()
    gesamtwohnflaeche = models.DecimalField(max_digits=10, decimal_places=2)
    anteilwohnflaeche = models.DecimalField(max_digits=10, decimal_places=2)
    anteilbetrag = models.DecimalField(max_digits=8, decimal_places=2)
    miettage = models.IntegerField()

    def __str__(self):
        return f"Forderung {self.id} - {self.bezeichnung}"

class Einheitstypen(models.Model):
    typname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.typname
