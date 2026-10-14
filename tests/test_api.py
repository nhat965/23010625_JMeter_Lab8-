"""Simple API correctness smoke tests; does not replace JMeter performance testing."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen, Request
from api.server import Handler

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base = f"http://127.0.0.1:{cls.httpd.server_port}"
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def test_health(self):
        with urlopen(self.base + "/health") as r:
            self.assertEqual(r.status, 200)
            self.assertEqual(json.load(r)["status"], "ok")

    def test_items(self):
        with urlopen(self.base + "/api/items") as r:
            data = json.load(r)
            self.assertEqual(data["count"], len(data["items"]))

    def test_echo(self):
        req = Request(self.base + "/api/echo", data=b'{"message":"hello"}',
                      headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(req) as r:
            self.assertEqual(json.load(r)["received"]["message"], "hello")

if __name__ == "__main__":
    unittest.main()
