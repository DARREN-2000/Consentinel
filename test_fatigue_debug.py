from datetime import datetime, timedelta, timezone

def calculate_fatigue_score(recent_count, engaged_count):
    if recent_count == 0:
        return 0.0

    engagement_rate = engaged_count / recent_count if recent_count > 0 else 0.0
    volume_factor = min(recent_count / 10.0, 1.0)
    fatigue = volume_factor * (1.0 - engagement_rate)

    return round(min(max(fatigue, 0.0), 1.0), 4)

print(calculate_fatigue_score(12, 0))
