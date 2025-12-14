"""School holiday helper for Custody Schedule."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.util import dt as dt_util

from .const import HOLIDAY_API, LOGGER


@dataclass(frozen=True, slots=True)
class SchoolHoliday:
    """Represent a school holiday period."""

    name: str
    zone: str
    start: datetime
    end: datetime


class SchoolHolidayClient:
    """Simple cached client around the Education Nationale API."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._session = aiohttp_client.async_get_clientsession(hass)
        self._cache: dict[tuple[str, int], list[SchoolHoliday]] = {}

    async def async_list(self, zone: str, year: int) -> list[SchoolHoliday]:
        """Return all holidays for the provided zone/year pair."""
        cache_key = (zone, year)
        if cache_key in self._cache:
            return self._cache[cache_key]

        url = HOLIDAY_API.format(zone=zone, year=year)
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                resp.raise_for_status()
                payload: dict[str, Any] = await resp.json()
        except aiohttp.ClientError as err:
            LOGGER.warning("Failed to fetch school holidays for %s %s: %s", zone, year, err)
            self._cache[cache_key] = []
            return []

        holidays: list[SchoolHoliday] = []
        for record in payload.get("records", []):
            fields = record.get("fields", {})
            start = dt_util.parse_datetime(fields.get("start_date"))
            end = dt_util.parse_datetime(fields.get("end_date"))
            name = fields.get("description", "Vacances scolaires")
            if not start or not end:
                continue
            holidays.append(
                SchoolHoliday(
                    name=name,
                    zone=zone,
                    start=dt_util.as_local(start),
                    end=dt_util.as_local(end),
                )
            )

        holidays.sort(key=lambda holiday: holiday.start)
        self._cache[cache_key] = holidays
        return holidays

    def clear(self) -> None:
        """Drop the local cache."""
        self._cache.clear()
