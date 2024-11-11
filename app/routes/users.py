import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import UserData 

router = APIRouter()

SECRET_KEY = "4b340366f20f5e2f9325f4e6ebf05f65ed346e7afbecc4d6f308255c5e26e36f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

FAKE_API_BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"

# Configura o esquema de segurança OAuth2 com "Bearer Token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")  # Ajustado aqui

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "user": {"username": "user", "role": "user", "password": "L0XuwPOdS5U"},
    "admin": {"username": "admin", "role": "admin", "password": "JKSipm0YH"},
}

def get_fake_service_token(username, password):
    params = {
        "username": username,
        "password": password
    }
    response = requests.post(
        f"{FAKE_API_BASE_URL}/token",
        params=params, 
        verify=False 
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise HTTPException(status_code=401, detail="Unable to authenticate with external service")

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not verify_password(form_data.password, user_dict["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"], "role": user_dict["role"], "password": user_dict["password"]}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        password: str = payload.get("password") 
        if username is None or role is None or password is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "role": role, "password": password}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/user")
async def read_user_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    fake_service_token = get_fake_service_token(current_user["username"], current_user["password"])
    headers = {"Authorization": f"Bearer {fake_service_token}"}
    response = requests.get(f"{FAKE_API_BASE_URL}/user", headers=headers, verify=False)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from external service")
    
    save_fake_data(db, current_user["username"], current_user["role"], response.json())
    
    return response.json()

@router.get("/admin")
async def read_admin_data(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted")

    fake_service_token = get_fake_service_token(current_user["username"], current_user["password"])
    headers = {"Authorization": f"Bearer {fake_service_token}"}
    response = requests.get(f"{FAKE_API_BASE_URL}/admin", headers=headers, verify=False)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from external service")
    
    save_fake_data(db, current_user["username"], current_user["role"], response.json())
    
    return response.json()

@router.get("/local_data")
async def get_local_data(db: Session = Depends(get_db)):
    data = db.query(UserData).all()
    return data

def save_fake_data(db: Session, username: str, role: str, data: dict):
    user_data = UserData(username=username, role=role, data=data)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data
