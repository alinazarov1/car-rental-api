from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token, verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://car-rental-frontend-eta-nine.vercel.app",
        "https://car-rental-frontend-5agxmofsj-alinazarov1s-projects.vercel.app",
        "https://car-rental-frontend-git-main-alinazarov1s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

class CarSchema(BaseModel):
    brand: str
    model: str
    price_per_day: int

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    username: str
    password: str

@app.get("/cars")
def get_cars(db:Session = Depends(get_db)):
    return db.query(models.Car).all()

@app.post("/cars")
def add_cars(car: CarSchema,db: Session=Depends(get_db),current_user: str = Depends(get_current_user)):
    new_car = models.Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@app.get("/cars/{car_id}")
def get_car(car_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        return {"error":"Car not found"}
    return car


@app.put("/cars/{car_id}")
def update_car(car_id: int, updated_car: CarSchema,db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    car =  db.query(models.Car).filter(models.Car.id==car_id).first()
    if car is None:
        return {"error":"Car not found"}
    for key, value in updated_car.dict().items():
        setattr(car,key,value)
    db.commit()
    return{"message":"Car updated successfully"}


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car is None:
        return {"error": "Car not found"}
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        return {"error": "Username already exists"}
    new_user = models.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user:UserSchema,db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return{"error":"Invalid username or password"}
    token = create_access_token(data={"sub":db_user.username})
    return {"access_token": token, "token_type": "bearer"}
