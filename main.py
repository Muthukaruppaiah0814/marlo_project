from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.dbmodel import VesselData as DBVesselData
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.fetch_data import get_data_from_third_party
from app.database import Base
from app import schema
from app import crud
from datetime import datetime

app = FastAPI()

scheduler = BackgroundScheduler()


scheduler.add_job(
    get_data_from_third_party,
    CronTrigger(hour=0, minute=0),
)

scheduler.start()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully on startup.")

@app.get("/vessel_data/{vessel_name}", response_model=schema.VesselDataSchema)
def get_vessel_data(db: Session = Depends(get_db),start_date: str = Query(...),end_date: str = Query(...)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    db_vessel_data = crud.get_vessel_data_by_name(db, vessel_name, start_date, end_date)
    if db_vessel_data is None:
        raise HTTPException(status_code=404, detail="Vessel data not found")
    return db_vessel_data

@app.get("/vessel_data", response_model=schema.VesselDataSchema)
def get_vessel_data(db: Session = Depends(get_db),mail: str = Query(...)):
    role = crud.get_role(db, mail)
    db_vessel_data = crud.get_vessel_data_by_id(db, role)
    if db_vessel_data is None:
        raise HTTPException(status_code=404, detail="Sending webhook response of Vessel data not found")
    return db_vessel_data

@app.get("/all_vessel_data", response_model=list[schema.VesselDataSchema])
def get_all_vessel_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),mail: str = Query(...)):
    role = crud.get_role(db, mail)
    if role == 'admin':
        vessel_data = crud.get_all_vessel_data(db, skip=skip, limit=limit)
    else:
        return "Admin only have rights to see all data"
    return vessel_data

@app.delete("/vessel_data", response_model=schema.VesselDataSchema)
def delete_vessel_data(db: Session = Depends(get_db),mail: str = Query(...)):
    role = crud.get_role(db, mail)
    db_vessel_data = crud.delete_vessel_data(db, role)
    if db_vessel_data is None:
        raise HTTPException(status_code=404, detail="Webhook response of Vessel data not found")
    return db_vessel_data


