import asyncio
import os
from typing import Any

import httpx

from model import Station, StationInformation, StationStatus

GBFS_BASE_URL = "https://gbfs.urbansharing.com/oslobysykkel.no"
STATION_INFORMATION_URL = f"{GBFS_BASE_URL}/station_information.json"
STATION_STATUS_URL = f"{GBFS_BASE_URL}/station_status.json"


async def fetch_stations() -> list[Station]:
    async with httpx.AsyncClient(
        headers={"Client-Identifier": _client_identifier()}
    ) as client:
        information, status = await asyncio.gather(
            _fetch_information(client),
            _fetch_status(client),
        )
    return _merge(information, status)


async def _fetch_information(
    client: httpx.AsyncClient,
) -> list[StationInformation]:
    raw = await _get_stations(client, STATION_INFORMATION_URL)
    return [_parse_information(item) for item in raw]


async def _fetch_status(client: httpx.AsyncClient) -> list[StationStatus]:
    raw = await _get_stations(client, STATION_STATUS_URL)
    return [_parse_status(item) for item in raw]


async def _get_stations(client: httpx.AsyncClient, url: str) -> list[dict[str, Any]]:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()["data"]["stations"]


def _parse_information(raw: dict[str, Any]) -> StationInformation:
    return StationInformation(
        station_id=raw["station_id"],
        name=raw["name"],
        capacity=raw["capacity"],
    )


def _parse_status(raw: dict[str, Any]) -> StationStatus:
    return StationStatus(
        station_id=raw["station_id"],
        num_bikes_available=raw["num_bikes_available"],
        num_docks_available=raw["num_docks_available"],
    )


def _merge(
    information: list[StationInformation],
    status: list[StationStatus],
) -> list[Station]:
    status_by_id = {s.station_id: s for s in status}
    stations = (
        Station(
            name=info.name,
            available_bikes=status_by_id[info.station_id].num_bikes_available,
            available_locks=status_by_id[info.station_id].num_docks_available,
        )
        for info in information
        if info.station_id in status_by_id
    )
    return sorted(stations, key=lambda s: s.name)


def _client_identifier() -> str:
    identifier = os.environ.get("CLIENT_IDENTIFIER", "").strip()
    if not identifier:
        raise RuntimeError(
            "CLIENT_IDENTIFIER er ikke satt. Se README.md for hvordan du setter den."
        )
    return identifier
