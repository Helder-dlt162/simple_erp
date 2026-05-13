from fastapi import APIRouter, Response
import jwt, datetime
import config

router = APIRouter(prefix="/auth", tags=["auth"])
SECRET = config.auth_config["JWT_SECRET"]

@router.post("/login")
def login(response: Response, email: str, senha: str):
    # valida no banco (exemplo fake)
    if email != "a@a.com" or senha != "123":
        return {"erro": "inválido"}

    payload = {
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {"ok": True}