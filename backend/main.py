from fastapi import FastAPI, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from . import models, schemas
import requests

app = FastAPI()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "WhatsApp Message Scheduler API is running."}

# Recipient Endpoints
@app.post("/recipients/", response_model=schemas.RecipientOut)
def create_recipient(recipient: schemas.RecipientCreate, db: Session = Depends(get_db)):
    db_recipient = models.Recipient(**recipient.dict())
    db.add(db_recipient)
    db.commit()
    db.refresh(db_recipient)
    return db_recipient

@app.get("/recipients/", response_model=list[schemas.RecipientOut])
def read_recipients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Recipient).offset(skip).limit(limit).all()

@app.get("/recipients/{recipient_id}", response_model=schemas.RecipientOut)
def read_recipient(recipient_id: int, db: Session = Depends(get_db)):
    db_recipient = db.query(models.Recipient).filter(models.Recipient.id == recipient_id).first()
    if not db_recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return db_recipient

@app.put("/recipients/{recipient_id}", response_model=schemas.RecipientOut)
def update_recipient(recipient_id: int, recipient: schemas.RecipientUpdate, db: Session = Depends(get_db)):
    db_recipient = db.query(models.Recipient).filter(models.Recipient.id == recipient_id).first()
    if not db_recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    for var, value in vars(recipient).items():
        if value is not None:
            setattr(db_recipient, var, value)
    db.commit()
    db.refresh(db_recipient)
    return db_recipient

@app.delete("/recipients/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(recipient_id: int, db: Session = Depends(get_db)):
    db_recipient = db.query(models.Recipient).filter(models.Recipient.id == recipient_id).first()
    if not db_recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    db.delete(db_recipient)
    db.commit()
    return None 

def send_whatsapp_message(to: str, message: str):
    url = "http://localhost:3001/send"
    payload = {"to": to, "message": message}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception("Failed to send WhatsApp message")

@app.post("/send_whatsapp/")
def send_whatsapp(
    to: str = Body(..., embed=True),
    message: str = Body(..., embed=True)
):
    try:
        send_whatsapp_message(to, message)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 