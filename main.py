from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/stasjoner")
async def get_stations():
    return {"message": "stasjoner"}
