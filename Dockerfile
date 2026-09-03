# Stage 1: Build & Dependencies
FROM python:3.11-alpine AS builder

WORKDIR /app

# Copy application requirements if present
COPY src/ /app/src/
COPY public/ /app/public/
COPY tests/ /app/tests/

# Stage 2: Minimal Production Image
FROM python:3.11-alpine AS runner

WORKDIR /app

# Create unprivileged security user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy built application source
COPY --from=builder /app /app

# Expose web server port
EXPOSE 8080

# Configure environment defaults
ENV PORT=8080 \
    PYTHONUNBUFFERED=1

# Set ownership & non-root user context
USER appuser

# Healthcheck for container health verification
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/api/health || exit 1

# Start Weather HTTP Server
CMD ["python", "src/app.py"]
