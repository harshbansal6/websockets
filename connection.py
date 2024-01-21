from typing import Dict
from fastapi import WebSocket

connections: Dict[str, WebSocket] = {}
