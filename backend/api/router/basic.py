from fastapi import APIRouter


basic_router = APIRouter()


@basic_router.get("/")
def root():
    return {"Status": "OK"}


@basic_router.get("/healthcheck")
def health_check():
    return {"Status": "Running faster than iwi's brain"}
