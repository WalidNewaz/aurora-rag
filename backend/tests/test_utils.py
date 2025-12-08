from fastapi.testclient import TestClient

from app.main import app

def create_test_app():
    """Factory to return a fresh TestClient with DB overrides."""
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    #
    # # IMPORTANT: Set overrides BEFORE creating TestClient
    # app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)