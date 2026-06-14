import logging

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from model import Station
from services.bysykkel import fetch_stations


load_dotenv()

logger = logging.getLogger("bysykkel")

app = FastAPI(
    title="Oslo Bysykkel — stasjoner",
    description="API som viser tilgjengelige sykler og låser for sykkelstasjoner i Oslo",
)


@app.get("/stations")
async def get_stations() -> list[Station]:
    """Returnerer alle stasjoner med antall ledige sykler og låser akkurat nå."""
    try:
        return await fetch_stations()
    except RuntimeError as exc:
        logger.exception("Konfigurasjonsfeil ved henting av stasjoner")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        logger.exception("Klarte ikke å hente data fra Oslo Bysykkel")
        raise HTTPException(
            status_code=502,
            detail="Klarte ikke å hente data fra Oslo Bysykkel.",
        ) from exc
