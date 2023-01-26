from lolsapiens.lolsapiens import getBuildGivenParams
from fastapi import FastAPI

# To run, install pandas at machine level, also FastApi
# Run using uvicorn server:app --reload
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def write_root():
    res = getBuildGivenParams(
        'Jax',
        'top',
        'gold_plus',
        'LethalTempo'
    )
    return res