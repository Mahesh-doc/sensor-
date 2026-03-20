from fastapi import FastAPI
from contextlib import asynccontextmanager
from monitoring_service import MonitoringService
from logger_config import setup_logger

logger = setup_logger()

# Create monitoring service
service = MonitoringService(logger)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info("Sensor Monitoring API is running")
    service.start_monitoring()
    yield
    # Shutdown code (optional)
    service.running = False
    logger.info("Sensor Monitoring API is shutting down")

# FastAPI app with lifespan handler
app = FastAPI(
    title="Sensor Monitoring API",
    version="0.1.0",
    lifespan=lifespan
)

# List all sensors
@app.get("/sensors")
def list_sensors():
    return service.list_sensors()

# Stop a sensor manually (includes failure reasons)
@app.post("/sensors/stop")
def stop_sensor():
    return service.stop_fuel_flow_sensor()