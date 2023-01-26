from lolsapiens.lolsapiens import getBuildGivenParams
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# To run, install pandas at machine level, also FastApi
# Run using uvicorn server:app --reload
app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def write_root():
    res = getBuildGivenParams(
        'Jax',
        'top',
        'gold_plus',
        'LethalTempo'
    )
    return res
