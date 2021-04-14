from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.extensions.utils import list_to_tree
from random import randint
from app.api.api_v1.robots.RMT_core import rmt_py_wrapper
import json
import os 
import subprocess
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ConfigReqBody(BaseModel):
    custom_config_list: List[str] = ["cpu", "ram", "hostname", "wifi"]

def rmt_get_config(dev_list, dev_num, config_list):
    # Create config key string
    config_key_str = ""
    for item in config_list:
        config_key_str += item + ';'

    # Get device info list
    id_list = rmt_py_wrapper.ulong_array(dev_num)
    for i in range(0, dev_num):
        id_list[i] = dev_list[i].deviceID
    info_num_ptr = rmt_py_wrapper.new_intptr()
    info_list = rmt_py_wrapper.data_info_list.frompointer(rmt_py_wrapper.rmt_server_get_info(id_list, dev_num, config_key_str, info_num_ptr))
    info_num = rmt_py_wrapper.intptr_value(info_num_ptr)
    rmt_py_wrapper.delete_intptr(info_num_ptr) # release info_num_ptr
    
    # print("=== get config result ===")
    config_data = []
    for i in range(0, info_num):
        # Split the result string into dictionary data
        result_list = info_list[i].value_list.split(";")
        dict_data = {"deviceID": info_list[i].deviceID}
        for item in result_list:
            for key in config_list:
                if key in item:
                    dict_data[key] = item[len(key)+1:]
        # print(dict_data)
        config_data.append(dict_data)
    # result = json.dumps(config_data, indent=4)
    # print(result)

    return config_data

def rmt_get_config_by_id(dev_list, dev_num, config_list, device_id):
    # Create config key string
    config_key_str = ""
    for item in config_list:
        config_key_str += item + ';'

    # Get device info list
    id_list = rmt_py_wrapper.ulong_array(dev_num)
    for i in range(0, dev_num):
        id_list[i] = dev_list[i].deviceID
    info_num_ptr = rmt_py_wrapper.new_intptr()
    info_list = rmt_py_wrapper.data_info_list.frompointer(rmt_py_wrapper.rmt_server_get_info(id_list, dev_num, config_key_str, info_num_ptr))
    info_num = rmt_py_wrapper.intptr_value(info_num_ptr)
    rmt_py_wrapper.delete_intptr(info_num_ptr) # release info_num_ptr
    
    # print("=== get config result ===")
    config_data = []
    for i in range(0, info_num):
        if device_id == info_list[i].deviceID:
            # Split the result string into dictionary data
            result_list = info_list[i].value_list.split(";")
            dict_data = {"deviceID": info_list[i].deviceID}
            for item in result_list:
                for key in config_list:
                    if key in item:
                        dict_data[key] = item[len(key)+1:]
            # print(dict_data)
            config_data.append(dict_data)
            break
    # result = json.dumps(config_data, indent=4)
    # print(result)

    return config_data

def rmt_discovery():
    rmt_py_wrapper.rmt_server_init()
    num_ptr = rmt_py_wrapper.new_intptr()
    dev_list = rmt_py_wrapper.device_info_list.frompointer(rmt_py_wrapper.rmt_server_create_device_list(num_ptr))
    num = rmt_py_wrapper.intptr_value(num_ptr)
    rmt_py_wrapper.delete_intptr(num_ptr) # release num_ptr
    return dev_list, num

@router.post("/get_config", response_model=schemas.Response)
def get_config(config_req_body: ConfigReqBody) -> Any:
    code = 40400 # not found for default
    dev_list, num = rmt_discovery()
    data = rmt_get_config(dev_list, num, config_req_body.custom_config_list)
    if data:
        # found => 200 OK
        code = 20000
    # TODO: free dev_list
    # rmt_py_wrapper.rmt_server_free_device_list(dev_list)
    rmt_py_wrapper.rmt_server_deinit()
    return {"code": code, "data": data}

@router.post("/get_config/{device_id}", response_model=schemas.Response)
def get_config_by_id(config_req_body: ConfigReqBody, device_id: int) -> Any:
    code = 40400 # not found for default
    dev_list, num = rmt_discovery()
    data = rmt_get_config_by_id(dev_list, num, config_req_body.custom_config_list, device_id)
    if data:
        # found => 200 OK
        code = 20000
    # TODO: free dev_list
    # rmt_py_wrapper.rmt_server_free_device_list(dev_list)
    return {"code": code, "data": data}
