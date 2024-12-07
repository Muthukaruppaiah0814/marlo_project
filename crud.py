from sqlalchemy.orm import Session
from app.dbmodel import VesselData as DBVesselData, User as DBUser



def get_role(db:Session, mail:str):
    return db.query(DBUser).filter(DBUser.mail == mail).first()
def get_vessel(db: Session, role: str):
    return db.query(DBVesselData).filter(DBVesselData.group == role)

def get_vessel_data_by_name(db: Session, name: str, start_date: str, end_date: str):
    return db.query(models.VesselData).filter(models.VesselData.date >= start_date, models.VesselData.date <= end_date)

def get_all_vessel_data(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBVesselData).offset(skip).limit(limit).all()

def delete_vessel(db: Session, role: str):
    db_vessel = db.query(DBVesselData).filter(DBVesselData.group == role).first()
    if db_vessel:
        db.delete(db_vessel)
        db.commit()
        return db_vessel
    return None
