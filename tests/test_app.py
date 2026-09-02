"""
Integration tests for Weather Dashboard HTTP endpoints and Prometheus metrics.
"""

import unittest
import urllib.request
import json
import threading
import time

from src.app import WeatherHTTPRequestHandler
import http.server

class TestWeatherHTTPEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), WeatherHTTPRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.2) # Allow server thread to initialize

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/health"
        req = urllib.request.urlopen(url)
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "weather-dashboard")

    def test_weather_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/weather?city=Tokyo"
        req = urllib.request.urlopen(url)
        self.assertEqual(req.status, 200)
        data = json.loads(req.read().decode("utf-8"))
        self.assertEqual(data["city"], "Tokyo")
        self.assertIn("temperature", data)

    def test_metrics_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/metrics"
        req = urllib.request.urlopen(url)
        self.assertEqual(req.status, 200)
        body = req.read().decode("utf-8")
        self.assertIn("process_uptime_seconds", body)
        self.assertIn("http_requests_total", body)
        self.assertIn("weather_api_up", body)

if __name__ == "__main__":
    unittest.main()
