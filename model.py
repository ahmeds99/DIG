from dataclasses import dataclass


@dataclass(frozen=True)
class StationInformation:
    station_id: str
    name: str
    capacity: int
    address: str


@dataclass(frozen=True)
class StationStatus:
    station_id: str
    num_bikes_available: int
    num_docks_available: int


@dataclass(frozen=True)
class Station:
    name: str
    address: str
    available_bikes: int
    available_locks: int
