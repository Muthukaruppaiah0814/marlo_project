import requests
from app.database import SessionLocal, VesselData
from datetime import datetime

def get_data_from_third_party():
    url = "https://12af-14-97-224-214.ngrok-free.app/index"
    response = requests.get(url)

    if response.status_code == 200:
        print("Going to store data into the database")
        data = response.json()
        store_data_into_db(data)
    else:
        print("Failed to fetch data:", response.status_code)

def store_data_into_db(data):
    db = SessionLocal()
    try:
        for item in data:
            vessel = VesselData(
                id=item['id'],
                name=item['name'],
                group=item['group'],
                date=datetime.strptime(item['date'], '%Y-%m-%d').date(),
                value=item['value']
            )
            db.add(vessel)
        db.commit()
        print("Data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Failed to insert data: {e}")
    finally:
        db.close()
