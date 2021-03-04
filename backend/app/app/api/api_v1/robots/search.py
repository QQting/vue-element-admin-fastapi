from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.extensions.utils import list_to_tree
from random import randint

router = APIRouter()

mocklist = []
for i in range(1, 101):
    new_data = {
        "id": i,
        "hostname": "robot-" + str(i),
        "status": "Active" if randint(0, 1) else "Inactive",
        "battery": randint(0, 100),
        "cpu": randint(0, 100),
        "memory": randint(0, 100),
        "storage": randint(0, 100),
        "timezone": "London",
        "content_short": "mock data",
        "content": "<p>I am testing data, I am testing data.</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>"        
    }
    mocklist.append(new_data)

@router.get("/list", response_model=schemas.Response)
def get_robots_list(title: Optional[str] = None, db: Session = Depends(deps.get_db)) -> Any:
    robot_data = {
        'total': len(mocklist),
        'items': mocklist
    }
    return {"code": 20000, "data": robot_data}
