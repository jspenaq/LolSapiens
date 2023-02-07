# from backend.lolsapiens.lcu.lcu_connection import main_loop
import os
import uvicorn
from backend.api.lol_scraper import main
from backend.api.router.basic import basic_router
from backend.api.router.bans import bans_router
from backend.api.router.build import build_router
from backend.api.router.picks import picks_router
from backend.api.utils import create_parser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basic_router)
app.include_router(bans_router)
app.include_router(build_router)
app.include_router(picks_router)

if __name__ == "__main__":

    parser = create_parser()
    args = parser.parse_args()
    if args.start:
        port = int(os.environ.get("PORT", 3200))
        uvicorn.run(app, host="0.0.0.0", port=port)

    # main_loop()
    print("Done")
