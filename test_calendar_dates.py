#!/usr/bin/env python3
"""Sandbox test to verify calendar date calculations for alternate_weekend custody type."""

from datetime import datetime, time, timedelta
from typing import Any

# Mock CustodyWindow
class CustodyWindow:
    def __init__(self, start: datetime, end: datetime, label: str, source: str = "pattern"):
        self.start = start
        self.end = end
        self.label = label
        self.source = source

# Mock configuration
CONF_ARRIVAL_TIME = "arrival_time"
CONF_DEPARTURE_TIME = "departure_time"
CONF_CUSTODY_TYPE = "custody_type"
CONF_REFERENCE_YEAR = "reference_year"
CONF_START_DAY = "start_day"

CUSTODY_TYPES = {
    "alternate_weekend": {
        "label": "Alternating Weekends",
        "cycle_days": 14,
        "pattern": [
            {"days": 12, "state": "off"},
            {"days": 2, "state": "on"},
        ],
    },
}

WEEKDAY_LOOKUP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

class MockScheduleManager:
    def __init__(self, config: dict[str, Any]):
        self._config = config
        self._arrival_time = self._parse_time(config.get(CONF_ARRIVAL_TIME, "16:15"))
        self._departure_time = self._parse_time(config.get(CONF_DEPARTURE_TIME, "19:00"))
    
    def _parse_time(self, time_str: str) -> time:
        """Parse time string like '16:15' to time object."""
        parts = time_str.split(":")
        return time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    
    def _apply_time(self, date: datetime, time_obj: time) -> datetime:
        """Apply time to a date."""
        return datetime.combine(date.date(), time_obj)
    
    def _reference_start(self, now: datetime, custody_type: str) -> datetime:
        """Calculate reference start date."""
        reference_year = self._config.get(CONF_REFERENCE_YEAR, "even")
        start_day = self._config.get(CONF_START_DAY, "friday")
        
        target_weekday = WEEKDAY_LOOKUP.get(start_day, 4)  # Default to Friday
        
        if custody_type == "alternate_weekend":
            # For alternate_weekend, find the Friday that starts the cycle
            # The cycle is 14 days: 12 off, 2 on
            # We need an anchor date to calculate from
            
            # Use a known reference: January 1, 2024 was a Monday
            # Find the first Friday of 2024
            anchor_year = 2024
            anchor = datetime(anchor_year, 1, 1)
            days_to_first_friday = (4 - anchor.weekday()) % 7
            if days_to_first_friday == 0:
                days_to_first_friday = 7
            first_friday_2024 = anchor + timedelta(days=days_to_first_friday)
            
            # Adjust based on reference year
            ref_year = now.year
            if reference_year == "even" and ref_year % 2 != 0:
                ref_year -= 1
            elif reference_year == "odd" and ref_year % 2 == 0:
                ref_year -= 1
            
            # Find first Friday of reference year
            ref_anchor = datetime(ref_year, 1, 1)
            days_to_ref_friday = (4 - ref_anchor.weekday()) % 7
            if days_to_ref_friday == 0:
                days_to_ref_friday = 7
            first_friday_ref = ref_anchor + timedelta(days=days_to_ref_friday)
            
            # Find the most recent Friday from now
            days_to_friday = (target_weekday - now.weekday()) % 7
            if days_to_friday == 0 and now.time() < self._arrival_time:
                days_to_friday = 0
            elif days_to_friday == 0:
                days_to_friday = 7
            
            candidate_friday = now + timedelta(days=days_to_friday)
            candidate_friday = candidate_friday.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate position in 14-day cycle
            days_since_ref = (candidate_friday - first_friday_ref).days
            cycle_position = days_since_ref % 14
            
            # Position 12-13 is the "on" period (Friday-Saturday of the weekend)
            # Position 0-11 is the "off" period
            if cycle_position < 12:
                # We're in the "off" period, find the next "on" Friday
                days_to_next_on = 12 - cycle_position
                candidate_friday += timedelta(days=days_to_next_on)
            elif cycle_position >= 14:
                # Wrap around
                candidate_friday += timedelta(days=14 - cycle_position + 12)
            
            return candidate_friday
        
        # For other custody types, use the original logic
        days_back = (now.weekday() - target_weekday) % 7
        if days_back == 0 and now.time() < self._arrival_time:
            days_back = 7
        
        base_date = now - timedelta(days=days_back)
        base_date = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return base_date
    
    def _generate_pattern_windows(self, now: datetime) -> list[CustodyWindow]:
        """Create repeating windows from the selected custody type."""
        custody_type = self._config.get(CONF_CUSTODY_TYPE, "alternate_week")
        type_def = CUSTODY_TYPES.get(custody_type) or CUSTODY_TYPES["alternate_weekend"]
        horizon = now + timedelta(days=90)
        
        cycle_days = type_def["cycle_days"]
        pattern = type_def["pattern"]
        windows: list[CustodyWindow] = []
        reference_start = self._reference_start(now, custody_type)
        pointer = reference_start
        
        print(f"\n📅 Reference start: {reference_start} ({reference_start.strftime('%A')})")
        print(f"📅 Current time: {now} ({now.strftime('%A')})")
        print(f"📅 Horizon: {horizon}")
        print(f"📅 Pattern: {pattern}")
        print(f"📅 Cycle days: {cycle_days}")
        print()
        
        window_count = 0
        while pointer < horizon and window_count < 5:  # Limit to 5 windows for testing
            offset = timedelta()
            for segment in pattern:
                segment_start = pointer + offset
                # For alternate_weekend with 2 days "on", it means:
                # - Day 0: Friday (arrival)
                # - Day 1: Saturday  
                # - Day 2: Sunday (departure)
                # So we need segment_start + 2 days to get to Sunday
                # But wait, if days=2, that's Friday+Saturday, we need Sunday
                # So for weekend, if days=2, we actually want 3 days: Fri, Sat, Sun
                if custody_type == "alternate_weekend" and segment["state"] == "on":
                    # Weekend: Friday to Sunday = 3 days
                    segment_end = segment_start + timedelta(days=2)  # Fri -> Sun (Fri=0, Sat=1, Sun=2)
                else:
                    # For other cases, if segment is N days, it spans from day 0 to day N-1
                    segment_end = segment_start + timedelta(days=segment["days"] - 1)
                
                if segment["state"] == "on":
                    window_start = self._apply_time(segment_start, self._arrival_time)
                    window_end = self._apply_time(segment_end, self._departure_time)
                    
                    windows.append(
                        CustodyWindow(
                            start=window_start,
                            end=window_end,
                            label="Custody period",
                        )
                    )
                    
                    window_count += 1
                    print(f"✅ Window {window_count}:")
                    print(f"   Start: {window_start} ({window_start.strftime('%A %d %B %Y à %H:%M')})")
                    print(f"   End:   {window_end} ({window_end.strftime('%A %d %B %Y à %H:%M')})")
                    print(f"   Duration: {(window_end - window_start).total_seconds() / 86400:.2f} days")
                    print()
                
                offset += timedelta(days=segment["days"])
            pointer += timedelta(days=cycle_days)
        
        return windows

