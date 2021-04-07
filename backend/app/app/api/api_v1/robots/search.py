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

    # TODO: free dev_list
    # rmt_py_wrapper.rmt_server_free_device_list(dev_list)
    rmt_py_wrapper.rmt_server_deinit()

    return data


@router.get("/list", response_model=schemas.Response)
def get_robots_list(title: Optional[str] = None, db: Session = Depends(deps.get_db)) -> Any:
    robot_data = search()
    return {"code": 20000, "data": robot_data}

def wifi_ap_init():
    wifi_interface = ""
    for interface in os.listdir('/sys/class/net'):
        if "wireless" in os.listdir('/sys/class/net/' + interface):
            wifi_interface = interface
            break

    result = subprocess.run(["nmcli", "con", "add", "type", "wifi", "ifname", str(wifi_interface), "con-name",
                            "RMTHost", "ssid", "RMTHost"], stdout=subprocess.PIPE)
    result = subprocess.run(["nmcli", "con", "modify", "RMTHost", "802-11-wireless.mode", "ap", "802-11-wireless.band",
                            "bg", "ipv4.method", "shared"], stdout=subprocess.PIPE)
    result = subprocess.run(["nmcli", "con", "modify", "RMTHost", "802-11-wireless-security.key-mgmt", "wpa-psk"], stdout=subprocess.PIPE)

def modify_ap_config(ssid, password, band):
    result = subprocess.run(["nmcli", "con", "modify", "RMTHost", "802-11-wireless.ssid", str(ssid)], stdout=subprocess.PIPE)
    result = subprocess.run(["nmcli", "con", "modify", "RMTHost", "802-11-wireless-security.psk", str(password)], stdout=subprocess.PIPE)
    result = subprocess.run(["nmcli", "con", "modify", "RMTHost", "802-11-wireless.band", str(band)], stdout=subprocess.PIPE)

@router.post("/wifi", response_model=schemas.Response)
def wifi_callback(*, db: Session = Depends(deps.get_db), wifi_mode: schemas.WifiMode,) -> Any:
    wifi_set = {"ssid": wifi_mode.ssid, "password": wifi_mode.password, "band": wifi_mode.band, "mode_on": wifi_mode.mode_on}
    if "RMTHost.nmconnection" not in os.listdir("/etc/NetworkManager/system-connections"):
        wifi_ap_init()
    band_code = {"2.4 GHz": "bg", "5 GHz": "a"}
    modify_ap_config(wifi_set["ssid"], wifi_set["password"], band_code[wifi_set["band"]])

    if wifi_set["mode_on"]:
        result = subprocess.run(["nmcli", "con", "up", "RMTHost"], stdout=subprocess.PIPE)
    else:
        result = subprocess.run(["nmcli", "con", "down", "RMTHost"], stdout=subprocess.PIPE)

    return {"code": 20000, "data": {"status": "success"}}

@router.get("/wifi-init", response_model=schemas.Response)
def current_wifi():
    if "RMTHost.nmconnection" not in os.listdir("/etc/NetworkManager/system-connections"):
        wifi_data = {
            "ssid": "RMTserver",
            "password": "adlinkros",
            "band": "2.4 GHz",
            "mode_on": False
        }

        return {"code": 20000, "data": wifi_data}

    result = subprocess.run(["nmcli", "-t", "-f", "NAME", "con", "show", "--active"], stdout=subprocess.PIPE)
    active_name = result.stdout.decode('utf-8').split("\n")
    mode_on = "RMTHost" in active_name
    result = subprocess.run(["nmcli", "-f", "802-11-wireless.ssid", "connection", "show", "RMTHost"], stdout=subprocess.PIPE)
    ssid = result.stdout.decode('utf-8').replace("\n", "").split()[1]
    result = subprocess.run(["nmcli", "-s", "-f", "802-11-wireless-security.psk", "connection", "show", "RMTHost"], stdout=subprocess.PIPE)
    password = result.stdout.decode('utf-8').replace("\n", "").split()[1]
    result = subprocess.run(["nmcli","-f", "802-11-wireless.band", "connection", "show", "RMTHost"], stdout=subprocess.PIPE)
    band = result.stdout.decode('utf-8').replace("\n", "").split()[1]
    band_code = {"bg": "2.4 GHz", "a": "5 GHz"}
    band_freq = band_code[band]
    wifi_data = {
        "ssid": ssid,
        "password": password,
        "band": band_freq,
        "mode_on": mode_on
    }

    return {"code": 20000, "data": wifi_data}