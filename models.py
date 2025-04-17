from pydantic import BaseModel
from typing import Optional


class HostCreateRequest(BaseModel):
    zabbix_url: str
    hostid: str
    host: str
    name: str
    ip: str
    maintenance_port: str
    proxy_name: Optional[str] = None


class HostResponse(BaseModel):
    zabbix_url: str
    hostid: str
    host: str
    name: str
    ip: str
    maintenance_port: str
    proxy_name: Optional[str] = None