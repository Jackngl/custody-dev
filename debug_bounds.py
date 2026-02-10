
from datetime import datetime, time, timedelta
import zoneinfo
from dataclasses import dataclass

def compute_bounds(holiday, arrival_time, departure_time, end_day):
    WEEKDAY_LOOKUP = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
    
    start_dt = holiday.start
    end_dt = holiday.end

    start_date = start_dt.date()
    end_date = end_dt.date()

    # Log API dates
    print(f"DEBUG: API Start: {start_dt} ({start_dt.strftime('%A')})")
    print(f"DEBUG: API End:   {end_dt} ({end_dt.strftime('%A')})")

    if end_dt.hour == 0 and end_dt.minute == 0 and end_dt.second == 0:
        end_date = end_date - timedelta(days=1)
        print(f"DEBUG: 00:00 detected, end_date shifted to {end_date}")

    effective_start_date = start_date
    while effective_start_date.weekday() != 4:  # Friday
        effective_start_date -= timedelta(days=1)
    print(f"DEBUG: Effective Start Date (Friday): {effective_start_date}")

    target_end_weekday = WEEKDAY_LOOKUP.get(end_day, 6)
    effective_end_date = end_date

    # --- CURRENT LOGIC ---
    if end_dt.hour == 0 and end_dt.minute == 0:
        print("DEBUG: School reprise detected. NO SHIFT to transition day.")
        pass 
    else:
        print(f"DEBUG: Regular end. Shifting to {end_day} (target={target_end_weekday})")
        while effective_end_date.weekday() != target_end_weekday:
            effective_end_date += timedelta(days=1)
    # -------------------

    effective_start = datetime.combine(effective_start_date, arrival_time, start_dt.tzinfo)
    effective_end = datetime.combine(effective_end_date, departure_time, end_dt.tzinfo)

    midpoint = effective_start + (effective_end - effective_start) / 2
    
    return effective_start, effective_end, midpoint

@dataclass
class SchoolHoliday:
    name: str
    zone: str
    start: datetime
    end: datetime

def test():
    # User's likely config: end_day=sunday, departure=19:00
    arrival_time = time(8, 0)
    departure_time = time(19, 0)
    end_day = "sunday" 
    
    tz = zoneinfo.ZoneInfo("Europe/Paris")
    # Summer 2026 Zone C
    holiday_start = datetime(2026, 7, 4, 0, 0, tzinfo=tz) 
    holiday_end = datetime(2026, 9, 1, 0, 0, tzinfo=tz) # Tuesday Sept 1st
    
    holiday = SchoolHoliday("Vacances d'Été", "C", holiday_start, holiday_end)
    
    eff_start, eff_end, midpoint = compute_bounds(holiday, arrival_time, departure_time, end_day)
    
    print("-" * 30)
    print(f"Effective Start: {eff_start} ({eff_start.strftime('%A')})")
    print(f"Effective End:   {eff_end} ({eff_end.strftime('%A')})")
    print(f"Midpoint:        {midpoint} ({midpoint.strftime('%A')})")
    print("-" * 30)

if __name__ == "__main__":
    test()
