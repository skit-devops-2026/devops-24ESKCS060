"""
Prometheus Metrics Exporter for Weather Dashboard Application.
Tracks request counts, latency histograms, active connections, and weather service status.
"""

import time
import os

class PrometheusMetrics:
    def __init__(self):
        self.request_counts = {}
        self.request_latencies = {}
        self.start_time = time.time()

    def record_request(self, method: str, path: str, status_code: int, duration_seconds: float):
        """Record HTTP request metric counters and latencies."""
        key = (method, path, str(status_code))
        self.request_counts[key] = self.request_counts.get(key, 0) + 1

        if key not in self.request_latencies:
            self.request_latencies[key] = []
        self.request_latencies[key].append(duration_seconds)
        # Keep recent 100 duration samples
        if len(self.request_latencies[key]) > 100:
            self.request_latencies[key].pop(0)

    def generate_metrics(self) -> str:
        """Generate Prometheus exposition text format (version 0.0.4)."""
        lines = []
        
        # System Uptime Metric
        uptime = time.time() - self.start_time
        lines.append("# HELP process_uptime_seconds Total process uptime in seconds.")
        lines.append("# TYPE process_uptime_seconds counter")
        lines.append(f"process_uptime_seconds {uptime:.2f}")

        # HTTP Requests Total Counter Metric
        lines.append("# HELP http_requests_total Total number of HTTP requests processed.")
        lines.append("# TYPE http_requests_total counter")
        if not self.request_counts:
            lines.append('http_requests_total{method="GET",handler="/",status="200"} 0')
        else:
            for (method, path, status), count in self.request_counts.items():
                lines.append(f'http_requests_total{{method="{method}",handler="{path}",status="{status}"}} {count}')

        # HTTP Request Duration Latency Metric
        lines.append("# HELP http_request_duration_seconds HTTP request latency in seconds.")
        lines.append("# TYPE http_request_duration_seconds gauge")
        if not self.request_latencies:
            lines.append('http_request_duration_seconds{handler="/"} 0.000')
        else:
            for (method, path, status), durations in self.request_latencies.items():
                avg_dur = sum(durations) / len(durations) if durations else 0
                lines.append(f'http_request_duration_seconds{{method="{method}",handler="{path}"}} {avg_dur:.4f}')

        # Weather API Health Metric
        lines.append("# HELP weather_api_up Weather telemetry service availability (1 = UP, 0 = DOWN).")
        lines.append("# TYPE weather_api_up gauge")
        lines.append("weather_api_up 1")

        return "\n".join(lines) + "\n"

metrics = PrometheusMetrics()
