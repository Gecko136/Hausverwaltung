from setuptools import setup, find_packages

setup(
    name="hausverwaltung",  # Der Name des Projekts
    version="0.1.0",  # Die Version des Projekts
    description="Projekt für Hausverwaltung mit Nebenkostenabrechnung",  # Eine kurze Beschreibung
    author="Gunnar Quehl",  # Dein Name
    author_email="mail@gunnar-quehl.de",  # Deine E-Mail
    packages=find_packages(where='src'),  # Sucht automatisch nach allen Paketen im src-Ordner
    package_dir={"": "src"},  # Gibt an, dass die Pakete im `src`-Verzeichnis liegen
    include_package_data=True,  # Damit auch andere Dateien wie Templates oder Konfigurationen einbezogen werden
    install_requires=[  # Die Abhängigkeiten, die das Projekt benötigt
        "click",
        "jinja2",
        "python-docx",
        "fpdf2",
        "pyodbc",
        "python-dotenv",
        "reportlab",
        "django",
        "djangorestframework"
    ],
    entry_points={  # Definiert den Einstiegspunkt für das CLI
        "console_scripts": [
            "immo = hausverwaltung.cli:cli"
        ]
    }
)
