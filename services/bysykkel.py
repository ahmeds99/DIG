import asyncio
import os

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
    return _build_stations(information, status)


async def _fetch_information(
    client: httpx.AsyncClient,
) -> list[StationInformation]:
    response = await client.get(STATION_INFORMATION_URL)
    response.raise_for_status()
    return [
        StationInformation(
            station_id=s["station_id"],
            name=s["name"],
            capacity=s["capacity"],
            address=s.get("address"),
        )
        for s in response.json()["data"]["stations"]
    ]


async def _fetch_status(client: httpx.AsyncClient) -> list[StationStatus]:
    response = await client.get(STATION_STATUS_URL)
    response.raise_for_status()
    return [
        StationStatus(
            station_id=s["station_id"],
            num_bikes_available=s["num_bikes_available"],
            num_docks_available=s["num_docks_available"],
        )
        for s in response.json()["data"]["stations"]
    ]


def _build_stations(
    information: list[StationInformation],
    status: list[StationStatus],
) -> list[Station]:
    status_by_id = {s.station_id: s for s in status}
    stations = (
        Station(
            name=info.name,
            address=info.address,
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
