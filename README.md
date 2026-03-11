# Discord-Advaced-Chat-AI
# 🤖 Discord AI Multimodal Bot

```text
    8888888b.                            888                              
    888   Y88b                           888                              
    888    888                           888                              
    888   d88P 8888b.  88888b.   .d8888b.888  .d8888b.  888d888 8888b.    
    8888888P"     "88b 888 "88b  d88"   8888 d88"   88b 888P"      "88b   
    888       .d888888 888  888  888    8888 888    888 888    .d888888   
    888       888  888 888  888  Y88b  d8888 Y88b  d88P 888    888  188   
    888       "Y888888 888  888  "Y8888P"888  "Y8888P"  888    "Y888888   

::: Application Development by ✘ Aki_SystemDown® ©2026 :::

Dieser Bot nutzt Google Gemini 1.5 Flash zur Intent-Analyse, um Nutzeranfragen automatisch in Bild- (DALL-E 3) oder Video-Generierungen (Luma AI) umzuwandeln. Ein integriertes Firebase-System verwaltet die Credits der User.
​
## 🛠️ Features
​Automatische Erkennung: Der Bot entscheidet selbstständig, ob ein Bild oder eine Animation gewünscht ist.
​Smart Prompting: Gemini optimiert die User-Eingabe für bessere KI-Ergebnisse.
​Credit-System: Firebase-Anbindung mit automatischem stündlichem Reset.
​
## 📦 Voraussetzungen
​Python 3.10+ installiert.
​API Keys für OpenAI, Google Gemini und Luma AI.
​Eine Firebase-Projekt-Datei (firebase-adminsdk.json).

## ​🚀 Anleitung: Eine .exe Datei erstellen
​Wenn du den Bot als eigenständiges Windows-Programm (.exe) ohne Python-Installation nutzen möchtest, folge diesen Schritten:

​## 1. Abhängigkeiten installieren
​Öffne dein Terminal/CMD im Projektordner und installiere alle Bibliotheken sowie den Compiler:

pip install discord.py google-generativeai openai lumaai firebase-admin aiohttp pyinstaller

## 2. Die .exe kompilieren
​Nutze den folgenden Befehl, um alle Dateien in eine einzige ausführbare Datei zu packen:

pyinstaller --onefile --noconsole --name "Aki_AI_Bot" --add-data "firebase-adminsdk.json;." main.py

​--onefile: Erstellt eine einzige Datei.
​--noconsole: Verhindert, dass sich ein CMD-Fenster öffnet (der Bot läuft im Hintergrund).
​--add-data: Bindet deine Firebase-Key-Datei direkt in die Exe ein.
​Ergebnis: Du findest die fertige Datei im neu erstellten Ordner dist/.
​⚖️ Lizenz
​© 2026 Aki_SystemDown. Alle Rechte vorbehalten.
