
from datetime import datetime, time, timedelta
import zoneinfo

def simulate_split(start_dt, end_dt, mode="half"):
    duration = end_dt - start_dt
    print(f"Total Duration: {duration}")
    
    if mode == "half":
        midpoint = start_dt + duration / 2
        return [
            (start_dt, midpoint, "1ère moitié"),
            (midpoint, end_dt, "2ème moitié")
        ]
    elif mode == "quarter":
        seg = duration / 4
        return [
            (start_dt, start_dt + seg, "1/4"),
            (start_dt + seg, start_dt + 2*seg, "2/4"),
            (start_dt + 2*seg, start_dt + 3*seg, "3/4"),
            (start_dt + 3*seg, end_dt, "4/4")
        ]
    return []

def run_scenarios():
    tz = zoneinfo.ZoneInfo("Europe/Paris")
    # Simulation parameters for 2026
    arrival = time(16, 15) # Pickup at school Friday July 3
    departure = time(19, 0)
    
    # Effective bounds as per code
    start = datetime(2026, 7, 3, 16, 15, tzinfo=tz) 
    end = datetime(2026, 8, 31, 19, 0, tzinfo=tz) 
    
    print("=== SCENARIO 1: HALF SPLIT (50/50) ===")
    parts = simulate_split(start, end, "half")
    for s, e, l in parts:
        print(f"{l}: {s.strftime('%d %b %H:%M')} -> {e.strftime('%d %b %H:%M')}")
        
    print("\n=== SCENARIO 2: QUARTER SPLIT (Quinzaines) ===")
    parts = simulate_split(start, end, "quarter")
    for s, e, l in parts:
        print(f"{l}: {s.strftime('%d %b %H:%M')} -> {e.strftime('%d %b %H:%M')}")

    print("\n=== SCENARIO 3: FIXED AUG 1st MIDPOINT (Hypothetical) ===")
    mid = datetime(2026, 8, 1, 0, 0, tzinfo=tz)
    print(f"1ère moitié: {start.strftime('%d %b %H:%M')} -> {mid.strftime('%d %b %H:%M')}")
    print(f"2ème moitié: {mid.strftime('%d %b %H:%M')} -> {end.strftime('%d %b %H:%M')}")

if __name__ == "__main__":
    run_scenarios()
