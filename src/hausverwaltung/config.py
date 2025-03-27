import configparser
import os

# Definiere den Pfad zur Konfigurationsdatei
CONFIG_FILE_PATH = "config.ini"

# Stelle sicher, dass die Konfigurationsdatei existiert
def ensure_config_file():
    if not os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config.read_dict({"DEFAULT": {"gnucash_path": "", "db_path": ""}})
        with open(CONFIG_FILE_PATH, "w") as configfile:
            config.write(configfile)

# Lade die Konfiguration aus der Datei
def load_config():
    ensure_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config

# Lese den GnuCash-Pfad
def get_gnucash_path():
    config = load_config()
    return config["DEFAULT"].get("gnucash_path", "")

# Lese den DB-Pfad
def get_db_path():
    config = load_config()
    return config["DEFAULT"].get("db_path", "")

# Setze den GnuCash-Pfad
def set_gnucash_path(path):
    config = load_config()
    config["DEFAULT"]["gnucash_path"] = path
    with open(CONFIG_FILE_PATH, "w") as configfile:
        config.write(configfile)

# Setze den DB-Pfad
def set_db_path(path):
    config = load_config()
    config["DEFAULT"]["db_path"] = path
    with open(CONFIG_FILE_PATH, "w") as configfile:
        config.write(configfile)

# Setze beide Pfade (GnuCash und DB)
def set_config(gnucash_path=None, db_path=None):
    if gnucash_path:
        set_gnucash_path(gnucash_path)
    if db_path:
        set_db_path(db_path)
