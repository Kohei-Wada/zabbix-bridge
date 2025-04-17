from typing import List, Optional

from models import HostCreateRequest, HostResponse


class HostRepository:
    def __init__(self, connection):
        self.conn = connection

    def insert_hosts(self, hosts: List[HostCreateRequest]):
        cursor = self.conn.cursor()
        for host in hosts:
            cursor.execute(
                """
                INSERT INTO hosts (
                    zabbix_url,
                    hostid,
                    host,
                    name,
                    ip,
                    maintenance_port,
                    proxy_name
                )
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
                ),
            )
        self.conn.commit()
        cursor.close()
        return {
            "status": "ok",
            "inserted": len(hosts),
            "hosts": [h.name for h in hosts],
        }

    def get_hosts(self, zabbix_url: Optional[str] = None) -> List[HostResponse]:
        cursor = self.conn.cursor()
        if zabbix_url:
            cursor.execute(
                """
                SELECT
                    zabbix_url,
                    hostid,
                    host,
                    name,
                    ip,
                    maintenance_port,
                    proxy_name
                FROM hosts
                WHERE zabbix_url = %s
                """,
                (zabbix_url,),
            )
        else:
            cursor.execute(
                """
                SELECT
                    zabbix_url,
                    hostid,
                    host,
                    name,
                    ip,
                    maintenance_port,
                    proxy_name
                FROM hosts
                """
            )
        rows = cursor.fetchall()
        cursor.close()
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
