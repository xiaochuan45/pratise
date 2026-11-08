import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from app.models import Ship

@pytest.fixture
def client():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    TestingSession=sessionmaker(autocommit=False,autoflush=False,bind=engine)
    Base.metadata.create_all(bind=engine)
    def override():
        db=TestingSession()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override
    with TestingSession() as db:
        db.add_all([
            Ship(name="测试货轮",mmsi="413000001",ship_type="cargo",status="sailing",owner="测试航运"),
            Ship(name="测试客船",mmsi="413000002",ship_type="passenger",status="moored",owner="测试客运"),
        ])
        db.commit()
    with TestClient(app) as c: yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

def test_health(client):
    r=client.get("/api/health")
    assert r.status_code==200 and r.json()=={"status":"ok"}

def test_list_ships(client):
    r=client.get("/api/ships")
    assert r.status_code==200 and len(r.json())==2

def test_get_ship(client):
    r=client.get("/api/ships/1")
    assert r.status_code==200 and r.json()["mmsi"]=="413000001"

def test_missing_ship(client):
    assert client.get("/api/ships/999").status_code==404
