# Kodeoppgave for Digitaliseringsetaten — Oslo Bysykkel

Liten FastAPI-applikasjon som henter sanntidsdata fra
[Oslo Bysykkels åpne GBFS-API](https://oslobysykkel.no/apne-data/sanntid) og
eksponerer en liste over stativ med antall ledige sykler og ledige låser.

## Krav

- Python 3.12+
- En `Client-Identifier` til Oslo Bysykkel-API-et. Format:
  `organisasjon-appnavn` (se lenken over).

## Kom i gang

```bash
git clone https://github.com/ahmeds99/DIG

python3.12 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

# Åpne .env og fyll inn CLIENT_IDENTIFIER

fastapi dev
```

Tjeneren kjører på <http://127.0.0.1:8000>.

## Endepunkter

| Metode | Sti         | Beskrivelse                                                  |
| ------ | ----------- | ------------------------------------------------------------ |
| `GET`  | `/stations` | Liste over alle stativ med ledige sykler og låser akkurat nå |
| `GET`  | `/docs`     | Swagger-dokumentasjon (autogenerert av FastAPI)              |

## Arkitektur

- Forsøksvis inndeling i Controller-Service-Model-lag med hvert sitt ansvarsområde. Fokus på immuterbar data og dataklasser.
- Selv om metadata om stasjonene intuitivt oppdateres sjeldnere enn sanntidsdata, blir det ikke benyttet en database for å lagre denne dataen. Dette grunnet skopet av kodeoppgaven og tidsbruken.
