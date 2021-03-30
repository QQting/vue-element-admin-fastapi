from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.extensions.utils import list_to_tree
from random import randint
from app.api.api_v1.robots.RMT_core import rmt_py_wrapper
import json

router = APIRouter()

def search():
    rmt_py_wrapper.rmt_server_init()

    num_ptr = rmt_py_wrapper.new_intptr()
    dev_list = rmt_py_wrapper.device_info_list.frompointer(rmt_py_wrapper.rmt_server_create_device_list(num_ptr))
    num = rmt_py_wrapper.intptr_value(num_ptr)
    rmt_py_wrapper.delete_intptr(num_ptr) # release num_ptr

    # Put data in JSON format
    data = {"total": num, "items": []}
    items = []
    for i in range(0, num):
        item = {
            "Index": (i+1),
            "DeviceID": dev_list[i].deviceID,
            "Hostname": dev_list[i].host,
            "Model": dev_list[i].model,
            "IP": dev_list[i].ip,
            "MAC": dev_list[i].mac,
            "RMT_VERSION": dev_list[i].rmt_version
        }
        items.append(item)

    print("=== data ===")
    data["items"] = items
    result = json.dumps(data, indent=4)
    print(result)

    return data


@router.get("/list", response_model=schemas.Response)
def get_robots_list(title: Optional[str] = None, db: Session = Depends(deps.get_db)) -> Any:
    robot_data = search()
    return {"code": 20000, "data": robot_data}
