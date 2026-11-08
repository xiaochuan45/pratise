from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, SessionLocal, engine
from app.models import Ship
from app.routers.ships import router as ships_router

BASE = Path(__file__).resolve().parent
app = FastAPI(title="Ship Management Demo")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
app.include_router(ships_router)

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok"}

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Ship).count() == 0:
            db.add_all([
                Ship(name="海巡01", mmsi="413123456", ship_type="patrol", status="sailing", owner="海事管理局"),
                Ship(name="远洋之星", mmsi="413123457", ship_type="cargo", status="moored", owner="远洋运输"),
                Ship(name="蓝海号", mmsi="413123458", ship_type="tanker", status="maintenance", owner="蓝海航运"),
                Ship(name="江海快线", mmsi="413123459", ship_type="passenger", status="sailing", owner="江海客运"),
                Ship(name="渔丰8号", mmsi="413123460", ship_type="fishing", status="offline", owner="渔丰水产"),
            ])
            db.commit()
    finally:
        db.close()

init_db()
