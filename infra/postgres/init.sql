CREATE TABLE IF NOT EXISTS hosts (
    zabbix_url TEXT,
    hostid TEXT,
    host TEXT,
    name TEXT,
    ip TEXT,
    maintenance_port TEXT,
    proxy_name TEXT,
    PRIMARY KEY (zabbix_url, hostid)
);
