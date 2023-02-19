from jose import JWSError, jwt
import schemas, database, models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# ALGORITHM
# EXPRIATION TIME OF TOKEN

SECRET_KEY = "09cfbit7h5ihvhvipu9e4t74t845yth8rvh745gh547gh45ghd7rfg4h75gh785"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# access token -> contain a pyload -> whatever the data we want to send -> pass into dictionary
def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str, credentials_exception):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)

    except JWSError:
        raise credentials_exception

    return token_data

# pass dependancy -> take token -> verify token -> extract id -> automatically fetch the user from the database added into path operation function
def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
