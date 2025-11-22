from fastapi import FastAPI
from app.database import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.transaction_routes import router as txn_router
from app.routes.portfolio_routes import router as summary_router
from app.routes.price_route import router as price_router

app = FastAPI()

# Routes of all End-points
app.include_router(user_router)
app.include_router(txn_router)
app.include_router(summary_router)
app.include_router(price_router)

@app.get("/")
def home():
    return {"message": "Healthwise portfolio Tracker API Running"}
