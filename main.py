from fastapi import FastAPI
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app= FastAPI()
app.include_router(auth_router)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/")
async def home():
    return {
        "message":"Healthy message!!!",
        'login':auth_router.url_path_for('login'),
        'signup':auth_router.url_path_for('signup')
    }