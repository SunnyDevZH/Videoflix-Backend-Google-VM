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
```bash
git clone https://github.com/SunnyDevZH/videoflix-backend
```
```bash
cd videoflix-backend
```

### 2. .env Datei erstellen
```bash
cp .env.template .env
```

### 3. Docker-Container leeren
```bash
docker-compose down --volumes
```
```bash
docker-compose build --no-cache
```

### 4. Docker-Container starten
```bash
docker-compose up --build
```

### 5. Anwendung im Browser öffnen:
```bash
http://localhost:8000/admin
```

### 6. Benutzer und Passwort
```bash
Admin
```
```bash
Adminpassword
```
### 7. Video hochladen 
kann 5-10 Sek. dauern bis die Videos umgewandelt wurden von den Workers

### 8. Frontend starten
Siehe ReadMe

## 📧 Kontakt
```bash
Email: yannick.vaterlaus.dev@gmail.com
```

