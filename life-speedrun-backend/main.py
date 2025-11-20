# main.py
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from models import User, ScheduleEvent
from schemas import UserCreate, UserOut, EventCreate, EventOut, VerifyCode  # ← добавлено VerifyCode
from auth import (
    get_password_hash,
    create_access_token,
    get_current_user,
    get_db,
    verify_password
)
from verification import generate_code, store_code, verify_code          # ← новые импорты
from email_utils import send_verification_email                         # ← новые импорты
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LyfeStyler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registration & Verification ---
@app.post("/register", status_code=201)
def register(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw, is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Генерация и отправка кода
    code = generate_code()
    store_code(user.email, code)
    background_tasks.add_task(send_verification_email, user.email, code)

    return {"msg": "Verification code sent to your email"}

@app.post("/verify")
def verify_email(data: VerifyCode, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    if verify_code(data.email, data.code):
        user.is_verified = True
        db.commit()
        return {"msg": "Email verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired code")


# --- Auth (login) ---
@app.post("/token")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- User Profile ---
@app.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# --- Events ---
@app.post("/events", response_model=EventOut)
def create_event(
    event: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_event = ScheduleEvent(
        user_id=current_user.id,
        title=event.title,
        start_time=event.startTime,
        end_time=event.endTime,
        date=event.date,
        is_range=event.isRange,
        is_recurring=event.isRecurring,
        recurrence_days=event.recurrenceDays,
        reminder=event.reminder,
        reminder_minutes=event.reminderMinutes,
        color=event.color,
        description=event.description,
        tags=json.dumps(event.tags)
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/events", response_model=list[EventOut])
def get_events(
    date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(ScheduleEvent).filter(
        ScheduleEvent.user_id == current_user.id,
        ScheduleEvent.date == date
    ).all()
    for ev in events:
        ev.tags = json.loads(ev.tags) if ev.tags else []
    return events