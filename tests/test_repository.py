import unittest

from main import HostRepository, HostCreateRequest, HostResponse


class FakeCursor:
    def __init__(self):
        self.queries = []
        self.params = []
        self.rows = []

    def execute(self, query, params=None):
        self.queries.append(query)
        self.params.append(params)

    def fetchall(self):
        return self.rows

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def close(self):
        pass


class TestHostRepository(unittest.TestCase):
    def setUp(self):
        self.fake_conn = FakeConnection()
        self.repo = HostRepository(self.fake_conn)
        self.host1 = HostCreateRequest(
            zabbix_url="url1",
            hostid="1",
            host="h1",
            name="Host1",
            ip="127.0.0.1",
            maintenance_port="8080",
            proxy_name="proxy1"
        )

    def test_insert_hosts(self):
        result = self.repo.insert_hosts([self.host1])
        self.assertTrue(self.fake_conn.committed)
        self.assertEqual(len(self.fake_conn.cursor_obj.queries), 1)
        self.assertIn("INSERT INTO hosts",
                      self.fake_conn.cursor_obj.queries[0])
        self.assertEqual(
            self.fake_conn.cursor_obj.params[0],
            (
                "url1",
                "1",
                "h1",
                "Host1",
                "127.0.0.1",
                "8080",
                "proxy1"
            )
        )
        self.assertEqual(result["inserted"], 1)
        self.assertEqual(result["hosts"], ["Host1"])

    def test_get_hosts_without_filter(self):
        self.fake_conn.cursor_obj.rows = [
            ("url1", "1", "h1", "Host1", "127.0.0.1", "8080", "proxy1")
        ]
        result = self.repo.get_hosts()
        self.assertEqual(len(result), 1)
        hr = result[0]
        self.assertIsInstance(hr, HostResponse)
        self.assertEqual(hr.name, "Host1")
        last_query = self.fake_conn.cursor_obj.queries[-1]
        self.assertIn("FROM hosts", last_query)
        self.assertNotIn("WHERE", last_query)

    def test_get_hosts_with_filter(self):
        self.fake_conn.cursor_obj.rows = [
            ("url2", "2", "h2", "Host2", "127.0.0.2", "9090", None)
        ]
        result = self.repo.get_hosts("url2")
        self.assertEqual(len(result), 1)
        hr = result[0]
        self.assertEqual(hr.proxy_name, None)
        last_query = self.fake_conn.cursor_obj.queries[-1]
        self.assertIn("WHERE zabbix_url = %s", last_query)
        self.assertEqual(self.fake_conn.cursor_obj.params[-1], ("url2",))
