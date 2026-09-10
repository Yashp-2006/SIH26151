import pandas as pd
from shared.contracts import EvidenceCandidate

def temporal_overlap(events_a: list[str], events_b: list[str], window_days: int) -> float:
    if not events_a or not events_b:
        return 0.0
    a = pd.to_datetime(events_a)
    b = pd.to_datetime(events_b)
    
    overlaps = 0
    for t_a in a:
        if ((b >= t_a - pd.Timedelta(days=window_days)) & (b <= t_a + pd.Timedelta(days=window_days))).any():
            overlaps += 1
            
    return overlaps / len(a)
