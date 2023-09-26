from fastapi import FastAPI
from app.routers.auth import auth_routers
from fastapi_jwt_auth import AuthJWT
from app.schemas.user import Settings

app = FastAPI()
app.include_router(auth_routers)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/")
async def root():
    return {"message": "FastApi ishladi"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
