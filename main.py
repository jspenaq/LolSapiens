from backend.api.lol_scraper import main

# from backend.lolsapiens.lcu.lcu_connection import main_loop
import os
import uvicorn
from fastapi import FastAPI
from backend.api.router.build import router
from backend.api.utils import create_parser, setup_folders

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)

if __name__ == "__main__":
    setup_folders()

    parser = create_parser()
    args = parser.parse_args()
    if args.start:
        port = int(os.environ.get("PORT", 3200))
        uvicorn.run(app, host="0.0.0.0", port=port)
    # main()
    # main_loop()
    print("Done")
