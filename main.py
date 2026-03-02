from fastapi import FastAPI
from pydantic import BaseModel
class Car(BaseModel):
    id:int
    brand:str
    model:str
    price_per_day:int
app = FastAPI()

@app.get("/")
def home():
    return {"message":"Car Rental API is running!"}


cars = [
    {"id":1,"brand":"Toyota","model":"Cramy","price_per_day":50},
    {"id":2,"brand":"BMW","model":"X5","price_per_day":120},
    {"id":3,"brand":"Honda","model":"Civic","price_per_day":40},
]
@app.get("/cars")
def get_cars():
    return cars
@app.get("/cars/{car_id}")
def get_car(car_id:int):
    for car in cars:
        if car["id"] == car_id:
            return car
    return {"error":"Car not found"}
@app.post("/cars")
def add_car(car:Car):
    cars.append(car.dict())
    return{"message":"Car added successfully","car":car}
@app.delete("/cars/{car_id}")
def delete_car(car_id:int):
    for car in cars:
        if car["id"] == car_id:
            cars.remove(car)
            return {"message":"Car deleted successfully"}
    return {"error":"Car not found"}
@app.put("/cars/{car_id}")
def update_car(car_id : int, updated_car: Car):
    for car in cars:
        if car["id"] == car_id:
            car.update(updated_car.dict())
            return {"message":"Car updated succesfully"}
    return {"error":"Car not found"}