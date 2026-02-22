import asyncio
import aiohttp
import os
import sys
from datetime import datetime
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock homeassistant before importing
import sys
from unittest.mock import MagicMock

class MockAiohttpClient:
    @staticmethod
    def async_get_clientsession(hass):
        return aiohttp.ClientSession()

sys.modules['homeassistant.helpers.aiohttp_client'] = MockAiohttpClient()

from custom_components.custody_schedule.school_holidays import SchoolHolidayClient
from custom_components.custody_schedule.schedule import CustodyScheduleManager
from homeassistant.util import dt as dt_util

async def main():
    # Setup mock HA
    hass = MagicMock()
    
    # We set time_zone to Europe/Paris, similar to what a European user would have
    hass.config.time_zone = "Europe/Paris"
    dt_util.set_default_time_zone(dt_util.get_time_zone("Europe/Paris"))
    
    client = SchoolHolidayClient(hass)

    tests = [
        {"country": "FR", "zone": "C", "year": 2024},
        {"country": "BE", "zone": "FR", "year": 2024},
        {"country": "CH", "zone": "CH-GE", "year": 2024},
        {"country": "LU", "zone": "", "year": 2024},
        {"country": "CA_QC", "zone": "QC", "year": 2024},
    ]

    # Create session
    client._session = aiohttp.ClientSession()

    try:
        for t in tests:
            country = t["country"]
            zone = t["zone"]
            year = t["year"]
            
            print(f"\\n--- Testing {country} Zone: {zone} Year: {year} ---")
            
            holidays = await client.async_list(country, zone, year)
            print(f"Found {len(holidays)} holidays:")
            for h in holidays[:5]: # Print first 5
                print(f"  {h.name} | Start: {h.start.isoformat()} | End: {h.end.isoformat()}")
                
            if len(holidays) > 0:
                # Test the split logic using CustodyScheduleManager
                config_parent_a_odd_first = {
                    "country": country,
                    "zone": zone,
                    "vacation_split_mode": "odd_first",
                    "school_level": "primary",
                    "custody_type": "alternate_weekend", 
                    "reference_year_custody": "even",
                    "arrival_time": "16:15",
                    "departure_time": "19:00"
                }
                
                manager = CustodyScheduleManager(hass, config_parent_a_odd_first, client)
                
                # Fetch periods for 2024-2025
                periods = await manager.async_get_vacation_periods()
                print(f"Calculated vacation periods for Parent A (odd_first) [showing up to 5]:")
                for p in periods[:5]:
                    start_str = p.start.isoformat()
                    end_str = p.end.isoformat()
                    print(f"  {p.name} | {start_str} to {end_str}")
                    
    finally:
        await client._session.close()

if __name__ == "__main__":
    asyncio.run(main())
