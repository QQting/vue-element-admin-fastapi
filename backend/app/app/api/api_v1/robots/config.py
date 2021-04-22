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
from typing import List, Dict

router = APIRouter()

class SetSameConfigById_ReqBody(BaseModel):
    device_list: List[str] = ["5566", "6166"]
    config_dict: Dict[str, str] = {
        "locate": "on"
    }

# class SetDiffConfigById_ReqBody(BaseModel):
#     __root__: Dict[str, dict] = {
#         "5566": {
#             "hostname": "ROScube-1",
#             "locate": "on"
#         },
#         "6166": {
#             "hostname": "ROScube-2",
#             "locate": "on"            
#         }
#     }
#     def __iter__(self):
#         return iter(self.__root__)
#     def __getitem__(self, item):
#         return self.__root__[item]

class GetSameConfigById_ReqBody(BaseModel):
    device_list: List[str] = ["5566", "6166"]
    config_list: List[str] = ["cpu", "ram", "hostname", "wifi"]

# class GetDiffConfigById_ReqBody(BaseModel):
#     __root__: Dict[str, list] = {
#         "5566": ["cpu", "ram"],
#         "6166": ["hostname", "wifi"]
#     }
#     def __iter__(self):
#         return iter(self.__root__)
#     def __getitem__(self, item):
#         return self.__root__[item]

class GetConfigForAll_ReqBody(BaseModel):
    __root__: List[str] = ["cpu", "ram", "hostname", "wifi"]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]

def rmt_get_config_for_all(dev_list, dev_num, config_list):
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
    config_data = {}
    for i in range(0, info_num):
        # Split the result string into dictionary data
        result_list = info_list[i].value_list.split(";")
        device_dict = {}
        device_id = info_list[i].deviceID
        for item in result_list:
            for key in config_list:
                if key in item:
                    device_dict[key] = item[len(key)+1:]
        # print(device_dict)
        config_data[device_id] = device_dict
    # result = json.dumps(config_data, indent=4)
    # print(result)

    return config_data

def rmt_get_same_config_by_id(target_list, target_num, config_list):
    # Create config key string
    config_key_str = ""
    for item in config_list:
        config_key_str += item + ';'

    # Get device info list
    id_list = rmt_py_wrapper.ulong_array(target_num)
    for i in range(0, target_num):
        id_list[i] = int(target_list[i])
    info_num_ptr = rmt_py_wrapper.new_intptr()
    info_list = rmt_py_wrapper.data_info_list.frompointer(rmt_py_wrapper.rmt_server_get_info(id_list, target_num, config_key_str, info_num_ptr))
    info_num = rmt_py_wrapper.intptr_value(info_num_ptr)
    rmt_py_wrapper.delete_intptr(info_num_ptr) # release info_num_ptr
    
    # print("=== get config result ===")
    config_data = {}
    for i in range(0, info_num):
        # Split the result string into dictionary data
        result_list = info_list[i].value_list.split(";")
        device_dict = {}
        device_id = info_list[i].deviceID
        for item in result_list:
            for key in config_list:
                if key in item:
                    device_dict[key] = item[len(key)+1:]
        # print(device_dict)
        config_data[device_id] = device_dict
    # result = json.dumps(config_data, indent=4)
    # print(result)

    return config_data

