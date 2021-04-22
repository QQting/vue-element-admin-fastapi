from typing import Dict
from fastapi.testclient import TestClient
from app.core.config import settings
import os
import pytest
import subprocess
import random
import time

@pytest.fixture(scope="module", autouse=True)
def change_dir():
    os.chdir("../../../api/api_v1/robots/RMT_core/")

@pytest.fixture(scope="module", autouse=True)
def agent_start_id():
    return random.randint(0,500)

@pytest.fixture(scope="module", autouse=True)
def generate_agent(agent_start_id):
    subprocess.run(["killall", "agent_example"])
    num = random.randint(0,10)
    process = subprocess.Popen(["python3", "multi_agents.py", "-n", str(num), "-s", str(agent_start_id)])
    time.sleep(2)
    yield num
    process.kill()
    subprocess.run(["killall", "agent_example"])

class TestRobotPage:
    @pytest.fixture(scope="class", autouse=True)
    def get_robot_list(self, client: TestClient, superuser_token_headers: Dict[str, str]):
        response = client.get(
            "/robots/discovery", headers=superuser_token_headers)
        return response

    @pytest.fixture(scope="class", autouse=True)
    def agent_data(self, get_robot_list):
        return get_robot_list.json()["data"]

    def test_status_code(self, get_robot_list):
        assert get_robot_list.status_code == 200

    def test_robot_data(self, agent_data, generate_agent):
        assert agent_data["total"] == generate_agent
        if generate_agent:
            for agent in agent_data["items"]:
                for feature in agent:
                    assert agent[feature]

class TestGetConfig:
    @pytest.fixture(scope="class", autouse=True)
    def default_config_data(self):
        return {"custom_config_list": ["cpu","ram","hostname","wifi"]}
    @pytest.fixture(scope="class", autouse=True)
    def get_config_all(self, client: TestClient, superuser_token_headers: Dict[str, str], default_config_data):
        response = client.post(
            "/robots/get_config", headers=superuser_token_headers, json=default_config_data)
        return response

    @pytest.fixture(scope="class", autouse=True)
    def agent_data(self, get_config_all):
        return get_config_all.json()["data"]

    def test_status_code(self, get_config_all):
        assert get_config_all.status_code == 200

    def test_config_data(self, agent_data, generate_agent):
        assert len(agent_data) == generate_agent
        if generate_agent:
            for agent in agent_data:
                    for feature in agent:
                        assert agent[feature]

    def test_config_id(self, client: TestClient, superuser_token_headers: Dict[str, str], agent_start_id, generate_agent, default_config_data):
        for id in range(agent_start_id, agent_start_id+generate_agent):
            response = client.post(
                f"/robots/get_config/{id}", headers=superuser_token_headers, json=default_config_data)
            assert response.status_code == 200

    def test_faux_id(self, client: TestClient, superuser_token_headers: Dict[str, str], agent_start_id, default_config_data):
        response = client.post(
                f"/robots/get_config/{agent_start_id+20}", headers=superuser_token_headers, json=default_config_data)
        with pytest.raises(AssertionError):
            assert response.json()["code"] == 20000
