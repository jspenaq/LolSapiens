from fastapi import APIRouter
from backend.api.constants import s

basic_router = APIRouter()


@basic_router.get("/")
def root():
    return {"Status": "OK 🗿"}


@basic_router.get("/health-check")
def health_check():
    return {"Status": "Running faster than iwi's brain"}


@basic_router.get("/initial-data")
def get_initial_data():
    return s.get_initial_data()
