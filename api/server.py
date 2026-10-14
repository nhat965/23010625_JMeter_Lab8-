"""Local demo API for Apache JMeter Lab 8. No third-party service is load tested."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json
import time

ITEMS = [{"id": 1, "name": "Laptop", "price": 1500}, {"id": 2, "name": "Mouse", "price": 25}, {"id": 3, "name": "Keyboard", "price": 70}]

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self.respond(200, {"status": "ok"})
        elif path == "/api/items":
            self.respond(200, {"items": ITEMS, "count": len(ITEMS)})
        elif path == "/api/slow":
            time.sleep(0.2)
            self.respond(200, {"status": "ok", "delay_ms": 200})
        else:
            self.respond(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/echo":
            self.respond(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 4096:
                self.respond(413, {"error": "payload too large"})
                return
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("expected JSON object")
        except (ValueError, json.JSONDecodeError):
            self.respond(400, {"error": "invalid JSON object"})
            return
        self.respond(200, {"received": data})

if __name__ == "__main__":
    print("Demo API: http://127.0.0.1:8000 | Ctrl+C to stop")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