def rmt_set_same_config_by_id(target_list, target_num, config_dict):
    # Covert config_dict to config_str
    config_str = ""
    for key, value in config_dict.items():
        config_str += key + ':' + value + ';'

    # Create data_info_array to save configurations for each device
    data_info_array = rmt_py_wrapper.new_data_info_array(target_num)
    for i in range (0, target_num):
        data_info_element = rmt_py_wrapper.data_info()
        data_info_element.deviceID = int(target_list[i])
        data_info_element.value_list = config_str
        rmt_py_wrapper.data_info_array_setitem(data_info_array, i, data_info_element)

    # # Print what we want to set in data_info_array
    # print("=== set config req ===")
    # for i in range (0, target_num):
    #     data_info_element = rmt_py_wrapper.data_info_array_getitem(data_info_array, i)
    #     print("deviceID=%d" % data_info_element.deviceID)
    #     print("value_list=%s" % data_info_element.value_list)

    # Send data_info_array to RMT library
    info_num_ptr = rmt_py_wrapper.new_intptr()
    info_list = rmt_py_wrapper.data_info_list.frompointer(rmt_py_wrapper.rmt_server_set_info(data_info_array, target_num, info_num_ptr))
    info_num = rmt_py_wrapper.intptr_value(info_num_ptr)
    rmt_py_wrapper.delete_intptr(info_num_ptr) # release info_num_ptr

    print("=== set config result ===")
    config_data = {}
    for i in range(0, info_num):
        # Split the result string into dictionary data
        result_list = info_list[i].value_list.split(";")
        device_dict = {}
        device_id = info_list[i].deviceID
        for item in result_list:
            key_value_pair = item.split(":")
            if len(key_value_pair) > 1:
                key = key_value_pair[0]
                value = key_value_pair[1]
                device_dict[key] = value
        config_data[device_id] = device_dict
    result = json.dumps(config_data, indent=4)
    print(result)
    return config_data

def rmt_discovery():
    rmt_py_wrapper.rmt_server_init()
    num_ptr = rmt_py_wrapper.new_intptr()
    dev_list = rmt_py_wrapper.device_info_list.frompointer(rmt_py_wrapper.rmt_server_create_device_list(num_ptr))
    num = rmt_py_wrapper.intptr_value(num_ptr)
    rmt_py_wrapper.delete_intptr(num_ptr) # release num_ptr
    return dev_list, num

@router.post("/get_config_for_all", response_model=schemas.Response)
def get_config_for_all(config_req_body: GetConfigForAll_ReqBody) -> Any:
    code = 40400 # not found for default
    dev_list, num = rmt_discovery()
    data = rmt_get_config_for_all(dev_list, num, config_req_body.__root__)
    if data:
        # found => 200 OK
        code = 20000
    # TODO: free dev_list
    # rmt_py_wrapper.rmt_server_free_device_list(dev_list)
    rmt_py_wrapper.rmt_server_deinit()
    return {"code": code, "data": data}

@router.post("/get_same_config_by_id", response_model=schemas.Response)
def get_same_config_by_id(config_req_body: GetSameConfigById_ReqBody) -> Any:
    code = 40400 # not found for default
    rmt_py_wrapper.rmt_server_init()
    target_list = config_req_body.device_list
    config_list = config_req_body.config_list
    target_num = len(target_list)
    data = rmt_get_same_config_by_id(target_list, target_num, config_list)
    if data:
        # found => 200 OK
        code = 20000
    print(data)
    # TODO: free dev_list
    # rmt_py_wrapper.rmt_server_free_device_list(dev_list)
    rmt_py_wrapper.rmt_server_deinit()
    return {"code": code, "data": data}

# @router.post("/get_diff_config_by_id", response_model=schemas.Response)
# def get_diff_config_by_id(config_req_body: GetDiffConfigById_ReqBody) -> Any:
#     pass

@router.post("/set_same_config_by_id", response_model=schemas.Response)
def set_same_config_by_id(config_req_body: SetSameConfigById_ReqBody) -> Any:
    code = 40400 # not found for default
    rmt_py_wrapper.rmt_server_init()
    target_list = config_req_body.device_list
    config_dict = config_req_body.config_dict
    target_num = len(target_list)
    data = rmt_set_same_config_by_id(target_list, target_num, config_dict)
    if data:
        # found => 200 OK
        code = 20000
    return {"code": code, "data": data}

# @router.post("/set_diff_config_by_id", response_model=schemas.Response)
# def set_same_config_by_id(config_req_body: SetSameConfigById_ReqBody) -> Any:
#     pass