"""
Weather Dashboard HTTP Server.
Provides static UI delivery, JSON REST endpoints, and Prometheus metrics scraping endpoint.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import time
import sys

from src.weather_service import weather_service
from src.metrics import metrics

PORT = int(os.environ.get("PORT", 8080))
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")

class WeatherHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        start_time = time.time()
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        status_code = 200

        try:
            if path == "/api/weather":
                city = query_params.get("city", ["London"])[0]
                data = weather_service.get_weather(city)
                self._send_json(200, data)
                status_code = 200

            elif path == "/api/health":
                health_data = {
                    "status": "healthy",
                    "uptime_seconds": round(time.time() - metrics.start_time, 2),
                    "version": "1.0.0",
                    "service": "weather-dashboard"
                }
                self._send_json(200, health_data)
                status_code = 200

            elif path == "/metrics":
                metrics_content = metrics.generate_metrics()
                self._send_text(200, metrics_content, content_type="text/plain; version=0.0.4; charset=utf-8")
                status_code = 200

            else:
                # Default file serving (index.html, css, js)
                super().do_GET()
                return

        except Exception as e:
            status_code = 500
            self._send_json(500, {"error": str(e)})

        finally:
            duration = time.time() - start_time
            metrics.record_request("GET", path, status_code, duration)

    def _send_json(self, status_code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status_code: int, content: str, content_type: str = "text/plain"):
        body = content.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet standard HTTP logging for clean CLI & test output
        pass

def run_server(port=PORT):
    with socketserver.TCPServer(("", port), WeatherHTTPRequestHandler) as httpd:
        print(f"Weather Dashboard server running on http://localhost:{port}")
        print(f"Metrics available on http://localhost:{port}/metrics")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully.")

if __name__ == "__main__":
    run_server()
