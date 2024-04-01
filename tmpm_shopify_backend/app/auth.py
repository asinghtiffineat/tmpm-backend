from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
from .dependencies import get_db
from .models import ShopifyStore
from dotenv import load_dotenv
import os
import requests
import hmac
import hashlib

# Load environment variables
load_dotenv()

# Constants
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SCOPES = os.getenv("SHOPIFY_SCOPES", "read_products,write_products")
REDIRECT_URI = os.getenv("SHOPIFY_REDIRECT_URI", "https://yourapp.com/auth/shopify/callback")
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> ShopifyStore:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        shop: str = payload.get("sub")
        if shop is None:
            raise credentials_exception
        shopify_store = db.query(ShopifyStore).filter(ShopifyStore.shop == shop).first()
        if shopify_store is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return shopify_store

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_shopify_hmac(hmac_to_verify: str, query: dict) -> bool:
    """
    Verify Shopify HMAC
    """
    message = "&".join([f"{key}={value}" for key, value in query.items() if key != 'hmac'])
    secret = SHOPIFY_API_SECRET.encode()
    generated_hash = hmac.new(secret, msg=message.encode(), digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(generated_hash, hmac_to_verify)

def generate_install_redirect_url(shop: str) -> str:
    query_params = {
        "client_id": SHOPIFY_API_KEY,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI
    }
    return f"https://{shop}/admin/oauth/authorize?" + "&".join([f"{key}={value}" for key, value in query_params.items()])

@router.get("/auth/shopify")
def authenticate_shopify(shop: str):
    return {"url": generate_install_redirect_url(shop)}

@router.get("/auth/shopify/callback")
async def shopify_auth_callback(request: Request, shop: str, code: str, hmac: str, db: Session = Depends(get_db)):
    query_params = dict(request.query_params)
    if not verify_shopify_hmac(hmac, query_params):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid HMAC signature.")

    try:
        response = requests.post(
            f"https://{shop}/admin/oauth/access_token",
            data={"client_id": SHOPIFY_API_KEY, "client_secret": SHOPIFY_API_SECRET, "code": code},
        )
        response.raise_for_status()
        response_data = response.json()
        access_token = response_data.get("access_token")

        shopify_store = ShopifyStore(shop=shop, access_token=access_token)
        db.add(shopify_store)
        db.commit()
        db.refresh(shopify_store)

        jwt_token = create_access_token(data={"sub": shop}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "jwt_token": jwt_token, "token_type": "bearer"}
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
