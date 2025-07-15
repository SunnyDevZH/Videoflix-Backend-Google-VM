# Videoflix Backend

Das Backend für die Videoflix-Plattform, entwickelt mit Django und Django REST Framework. Es bietet APIs für die Benutzerverwaltung, Videoverwaltung und Authentifizierung.

---

## 🚀 Features

- **Benutzerverwaltung**: Registrierung, Login und Token-basierte Authentifizierung.
- **Videoverwaltung**: Hochladen, Abrufen und Kategorisieren von Videos.
- **JWT-Authentifizierung**: Sicherer Zugriff auf geschützte Endpunkte.
- **Kategorisierung**: Videos nach Kategorien gruppieren und durchsuchen.
- **Google Cloud Storage**: Speicherung und Abruf von Videos und Thumbnails.

---

## 🛠️ Technologien

- **Python**: Programmiersprache
- **Django**: Web-Framework
- **Django REST Framework**: API-Entwicklung
- **SQLite**: Datenbank 
- **JWT**: Authentifizierung mit JSON Web Tokens
- **Google Cloud Storage**: Speicherung von Videos und Medien.
- **Google Cloud VM**: Hosting des Backends auf einer virtuellen Maschine.
- **Gunicorn**: WSGI-Server für die Ausführung der Django-Anwendung.
- **Nginx**: Reverse Proxy und statische Dateiverwaltung.

---

## ⚙️ Installation und Setup mit Dockers 🐳


### 1. Repository klonen
git clone https://github.com/SunnyDevZH/videoflix-backend
cd videoflix-backend

### 2. .env Datei erstellen
cp .env.template .env

### 3. Docker-Container starten
docker-compose up --build

### 4. Anwendung im Browser öffnen:
http://localhost:8000/admin


## 📧 Kontakt
Email: yannick.vaterlaus.dev@gmail.com

