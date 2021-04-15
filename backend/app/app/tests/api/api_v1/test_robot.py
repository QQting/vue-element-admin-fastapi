from typing import Dict
from fastapi.testclient import TestClient
from app.api.api_v1.robots.RMT_core import rmt_py_wrapper
from app.core.config import settings
from app.main import app
import os
import pytest
import subprocess
import string
import random

def str_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@pytest.fixture(scope="class")
def get_agent_num():
    rmt_py_wrapper.rmt_server_init()
    num_ptr = rmt_py_wrapper.new_intptr()
    dev_list = rmt_py_wrapper.device_info_list.frompointer(rmt_py_wrapper.rmt_server_create_device_list(num_ptr))
    num = rmt_py_wrapper.intptr_value(num_ptr)
    rmt_py_wrapper.delete_intptr(num_ptr) # release num_ptr

    return num

@pytest.fixture(scope="class")
def default_wifi_data():
    return {"ssid": "RMTserver",
            "password": "adlinkros",
            "band": "2.4 GHz",
            "mode_on": False}
    
class TestRobotPage:
    @pytest.fixture(scope="class", autouse=True)
    def get_robot_list(self, client: TestClient, superuser_token_headers: Dict[str, str]):
        response = client.get(
            "/robots/discovery", headers=superuser_token_headers)
        return response

    @pytest.fixture(scope="class", autouse=True)
    def agent_data(self, get_robot_list):
        return get_robot_list.json()["data"]

    def test_status_code(self, get_robot_list) -> None:
        assert get_robot_list.status_code == 200

    def test_robot_data(self, agent_data, get_agent_num):
        if get_agent_num:
            assert agent_data["total"] == get_agent_num
            for agent in agent_data["items"]:
                for feature in agent:
                    assert agent[feature]

class TestWifiGetRequest:
    @pytest.fixture(scope="class", autouse=True)
    def get_wifi_set(self, client: TestClient, superuser_token_headers: Dict[str, str]):
        response = client.get(
            "/robots/wifi-init", headers=superuser_token_headers)
        return response

    @pytest.fixture(scope="class", autouse=True)
    def user_data(self, get_wifi_set):
        return get_wifi_set.json()["data"]

    def test_status_code(self, get_wifi_set) -> None:
        assert get_wifi_set.status_code == 200

    @pytest.mark.parametrize("config_name", ["password", "ssid", "band"])
    def test_wifi_pwd(self, user_data, config_name) -> None:
        assert user_data[config_name]

    def test_default_wifi(self, client: TestClient, superuser_token_headers: Dict[str, str], default_wifi_data):
            result = subprocess.run(["nmcli", "con", "delete", "RMTHost"], stdout=subprocess.PIPE)
            response = client.get(
                "/robots/wifi-init", headers=superuser_token_headers)
            assert response.json()["data"] == default_wifi_data

class TestWifiPostRequest:
    @pytest.fixture(scope="class", params=[(33,100,8,32), (1,32,0,7), (1,32,33,100)], ids=["ssid_over","pwd_short","pwd_over"])
    def faux_response(self, request, client: TestClient, superuser_token_headers: Dict[str, str], default_wifi_data):
        faux_set = {"ssid": str_generator(size=random.randint(request.param[0], request.param[1])),
                    "password": str_generator(size=random.randint(request.param[2], request.param[3])),
                    "band": "2.4 GHz",
                    "mode_on": False}
        response = client.post("/robots/wifi", headers=superuser_token_headers, json=faux_set)
        yield response
        result = subprocess.run(["nmcli", "con", "delete", "RMTHost"], stdout=subprocess.PIPE)
        response = client.post("/robots/wifi", headers=superuser_token_headers, json=default_wifi_data)

    @pytest.fixture(scope="class")
    def post_response(self, client: TestClient, superuser_token_headers: Dict[str, str]):
        test_set = {"ssid": str_generator(size=random.randint(1, 32)),
                    "password": str_generator(size=random.randint(8, 32)),
                    "band": "2.4 GHz",
                    "mode_on": False}
        response = client.post("/robots/wifi", headers=superuser_token_headers, json=test_set)
        return response

    def test_post_wifi(self, post_response) -> None: 
        assert post_response.status_code == 200
        assert "Error" not in post_response.json()["data"]

    def test_post_faux(self, faux_response):
        print(faux_response.json())
        with pytest.raises(AssertionError):
            assert faux_response.status_code == 200
