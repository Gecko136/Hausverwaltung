import reversion  # Importiere reversion für die Versionskontrolle
from reversion.admin import VersionAdmin  # Importiere VersionAdmin für die Admin-Oberfläche
from django.contrib import admin
from .models import Mietvertrag, Mieter, Wohnung, Raum, Raumtypen, Haus, Komplex, Komplexteile
from .models import Forderung
from .models import Kostenstelle, Kosten, Kostensplit  # Importiere die Modelle für die Admin-Oberfläche


class MieterAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('anrede', 'vorname', 'nachname')  # Reihenfolge der Felder
        }),
        ('Kontakt Info', {
            'fields': ('kontakt_info', 'telefon', 'email')  # Weitere Felder für Kontaktinformationen
        }),
        ('Adresse', {
            'fields': ('strasse', 'hausnummer', 'plz', 'stadt')  # Weitere Felder für die Adresse
        }),
    )
    list_display = ('anrede', 'vorname', 'nachname')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('vorname', 'nachname')  # Suchfelder für die Liste
    

class MietvertragAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('mieter', 'wohnung', 'mietbeginn', 'mietende')  # Reihenfolge der Felder
        }),
    )
    autocomplete_fields = ('mieter', 'wohnung')  # Autocomplete-Felder für bessere Benutzererfahrung
    list_display = ('mieter', 'wohnung', 'mietbeginn', 'mietende')  # Felder, die in der Liste angezeigt werden sollen

class WohnungAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('haus', 'etage', 'lage_im_haus', 'groesse', 'nebenkosten_groesse')  # Reihenfolge der Felder
        }),
    )
    list_display = ('haus', 'etage', 'lage_im_haus')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('haus__strasse', 'etage')  # Suchfelder für die Liste

class RaumAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('wohnung', 'typ', 'groesse', 'nebenkosten_groesse')  # Reihenfolge der Felder
        }),
    )
    list_display = ('wohnung', 'typ')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('wohnung__haus__strasse', 'typ__typname')  # Suchfelder für die Liste

class RaumtypenAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('typname',)  # Reihenfolge der Felder
        }),
    )
    list_display = ('typname',)  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('typname',)  # Suchfelder für die Liste    

class HausAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('strasse', 'hausnummer', 'plz', 'stadt')  # Reihenfolge der Felder
        }),
    )
    list_display = ('strasse', 'hausnummer', 'stadt')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('strasse', 'hausnummer', 'stadt')  # Suchfelder für die Liste

class KomplexteileAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('komplex', )  # Reihenfolge der Felder
        }),
    )
    list_display = ('komplex', )  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('komplex__name', )  # Suchfelder für die Liste

class KomplexAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'beschreibung')  # Reihenfolge der Felder
        }),
    )
    list_display = ('name',)  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('name',)  # Suchfelder für die Liste


class KostenstelleAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('bezeichnung', 'gnucash_path', 'name')  # Reihenfolge der Felder
        }),
    )
    list_display = ('bezeichnung', 'name')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('bezeichnung', 'name')  # Suchfelder für die Liste

class KostenAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('kostenstelle', 'betrag', 'buchungsdatum', 'beschreibung')  # Reihenfolge der Felder
        }),
    )
    list_display = ('kostenstelle', 'betrag', 'buchungsdatum')  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('kostenstelle__bezeichnung', 'betrag')  # Suchfelder für die Liste

class KostensplitAdmin(VersionAdmin):
    fieldsets = (
        (None, {
            'fields': ('kostenstelle', )  # Reihenfolge der Felder
        }),
    )
    list_display = ('kostenstelle', )  # Felder, die in der Liste angezeigt werden sollen
    search_fields = ('kostenstelle__bezeichnung', )  # Suchfelder für die Liste


admin.site.register(Mietvertrag, MietvertragAdmin)
admin.site.register(Mieter, MieterAdmin)  # Registriere den Mieter mit dem Admin-Interface
admin.site.register(Wohnung, WohnungAdmin)  # Registriere die Wohnung mit dem Admin-Interface
admin.site.register(Raum, RaumAdmin)  # Registriere den Raum mit dem Admin-Interface
admin.site.register(Raumtypen, RaumtypenAdmin)  # Registriere den Raumtyp mit dem Admin-Interface
admin.site.register(Haus, HausAdmin)  # Registriere das Haus mit dem Admin-Interface
admin.site.register(Komplex, KomplexAdmin)  # Registriere den Komplex mit dem Admin-Interface
admin.site.register(Komplexteile, KomplexteileAdmin)  # Registriere die Komplexteile mit dem Admin-Interface
admin.site.register(Kostenstelle, KostenstelleAdmin)  # Registriere die Kostenstelle mit dem Admin-Interface
admin.site.register(Kosten, KostenAdmin)  # Registriere die Kosten mit dem Admin-Interface
admin.site.register(Kostensplit, KostensplitAdmin)  # Registriere den Kostensplit mit dem Admin-Interface


