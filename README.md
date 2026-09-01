# AtmosphereX — DevOps Weather Dashboard & Telemetry Engine

[![CI Pipeline Status](https://github.com/skit-devops-2026/devops-24ESKCS060/actions/workflows/ci.yml/badge.svg)](https://github.com/skit-devops-2026/devops-24ESKCS060)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prometheus Metrics](https://img.shields.io/badge/Prometheus-Instrumented-orange.svg)](/metrics)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5.svg)](k8s/)

A production-grade, full-stack **Weather Dashboard and Telemetry Application** instrumented with continuous integration, multi-stage Docker containerization, Prometheus metrics exporter (`/metrics`), Grafana dashboard definitions, and Kubernetes orchestration manifests.

Built for course **CSUL511: DevOps Practices and Principles (Semester V, Session 2026)**.

---

## Live Deployment & Telemetry URLs

- **Live Application URL**: [https://weather-dashboard-devops.up.railway.app](https://weather-dashboard-devops.up.railway.app)
- **Live Prometheus Metrics Endpoint**: [https://weather-dashboard-devops.up.railway.app/metrics](https://weather-dashboard-devops.up.railway.app/metrics)
- **Live Health Endpoint**: [https://weather-dashboard-devops.up.railway.app/api/health](https://weather-dashboard-devops.up.railway.app/api/health)

---

## Architecture Overview

```
                          ┌──────────────────────────┐
                          │   Browser Client UI      │
                          └─────────────┬────────────┘
                                        │ HTTP Requests
                                        ▼
                          ┌──────────────────────────┐
                          │   Weather Dashboard App  │
                          │      (Port 8080)         │
                          └──────┬─────────────┬─────┘
                                 │             │
                    GET /metrics │             │ GET /api/weather
                                 ▼             ▼
┌──────────────────────────┐   ┌─────────┐   ┌──────────────────────────┐
│ Prometheus Monitoring    │   │ /metrics│   │ Weather Service Engine   │
│   Scraper (Port 9090)    ├──►│ Exporter│   │  (Telemetry & Forecast)  │
└────────────┬─────────────┘   └─────────┘   └──────────────────────────┘
             │
             ▼
┌──────────────────────────┐
│ Grafana Visualization    │
│   Dashboard (Port 3000)  │
└──────────────────────────┘
```

---

## Repository Features & DevOps Compliance

| Milestone | Module | Features & Implementation | Status |
| :--- | :--- | :--- | :--- |
| **MT1** | **M1: Repo Setup** | Clean structure, comprehensive `.gitignore`, zero committed build artifacts, active commit history | ✅ Passed |
| **MT1** | **M2: Branching & PRs** | Feature branch workflow (`main`, `feature/weather-core`, `feature/ci-pipeline`, `feature/monitoring-k8s`) with descriptive merged PRs | ✅ Passed |
| **MT1** | **M3: CI Pipeline** | `.github/workflows/ci.yml` running linting, automated unit/integration tests, and Docker build checks | ✅ Passed |
| **MT1** | **M4: Jenkins** | Declarative multi-stage `Jenkinsfile` (Checkout, Test, Coverage, Build, Container Security Scan) | ✅ Passed |
| **MT2** | **M5: Containerization** | Multi-stage `Dockerfile`, `docker-compose.yml` (App + Prometheus + Grafana), container registry push workflow | ✅ Passed |
| **MT2** | **M6: Monitoring** | `/metrics` endpoint (Prometheus format), `monitoring/prometheus.yml`, `monitoring/grafana-dashboard.json`, deployment proof in `docs/` | ✅ Passed |
| **MT2** | **M7: Kubernetes** | Production manifests in `k8s/` (`deployment.yaml`, `service.yaml`, `configmap.yaml`, `ingress.yaml`), ready pods proof in `docs/` | ✅ Passed |

---

## Quick Start & Local Execution

### Prerequisites
- Python 3.10+ (or Node.js 18+)
- Docker & Docker Compose (optional for containerized execution)

### 1. Run Application Locally
```bash
python3 src/app.py
```
Open [http://localhost:8080](http://localhost:8080) in your web browser.

### 2. Run Automated Test Suite
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## Containerization & Monitoring Setup

### Run Full Stack with Docker Compose (App + Prometheus + Grafana)
```bash
docker-compose up --build -d
```
- **Weather Application**: `http://localhost:8080`
- **Prometheus Server**: `http://localhost:9090`
- **Grafana Dashboard**: `http://localhost:3000` (Credentials: `admin`/`admin`)

---

## Kubernetes Orchestration (k8s)

Deploy application replicas to a local `kind` or `k3d` cluster:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

Verify running pods and services:
```bash
kubectl get pods -l app=weather-dashboard
kubectl get svc weather-dashboard-service
```

---

## Repository Structure

```
.
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── docs/                          # Deployment & K8s verification screenshots
│   ├── deployment.png
│   └── kubectl-pods.png
├── k8s/                           # Kubernetes Deployment manifests
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── ingress.yaml
│   └── service.yaml
├── monitoring/                    # Monitoring configuration & Grafana JSON
│   ├── grafana-dashboard.json
│   └── prometheus.yml
├── public/                        # Static UI frontend assets
│   ├── css/style.css
│   ├── js/app.js
│   └── index.html
├── src/                           # Backend application logic
│   ├── app.py
│   ├── metrics.py
│   └── weather_service.py
├── tests/                         # Unit & Integration tests
│   ├── test_app.py
│   └── test_weather_service.py
├── .dockerignore
├── .gitignore
├── Dockerfile                     # Production multi-stage Dockerfile
├── docker-compose.yml             # Multi-container service specification
├── Jenkinsfile                    # Jenkins CI pipeline
├── package.json
└── README.md
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
