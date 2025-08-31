from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr #for correct validation and json responses, schemas for validation
#email specific validation
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
#connects to mysql database and can run commands with python classes
from sqlalchemy.ext.declarative import declarative_base
# creates a base class for orm models
from sqlalchemy.orm import sessionmaker, Session
#factory to create db sessions, typehint for db injections

# Database connection URL 
DATABASE_URL = "mysql+pymysql://fastapi_user:strongpassword@localhost/fastapi_db"

engine = create_engine(DATABASE_URL, echo=True)  # doorway to database,echo=True to log SQL queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #blue print registery for all orm models

app = FastAPI()

# ORM Model for User table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)
    emailID = Column(String(100), unique=True, index=True)  # Unique & indexed

# Create the table if not exists
Base.metadata.create_all(bind=engine)

# Pydantic model for input/output validation
class UserCreate(BaseModel):
    name: str
    age: int
    emailID: EmailStr

class UserOut(BaseModel):
    id: int
    name: str
    age: int
    emailID: EmailStr

    class Config:
        orm_mode = True  #means it can read data directly from ORM objects

# Dependency to get DB session per request as in it wont expect the client to give all the detail, instead it will use 
# session and inject the databases
# like a library card,aitomatic route handlers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint to register user
@app.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.emailID == user.emailID).first()
    if existing_user:
        raise HTTPException(status_code=454, detail="EmailID already exists.")

    new_user = User(name=user.name, age=user.age, emailID=user.emailID)
    db.add(new_user)
    db.commit() #after add,still in SQL alch session, gotta commit to  make the changes in mysql db
    db.refresh(new_user) #so that user object keeps track of the stuff at the same time

    return {"message": "User registered successfully", "user_id": new_user.id}

# GET endpoint to return all users
@app.get("/users", response_model=list[UserOut]) #response thing is where FastAPI converts all user objects to json
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Optional root endpoint for quick test
@app.get("/")
def root():
    return {"message": "FastAPI MySQL user registration API is running."}


#mysql -u fastapi_user -p -h 127.0.0.1 -P 3306 
#uvicorn swa1:app --reload
#lsof -i :8000
#kill -9 PID