def main():
    print("🧪 Testing Calendar Date Calculations for Alternate Weekend")
    print("=" * 70)
    
    # Configuration: vendredi 18 déc arrivée, dimanche 21 déc retour
    config = {
        CONF_CUSTODY_TYPE: "alternate_weekend",
        CONF_ARRIVAL_TIME: "16:15",  # Vendredi 18 déc à 16:15
        CONF_DEPARTURE_TIME: "19:00",  # Dimanche 21 déc à 19:00
        CONF_REFERENCE_YEAR: "even",  # Année paire
        CONF_START_DAY: "friday",  # Commence le vendredi
    }
    
    print(f"\n⚙️  Configuration:")
    print(f"   Custody type: {config[CONF_CUSTODY_TYPE]}")
    print(f"   Arrival time: {config[CONF_ARRIVAL_TIME]}")
    print(f"   Departure time: {config[CONF_DEPARTURE_TIME]}")
    print(f"   Reference year: {config[CONF_REFERENCE_YEAR]}")
    print(f"   Start day: {config[CONF_START_DAY]}")
    
    # Current time: 16 décembre 2025, 22:00
    now = datetime(2025, 12, 16, 22, 0, 0)
    
    manager = MockScheduleManager(config)
    windows = manager._generate_pattern_windows(now)
    
    print("\n" + "=" * 70)
    print(f"\n📊 RESULT: Generated {len(windows)} windows")
    
    # Check the first window (should be the next one)
    if windows:
        first_window = windows[0]
        print(f"\n🎯 First window (next custody period):")
        print(f"   Start: {first_window.start.strftime('%A %d %B %Y à %H:%M')}")
        print(f"   End:   {first_window.end.strftime('%A %d %B %Y à %H:%M')}")
        
        # Expected: vendredi 18 déc à 16:15 → dimanche 20 déc à 19:00
        # Or: vendredi 18 déc à 16:15 → dimanche 21 déc à 19:00 ?
        expected_start = datetime(2025, 12, 18, 16, 15)
        expected_end = datetime(2025, 12, 21, 19, 0)
        
        print(f"\n✅ Expected:")
        print(f"   Start: {expected_start.strftime('%A %d %B %Y à %H:%M')}")
        print(f"   End:   {expected_end.strftime('%A %d %B %Y à %H:%M')}")
        
        if first_window.start.date() == expected_start.date() and first_window.start.time() == expected_start.time():
            print(f"\n✅ Start date is CORRECT!")
        else:
            print(f"\n❌ Start date is INCORRECT!")
            print(f"   Expected: {expected_start}")
            print(f"   Got:      {first_window.start}")
        
        if first_window.end.date() == expected_end.date() and first_window.end.time() == expected_end.time():
            print(f"✅ End date is CORRECT!")
        else:
            print(f"❌ End date is INCORRECT!")
            print(f"   Expected: {expected_end}")
            print(f"   Got:      {first_window.end}")

if __name__ == "__main__":
    main()

