from fastapi import FastAPI, HTTPException, Request, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import crud
from jose import jwt
import hashlib


app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Fonctions utiles :
def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

def decoder_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def verifier_token(req: Request):
    token = req.headers["Authorization"]

# Classes contenu
class UserRegister(BaseModel):
    username:str
    firstname:str
    lastname:str
    mail:str
    password:str

class UserLogin(BaseModel):
    mail:str
    password:str

class ActionCreate(BaseModel):
    company:str
    value:float

class ActionResponse(BaseModel):
    id:int
    company:str
    value:float

class UserActionCreate(BaseModel):
    action_id:int
    bought_value:float

class UserActionResponse(BaseModel):
    id:int
    action_id:int
    bought_value:float
    bought_time:str
    sold:bool
    sold_value:float = None
    sold_time:str = None

class UserFollowCreate(BaseModel):
    user_id_followed:int

class UserFollowResponse(BaseModel):
    user_id_following:int
    user_id_followed:int

class ActionValueChangeCreate(BaseModel):
    action_id:int
    value:float

class ActionValueChangeResponse(BaseModel):
    id:int
    action_id:int
    time:str
    value:float

app = FastAPI()

# Début des endpoints

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/auth/inscription")
async def inscription(user:UserRegister):
    if len(crud.get_users_by_mail(user.mail)) > 0:
        raise HTTPException(status_code=403, detail="L'email fourni possède déjà un compte")
    else:
        id_user = crud.create_user(user.username, user.firstname, user.lastname, user.mail, hasher_mdp(user.password), None)
        token = jwt.encode({
            "email" : user.mail,
            "mdp" : user.password,
            "id" : id_user
        # ici ajouter la date de creation du token pour augmenter la secu
        }, SECRET_KEY, algorithm=ALGORITHM)
        crud.update_token(id_user, token)
        return {"token" : token}

@app.post("/api/auth/token")
async def login_token(user:UserLogin):
    resultat = crud.get_jwt_from_mail_password(user.mail, hasher_mdp(user.password))
    if resultat is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe invalide")
    else:
        return {"token":resultat[0]}
    
@app.get("/api/articles")
async def mes_articles(req: Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        # ici verif si le token exist ds la base de donnee
        return {"id_user" : crud.get_user_id_from_mail(decode["email"])[0]}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")


# voir les actions d un utilisateur
@app.get("/api/user/actions")
async def get_user_actions(user_id: int, req: Request):
    try:
        # Vérification de l'authentification de l'utilisateur
        verifier_token(req)

        # Récupération de la liste des actions de l'utilisateur
        actions = crud.get_actions_by_user_id(user_id)

        # Vérification que l'utilisateur a bien des actions
        if actions is None:
            raise HTTPException(status_code=404, detail="Cet utilisateur ne possède aucune action")

        return {"actions": actions}

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# voir les actions d un utilisateur suivi
@app.get("/api/actions/followed/{user_id_followed}")
async def get_actions_by_user_id_followed(user_id_followed: int, req: Request):
    try:
        # Vérification de l'authentification
        decode = verifier_token(req)
        # Récupération de l'ID de l'utilisateur connecté
        id_user = crud.get_user_id_from_mail(decode["email"])[0]
        # Récupération de la liste des actions suivies par l'utilisateur
        actions_followed = crud.get_actions_by_user_id_followed(user_id_followed, id_user)
        return {"actions_followed": actions_followed}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifié pour accéder à cet endpoint")


# pour suivre un utilisateur
@app.post("/api/user/{user_id_following}/follow/{user_id_followed}")
async def follow_user(user_id_following: int, user_id_followed: int, req: Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        if decode["id"] != user_id_following:
            raise HTTPException(status_code=403, detail="Vous ne pouvez pas suivre cet utilisateur")
        else:
            crud.create_user_user(user_id_following, user_id_followed)
            return {"message": "Vous suivez maintenant l'utilisateur avec l'ID : {}".format(user_id_followed)}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur : {}".format(str(e)))
