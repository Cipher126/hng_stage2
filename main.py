import uvicorn
from fastapi import FastAPI
from database.connection import create_table
from routes.countries_routes import router
from routes.status_route import status


app = FastAPI(
    title="Country currency exchange service",
    description="A REST API that fetches country data and exchange rate and computes gdp for each countries"
)

app.include_router(router)
app.include_router(status)

@app.on_event("startup")
async def startup_event():
    await create_table()

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "ok",
        "message": "Country currency exchange service",
        "docs": "/docs",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8001, reload=True)