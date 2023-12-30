import requests

headers = {"Content-Type": "application/json"}
r = requests.post(
    "http://127.0.0.1:5000/api/predict",
    json={
        "aso": False,
        "brand": "BMW",
        "capacity": 2993,
        "color": "Granatowy",
        "fuel_type": "Diesel",
        "horse_power": 258,
        "is_used": True,
        "mileage": 230000,
        "no_accidents": True,
        "number_of_doors": 5,
        "origin_country": "Unknown",
        "transmission": "Automatyczna",
        "year": 2014,
    },
    headers=headers,
)

print(r.status_code)
print(r.text)
