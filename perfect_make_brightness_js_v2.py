import json
from datetime import datetime, timedelta
from skyfield.api import load, wgs84
import pytz

# -----------------------------
#  1) 도시 정보
# -----------------------------
CITIES = {
    "seoul":       (37.5665, 126.9780, "Asia/Seoul"),
    "tokyo":       (35.6895, 139.6917, "Asia/Tokyo"),
    "oslo":        (59.9139, 10.7522, "Europe/Oslo"),
    "stockholm":   (59.3293, 18.0686, "Europe/Stockholm"),
    "helsinki":    (60.1699, 24.9384, "Europe/Helsinki"),
    "reykjavik":   (64.1466, -21.9426, "Atlantic/Reykjavik"),
    "longyearbyen":(78.2232, 15.6469, "Arctic/Longyearbyen"),
    "new_york":    (40.7128, -74.0060, "America/New_York"),
    "sao_paulo":   (-23.5558, -46.6396, "America/Sao_Paulo"),
    "cape_town":   (-33.9249, 18.4241, "Africa/Johannesburg"),
}

START = datetime(2024, 12, 1)
END   = datetime(2025, 11, 30)

# -----------------------------
#  Skyfield load
# -----------------------------
ts = load.timescale()
eph = load('de421.bsp')
sun = eph['sun']


# -----------------------------
#  brightness model (C)
# -----------------------------
def compute_brightness(alt_deg: float) -> float:
    if alt_deg <= -6:
        return 0.0
    if alt_deg >= 45:
        return 1.0
    return (alt_deg + 6.0) / (45.0 + 6.0)


# -----------------------------
#  Main computation
# -----------------------------
data = {}

for city_id, (lat, lon, tzname) in CITIES.items():
    print(f"계산 중: {city_id} …")

    tz = pytz.timezone(tzname)

    dates = []
    values = []

    # 날짜 리스트 생성
    cur = START
    while cur <= END:
        dates.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)

    # 30분 단위 타임 스텝
    times = []
    for h in range(24):
        times.append(f"{h:02d}:00")
        times.append(f"{h:02d}:30")

    # 계산 반복
    for d in dates:
        row = []
        for t in times:
            dt_local = tz.localize(datetime.strptime(d + " " + t, "%Y-%m-%d %H:%M"))
            t_sf = ts.from_datetime(dt_local)

            # ⭐ 중요한 수정: Earth + location 로 observe!
            location = wgs84.latlon(lat, lon)
            alt, az, dist = (eph['earth'] + location).at(t_sf).observe(sun).apparent().altaz()

            alt_deg = alt.degrees
            b = compute_brightness(alt_deg)
            row.append(round(b, 6))

        values.append(row)

    # 데이터 저장
    data[city_id] = {
        "city_name": city_id.capitalize(),
        "dates": dates,
        "times": times,
        "values": values,
    }

# -----------------------------
#  Write output JS
# -----------------------------
with open("brightness_data.js", "w", encoding="utf-8") as f:
    f.write("window.BRIGHTNESS_DATA = ")
    json.dump(data, f, ensure_ascii=False)
    f.write(";\n")

print("완료! brightness_data.js 생성됨.")
