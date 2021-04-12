from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.extensions.utils import list_to_tree
from random import randint
from app.api.api_v1.robots.RMT_core import rmt_py_wrapper
import json
import numpy as np
import socketio
import threading

lock = threading.Lock()

background_task_started = False
client_connecting = 0

class ServerNamespace(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        print(f"{sid} is connected !")
        global background_task_started, client_connecting
        lock.acquire()
        client_connecting = client_connecting + 1
        lock.release()
        if not background_task_started:
            self.server.start_background_task(self.background_task)
            background_task_started = True
        # self.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

    async def on_disconnect(self, sid):
        print(f"{sid} is disconnected !")
        global background_task_started,client_connecting
        lock.acquire()
        client_connecting = client_connecting - 1
        lock.release()
        if client_connecting == 0:
            background_task_started = False


    async def on_disconnect_request(self, sid):
        await self.on_disconnect(sid)

    async def on_client_message(self, sid, data):
        print(data)

    async def on_my_event(self, sid, data):
        await self.emit('my_response', data)

    async def on_my_room_event(self, sid, message):
        await self.emit('my_response', {'data': message['data']}, room=message['room'])

    async def on_my_broadcast_event(self, sid, message):
        await self.emit('my_response', {'data': message['data']})

    async def on_join(self, sid, message):
        await self.enter_room(sid, message['room'])
        await self.emit('my_response', {'data': 'Entered room: ' + message['room']}, room=sid)

    async def on_leave(self, sid, message):
        await self.leave_room(sid, message['room'])
        await self.emit('my_response', {'data': 'Left room: ' + message['room']}, room=sid)

    async def on_close(self, sid, message):
        await self.emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
        await self.close_room(message['room'])

    async def background_task(self):
        global background_task_started
        while background_task_started:
            sys_info = await self.hardware_info()
            await self.emit('monitor_robot', sys_info)
            await self.server.sleep(1.5)

    async def hardware_info(self):
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
                "battery": np.random.randint(1,100),
                "cpu": np.random.randint(1,100),
                "memory": np.random.randint(1,100),
                "storage": np.random.randint(1,100),
            }
            items.append(item)

        data["items"] = items
        result = json.dumps(data, indent=4)

        return data
