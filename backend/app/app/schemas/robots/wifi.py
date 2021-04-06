from typing import Optional, Any

from pydantic import BaseModel

# Shared properties
class WifiBase(BaseModel):
    ssid: str = None
    password: str = None
    band: str = None
    init: bool = None
    mode_on: bool = None

# Properties to receive on item creation
class WifiMode(WifiBase):
    pass
