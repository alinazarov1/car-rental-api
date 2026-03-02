from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel

app=FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

class CarSchema(BaseModel):
    brand: str
    model: str
    price_per_day: int

    class Config:
        from_attributes = True
@app.get("/cars")
def get_cars(db:Session = Depends(get_db)):
    return db.query(models.Car).all()
@app.post("/cars")
def add_cars(car: CarSchema,db: Session=Depends(get_db)):
    new_car = models.Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car
@app.get("/cars/{car_id}")
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        return {"error":"Car not found"}
    return car
@app.put("/cars/{car_id}")
def update_car(car_id: int, updated_car: CarSchema,db: Session = Depends(get_db)):
    car =  db.query(models.Car).filter(models.Car.id==car_id).first()
    if car is None:
        return {"error":"Car not found"}
    for key, value in updated_car.dict().items():
        setattr(car,key,value)
    db.commit()
    return{"message":"Car updated successfully"}
@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        return {"error": "Car not found"}
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}




