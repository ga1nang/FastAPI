from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from starlette import status
import pytest
from ..models import Todos, Users
from ..database import Base
from ..main import app
from ..router.todos import get_db, get_current_user

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:abc@localhost/testdb'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
       
def override_get_current_user():
    return {'username': 'ga1nang', 'id': 1, 'user_role': 'admin'}        
        
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


@pytest.fixture
def test_todo():
    user = Users(id=1, username="ga1nang")
    db.add(user)
    db.commit()
    
    
    todo = Todos(
        title="Learn to code!",
        description="Learn everyday!",
        priority=5,
        complete=False,
        owner_id=user.id,
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.execute(text('DELETE FROM users;'))
        connection.commit()
    
    

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": "Learn to code!",
        "description": "Learn everyday!",
        "priority": 5,
        "complete": False,
        "id": test_todo.id
    }]