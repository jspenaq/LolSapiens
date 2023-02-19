from fastapi import APIRouter
from backend.api.constants import s

basic_router = APIRouter()


@basic_router.get("/", tags=["/"])
def root():
    return {"Status": "OK 🗿"}


@basic_router.get("/health-check", tags=["/"])
def health_check():
    return {"Status": "Running faster than iwi's brain"}


@basic_router.get("/initial-data", tags=["/"])
def get_initial_data():
    return s.get_initial_data()
