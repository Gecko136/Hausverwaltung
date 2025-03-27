
# Hausverwaltung API

## CLI-Kommandos

### 1. `import`

Liest Daten aus einer GnuCash-Datei und speichert sie in der Datenbank.

#### Syntax
```bash
immo import gnucash
````

#### Optionen

- `--file` : Der Pfad zur GnuCash-Datei (optional, wenn nicht angegeben, wird nach einer standardmäßigen Datei gesucht).

---

### 2. `report`

Erstellt Berichte über Nebenkosten für bestimmte Mieter oder alle Mieter eines Hauses.

#### Syntax

```bash
immo report --haus <haus_id> --mieter <mieter_id> --pdf
immo report --haus <haus_id> --mieter <mieter_id> --txt
immo report --haus <haus_id> --all --pdf
immo report --haus <haus_id> --all --txt
```

#### Optionen

- `--haus <haus_id>` : ID des Hauses, für das der Bericht erstellt werden soll.
- `--mieter <mieter_id>` : ID des Mieters, für den der Bericht erstellt werden soll.
- `--all` : Erstelle einen Bericht für alle Mieter des Hauses.
- `--pdf` : Erstelle den Bericht im PDF-Format.
- `--txt` : Erstelle den Bericht als Textausgabe.

---

### 3. `list`

Listet alle Häuser oder alle Mieter auf.

#### Syntax

```bash
immo list --haus
immo list --mieter
```

#### Optionen

- `--haus` : Listet alle Häuser auf.
- `--mieter` : Listet alle Mieter auf.

---

### 4. `config`

Verwaltet Konfigurationseinstellungen wie Datenbankverbindung und Pfad zur GnuCash-Datei.

#### Syntax

```bash
immo config --set --db <database_path> --gnucash <gnucash_path>
immo config --get
```

#### Optionen

- `--set` : Setzt neue Konfigurationseinstellungen.
- `--db <database_path>` : Pfad zur Datenbankdatei.
- `--gnucash <gnucash_path>` : Pfad zur GnuCash-Datei.
- `--get` : Gibt die aktuellen Konfigurationseinstellungen aus.

---

### 5. `mieter create`

Erstellt einen neuen Mieter-Datensatz.

#### Syntax

```bash
immo mieter create --name <name> --adresse <adresse> --email <email>
```

#### Optionen

- `--name <name>` : Name des Mieters.
- `--adresse <adresse>` : Adresse des Mieters.
- `--email <email>` : E-Mail-Adresse des Mieters.

---

### 6. `mieter delete`

Löscht einen Mieter-Datensatz.

#### Syntax

```bash
immo mieter delete --mieter_id <mieter_id>
```

#### Optionen

- `--mieter_id <mieter_id>` : ID des Mieters, der gelöscht werden soll.

---

### 7. `mieter edit`

Bearbeitet einen bestehenden Mieter-Datensatz.

#### Syntax

```bash
immo mieter edit --mieter_id <mieter_id> --name <name> --adresse <adresse> --email <email>
```

#### Optionen

- `--mieter_id <mieter_id>` : ID des Mieters, der bearbeitet werden soll.
- `--name <name>` : Neuer Name des Mieters.
- `--adresse <adresse>` : Neue Adresse des Mieters.
- `--email <email>` : Neue E-Mail-Adresse des Mieters.

---

### 8. `wohneinheit create`

Erstellt eine neue Wohneinheit.

#### Syntax

```bash
immo wohneinheit create --nummer <nummer> --mieter_id <mieter_id> --wohnflaeche <wohnflaeche>
```

#### Optionen

- `--nummer <nummer>` : Nummer der Wohneinheit.
- `--mieter_id <mieter_id>` : ID des Mieters, der in der Wohneinheit wohnt.
- `--wohnflaeche <wohnflaeche>` : Wohnfläche der Wohneinheit in Quadratmetern.

---

### 9. `wohneinheit delete`

Löscht eine Wohneinheit.

#### Syntax

```bash
immo wohneinheit delete --wohneinheit_id <wohneinheit_id>
```

#### Optionen

- `--wohneinheit_id <wohneinheit_id>` : ID der Wohneinheit, die gelöscht werden soll.

---

### 10. `wohneinheit edit`

Bearbeitet eine bestehende Wohneinheit.

#### Syntax

```bash
immo wohneinheit edit --wohneinheit_id <wohneinheit_id> --nummer <nummer> --mieter_id <mieter_id> --wohnflaeche <wohnflaeche>
```

#### Optionen

- `--wohneinheit_id <wohneinheit_id>` : ID der Wohneinheit, die bearbeitet werden soll.
- `--nummer <nummer>` : Neue Nummer der Wohneinheit.
- `--mieter_id <mieter_id>` : Neue ID des Mieters in dieser Wohneinheit.
- `--wohnflaeche <wohnflaeche>` : Neue Wohnfläche der Wohneinheit in Quadratmetern.

---

### 11. `raum create`

Erstellt einen neuen Raum innerhalb einer Wohneinheit.

#### Syntax

```bash
immo raum create --wohneinheit_id <wohneinheit_id> --raumname <raumname> --flaeche <flaeche>
```

#### Optionen

- `--wohneinheit_id <wohneinheit_id>` : ID der Wohneinheit, in der der Raum erstellt werden soll.
- `--raumname <raumname>` : Name des Raumes (z. B. "Küche", "Wohnzimmer").
- `--flaeche <flaeche>` : Fläche des Raumes in Quadratmetern.

---

### 12. `raum delete`

Löscht einen Raum innerhalb einer Wohneinheit.

#### Syntax

```bash
immo raum delete --raum_id <raum_id>
```

#### Optionen

- `--raum_id <raum_id>` : ID des Raums, der gelöscht werden soll.

---

### 13. `raum edit`

Bearbeitet einen bestehenden Raum.

#### Syntax

```bash
immo raum edit --raum_id <raum_id> --raumname <raumname> --flaeche <flaeche>
```

#### Optionen

- `--raum_id <raum_id>` : ID des Raums, der bearbeitet werden soll.
- `--raumname <raumname>` : Neuer Name des Raums.
- `--flaeche <flaeche>` : Neue Fläche des Raums in Quadratmetern.

---

### 14. `mietverhaeltnis create`

Erstellt ein neues Mietverhältnis zwischen einem Mieter und einer Wohneinheit.

#### Syntax

```bash
immo mietverhaeltnis create --mieter_id <mieter_id> --wohneinheit_id <wohneinheit_id> --startdatum <startdatum> --enddatum <enddatum>
```

#### Optionen

- `--mieter_id <mieter_id>` : ID des Mieters.
- `--wohneinheit_id <wohneinheit_id>` : ID der Wohneinheit.
- `--startdatum <startdatum>` : Startdatum des Mietverhältnisses (im Format YYYY-MM-DD).
- `--enddatum <enddatum>` : Enddatum des Mietverhältnisses (im Format YYYY-MM-DD).

---

### 15. `mietverhaeltnis delete`

Löscht ein Mietverhältnis.

#### Syntax

```bash
immo mietverhaeltnis delete --mietverhaeltnis_id <mietverhaeltnis_id>
```

#### Optionen

- `--mietverhaeltnis_id <mietverhaeltnis_id>` : ID des Mietverhältnisses, das gelöscht werden soll.

---

### 16. `mietverhaeltnis edit`

Bearbeitet ein bestehendes Mietverhältnis.

#### Syntax

```bash
immo mietverhaeltnis edit --mietverhaeltnis_id <mietverhaeltnis_id> --startdatum <startdatum> --enddatum <enddatum>
```

#### Optionen

- `--mietverhaeltnis_id <mietverhaeltnis_id>` : ID des Mietverhältnisses, das bearbeitet werden soll.
- `--startdatum <startdatum>` : Neues Startdatum des Mietverhältnisses (im Format YYYY-MM-DD).
- `--enddatum <enddatum>` : Neues Enddatum des Mietverhältnisses (im Format YYYY-MM-DD).