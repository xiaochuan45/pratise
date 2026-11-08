from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ship

router = APIRouter(prefix="/api/ships", tags=["ships"])

@router.get("")
def list_ships(db: Session = Depends(get_db)):
    # TODO: implement keyword search and status filtering
    return db.query(Ship).order_by(Ship.id.asc()).all()

@router.get("/{ship_id}")
def get_ship(ship_id: int, db: Session = Depends(get_db)):
    ship = db.query(Ship).filter(Ship.id == ship_id).first()
    if ship is None:
        raise HTTPException(status_code=404, detail="船舶不存在")
    return ship

@router.post("", status_code=501)
def create_ship():
    # TODO: implement create and validation
    raise HTTPException(status_code=501, detail="新增功能尚未实现")

@router.put("/{ship_id}", status_code=501)
def update_ship(ship_id: int):
    # TODO: implement update and validation
    raise HTTPException(status_code=501, detail="编辑功能尚未实现")
