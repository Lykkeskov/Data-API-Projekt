## Links
- [Website](https://halfdan.pythonanywhere.com)
- [Scrum](https://trello.com/invite/b/68a6fc9760098e3a707cd846/ATTI054e69901bb32a28f689f419624f4b910F01337E/data-api-projekt-informatik)
- [Miro](https://miro.com/welcomeonboard/YTFRQWRVQ2RIUXRBcjJjOHU0d0hzMG1MS05sZnpGbktObUtGdCtiU3N4bEIvU1U1RHBpNnVaN3Z1bmFoemVkcmRHUlhkVHJBeVMwdmI0d3J6UEc5UkFadHZFd3hkMGtMVWJ4UkVIUHc5UUpjNXJCOWFMTXZNVmZLU2xxQXVmNW9NakdSWkpBejJWRjJhRnhhb1UwcS9BPT0hdjE=?share_link_id=362116878752)

## Indholdsfortegnelse

1. Formål
2. Projektstruktur
3. Installation og opstart
4. Database (SQLite)
5. API-dokumentation (endpoints, eksempler)
6. ESP32: hvordan den sender data
7. Visualisering
8. Fejlfinding & logs
9. E/R-diagrammer og flowcharts
10. Licens / Kontakt

## 1) Introduktion

I dette projekt indsamler vi data vha. sensorer. Det er her lysniveau for lokaler på skolen, der indsamles vha. en lyssensor (light dependant resistor), som er tilsluttet en ESP32 micro controller. Værdierne gemmes i en SQLite-database og visualiseres med et kort over skolen.

## 2) Projektstruktur

```
/home/<brugernavn>/Data-API-Projekt/
├── flask_app.py        # Flask API + init_db()
├── data.db             # SQLite database (oprettes automatisk)
├── requirements.txt    # pip dependencies (flask, pandas, plotly ...)
├── index.py            # Visualiserings-app (PlanKort)
├── mapping.py          # PlanKort-klasse (tegner plankort med punkter)
├── static/             # billeder: plan1.png, plan2.png ...
└── templates/
    └── index.html
```

## 3) Installation og opstart

### Krav

* Python 3.8+
* pip
* En ESP32 med WiFi

### Python dependencies

Lav en `requirements.txt` med mindst:

```
Flask
pandas
plotly
```

Installer:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start lokalt (udvikling)

1. Slet evt. gammel database hvis skema har ændret sig:

```bash
rm /path/to/project/data.db
```

2. Kør Flask (kun til udvikling):

```bash
python3 flask_app.py
```

Flask vil køre på `http://127.0.0.1:5000` med `debug=True` (kun til test). På PythonAnywhere/produktion skal der bruges WSGI og platformen håndterer serveren.

## 4) Database (SQLite)

Databasefil: `data.db` (placering i `flask_app.py` som `DB_PATH`).

Tabel: `sensor_data` — skema:

```sql
CREATE TABLE IF NOT EXISTS sensor_data (
    lokale INTEGER PRIMARY KEY,
    lysniveau INTEGER,
    timestamp TEXT
);
```

Forklaring:

* `lokale`: room id (heltal). I projektet bruger vi `lokale` som PRIMARY KEY (nøgle), så der kun findes én række per lokale. Ny indkommende data opdaterer eksisterende række.
* `lysniveau`: integer (måling fra ESP32)
* `timestamp`: ISO-formateret streng (fx `2025-10-29 12:34:56`)

## 5) API-dokumentation (dansk)

Her går vi i dybden. Alle endpoints er under dit domæne, fx `https://<brugernavn>.pythonanywhere.com`.

### Generelle noter

* Content-Type: `application/json` for POST requests.
* Alle svar er JSON.

---

### 1) `POST /data`

**Beskrivelse:** Modtager/indsætter/opfører opdateret data for et lokale.

**URL:** `POST https://<dit_domæne>/data`

**Body (JSON):**

```json
{
  "lokale": 211,
  "lysniveau": 102
}
```

**Headers:**

```
Content-Type: application/json
```

**Svar (200 OK):**

```json
{ "status": "saved or updated" }
```

**Fejl (400 Bad Request):**

* Når JSON mangler eller felterne ikke findes.

```json
{ "error": "Invalid data format" }
```

**Fejl (500 Internal Server Error):**

* Databasefejl eller lignende.

```json
{ "error": "<fejlbesked>" }
```

**Eksempel med curl:**

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"lokale":211,"lysniveau":102}' \
  https://halfdan.pythonanywhere.com/data
```

---

### 2) `GET /data`

**Beskrivelse:** Returnerer alle lokaler (en række per `lokale`). Praktisk til visning af alle punkter på kort.

**URL:** `GET https://<dit_domæne>/data`

**Svar (200 OK):** JSON-array med objekter:

```json
[
  {"lokale": 111, "lysniveau": 300, "timestamp": "2025-10-29 10:00:00"},
  {"lokale": 211, "lysniveau": 102, "timestamp": "2025-10-29 10:05:00"}
]
```

---

### 3) `GET /data/<lokale>`

**Beskrivelse:** Returnerer data for et enkelt lokale (fx 211)

**URL:** `GET https://<dit_domæne>/data/211`

**Svar (200 OK):**

```json
{ "lokale": 211, "lysniveau": 102, "timestamp": "2025-10-29 10:05:00" }
```

**Fejl (404):**

```json
{ "error": "No data found for room 211" }
```

---

## 6) ESP32: hvordan den sender data

Nøglepunkter:

* Brug HTTP (http://) for nem test. HTTPS kræver `WiFiClientSecure` og certifikatstyring.
* Sæt header `Content-Type: application/json`.
* Send en JSON-streng med `lokale` (int) og `lysniveau` (int).

### Arduino (ESP32) eksempel (opdateret, robust):

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "DIT_SSID";
const char* password = "DIT_PASSWORD";
const char* server = "http://halfdan.pythonanywhere.com/data"; // eller dit domæne

void sendData(int lokale, int lysniveau) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(server);
  http.addHeader("Content-Type", "application/json");

  String json = "{";
  json += "\"lokale\":" + String(lokale) + ",";
  json += "\"lysniveau\":" + String(lysniveau);
  json += "}";

  int code = http.POST(json);
  Serial.print("HTTP code: "); Serial.println(code);
  if (code > 0) Serial.println(http.getString());
  http.end();
}
```

### Tip

* Brug `http://` under udvikling. Til produktion bør du opsætte HTTPS korrekt.
* Hvis du bruger PowerShell på Windows, pas på `curl`-escaping (brug single quotes i bash eller dobbelte med escaping i PowerShell).

## 7) Visualisering

* Filen `app.py` bruger `mapping.PlanKort` til at tegne et plankort og placere punkter.
* Data hentes fra `data.db` med `pandas.read_sql_query(...)`.
* Matching mellem kortets `lokale` tekst (fx `D2111`) og databasen sker ved at ekstrahere de sidste 3 cifre: `D2111` → `111` eller `D2211` → `211` afhængigt af dit mappings-regel. Tilpas `str.extract(r'(\d{3})$')` hvis formatet er forskelligt.
* `PlanKort.lav_figur()` returnerer et plotly-figure som konverteres til HTML via `fig.to_html(full_html=False)` og indsættes i `templates/index.html`.

**Auto-opdatering:** enten brug `<meta http-equiv="refresh" content="10">` eller AJAX for glattere opdateringer.

## 8) Fejlfinding og logs

* Hvis du ser "Something went wrong" i browseren på PythonAnywhere: tjek **Web → Error log** (der står traceback).
* Typiske fejl:

  * `ModuleNotFoundError: No module named 'flask_app'` → wsgi PATH peger ikke på mappen.
  * `IndentationError` i SQL triple-quoted string → sørg for korrekt indrykning: `CREATE TABLE` skal starte i kolonne 0 inden i '' '\n '.
  * `500` med `no such table: sensor_data` → slet `data.db` og genstart (init_db kører ved import og opretter tabellen).
  * HTTP 400 fra API → JSON-formatet er forkert eller mangler felter.

**Se logs:**

* PythonAnywhere: Web → View log files → Error log og Server log.
* Lokalt: se terminal output når du kører `python3 flask_app.py`.

## 9) E/R-diagram og flowcharts

### E/R (enkelt oversigt)

```
+-----------------+
|  sensor_data    |
+-----------------+
| lokale (PK)     |
| lysniveau       |
| timestamp       |
+-----------------+
```

Forklaring: eneste tabel i systemet er `sensor_data`. `lokale` er primary key — dvs. én række pr. lokale.

---

### Flowchart

```
[ESP32 button press] --> build JSON --> HTTP POST /data --> Flask API
    |                                            |
    v                                            v
[ESP32 prints response]                    Flask validates JSON
                                               |
                                               v
                                         DB: INSERT OR UPDATE
                                               |
                                               v
                                         Return 200 JSON {status}
                                               |
                                               v
                                          Visualizer GET /data --> show map
```

---

## 10) Eksempler på test-kommandoer

**Send test via curl:**

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"lokale":211,"lysniveau":102}' \
  https://halfdan.pythonanywhere.com/data
```

**Hent alle lokaler:**

```
curl https://halfdan.pythonanywhere.com/data
```

**Hent ét lokale:**

```
curl https://halfdan.pythonanywhere.com/data/211
```
