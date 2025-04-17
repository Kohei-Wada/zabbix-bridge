from fastapi import FastAPI, HTTPException, Body, Query, Depends
from typing import List, Union, Optional

from db import get_repository, get_db_connection
from models import HostCreateRequest, HostResponse
from repository import HostRepository

app = FastAPI()


@app.post("/hosts")
def insert_hosts(
    req: Union[HostCreateRequest, List[HostCreateRequest]] = Body(...),
    repo: HostRepository = Depends(get_repository),
):
    try:
        req_list = req if isinstance(req, list) else [req]
        return repo.insert_hosts(req_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hosts", response_model=List[HostResponse])
def get_hosts(
    zabbix_url: Optional[str] = Query(None),
    repo: HostRepository = Depends(get_repository),
):
    try:
        return repo.get_hosts(zabbix_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthz")
def healthz():
    """
    Health check endpoint. Returns OK if the application and DB are reachable.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="DB not ready")
