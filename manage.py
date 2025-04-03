#!/usr/bin/env python
import os
import sys

# Füge src zum Python-Pfad hinzu
sys.path.append('./src')

if __name__ == "__main__":
    # Setze den richtigen Pfad zu den Django-Einstellungen
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hausverwaltung.settings")  # Hier den Pfad zur settings.py anpassen

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
