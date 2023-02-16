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

description = """
This is LolSapiens API.
Endpoints include retrieving bans by tier and builds for specific champions for a given patch.
"""

app = FastAPI(
    title="LolSapiensApi",
    description=description,
    version="0.1.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basic_router)
app.include_router(bans_router, prefix="/tierlist")
app.include_router(picks_router, prefix="/tierlist")
app.include_router(build_router, prefix="/champion")

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.start:
        port = int(os.environ.get("PORT", 3200))
        uvicorn.run(app, host="0.0.0.0", port=port)

    print("Done")
