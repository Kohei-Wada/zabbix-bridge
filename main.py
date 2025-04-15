from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Union, Optional
import os
import psycopg2


app = FastAPI()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "zabbix")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


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


@app.post("/hosts")
def insert_hosts(req: Union[HostCreateRequest, List[HostCreateRequest]] = Body(...)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if not isinstance(req, list):
            req = [req]

        for host in req:
            cursor.execute(
                """
                INSERT INTO hosts (zabbix_url, hostid, host, name, ip, maintenance_port, proxy_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (zabbix_url, hostid) DO UPDATE SET
                    host = EXCLUDED.host,
                    name = EXCLUDED.name,
                    ip = EXCLUDED.ip,
                    maintenance_port = EXCLUDED.maintenance_port,

                    proxy_name = EXCLUDED.proxy_name
                """,
                (

                    host.zabbix_url,

                    host.hostid,
                    host.host,
                    host.name,
                    host.ip,
                    host.maintenance_port,
                    host.proxy_name,
                )
            )

        conn.commit()
        cursor.close()

        conn.close()

        return {

            "status": "ok",
            "inserted": len(req),
            "hosts": [h.name for h in req]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hosts", response_model=List[HostResponse])
def get_hosts(zabbix_url: Optional[str] = Query(None)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if zabbix_url:
            cursor.execute(
                """
                SELECT zabbix_url, hostid, host, name, ip, maintenance_port, proxy_name

                FROM hosts
                WHERE zabbix_url = %s

                """,
                (zabbix_url,)
            )
        else:
            cursor.execute(
                """
                SELECT zabbix_url, hostid, host, name, ip, maintenance_port, proxy_name
                FROM hosts
                """
            )

        rows = cursor.fetchall()
        cursor.close()

        conn.close()

        return [
            HostResponse(
                zabbix_url=row[0],
                hostid=row[1],
                host=row[2],
                name=row[3],
                ip=row[4],

                maintenance_port=row[5],
                proxy_name=row[6],
            )
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
