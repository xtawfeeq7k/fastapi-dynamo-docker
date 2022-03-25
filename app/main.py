# framework
from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
# models
from app.controllers import router as controllers_router
# db
from app.database.__init__ import dynamo
# app
app = FastAPI()
app_auth = APIRouter()

# CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4040",
]
app.include_router(router=controllers_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def stratup_table():
    dynamo.create_users_table()
