import threading
import time
import yaml
import csv
import os

from sensor import Sensor
from email_service import send_email_alert
from health_checker import check_health
from config import HEALTH_INTERVAL

try:
    from predict_model import predict_status
except Exception:
    predict_status = None


class MonitoringService:
    def __init__(self, logger):
        self.logger = logger
        self.sensors = []
        self.running = True
        self.start_time = time.time()
        self._create_sensors()

    def _create_sensors(self):
        with open("sensors.yaml", "r") as file:
            data = yaml.safe_load(file)

        self.sensors = []

        for s in data["sensors"]:
            sensor = Sensor(
                sensor_id=s["sensor_id"],
                label=s["label"],
                code=s["code"],
                temperature=s["temperature"],
                pressure=s["pressure"],
                vibration=s["vibration"],
                fuel_flow=s["fuel_flow"],
                voltage=s["voltage"],
                speed=s["speed"],
                brake_pressure=s["brake_pressure"],
                humidity=s["humidity"],
                track_aligned=s["track_aligned"],
                engine_load=s["engine_load"]
            )
            self.sensors.append(sensor)

    def save_sensor_data(self, sensor):
        file_exists = os.path.exists("sensor_data.csv")

        row = {
            "temperature": sensor.temperature,
            "pressure": sensor.pressure,
            "vibration": sensor.vibration,
            "fuel_flow": sensor.fuel_flow,
            "voltage": sensor.voltage,
            "speed": sensor.speed,
            "brake_pressure": sensor.brake_pressure,
            "humidity": sensor.humidity,
            "track_aligned": int(sensor.track_aligned),
            "engine_load": sensor.engine_load,
            "status": "Failed" if not sensor.active else "Healthy"
        }

        with open("sensor_data.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

    def _monitor_loop(self):
        while self.running:
            time.sleep(HEALTH_INTERVAL)
            elapsed_time = time.time() - self.start_time

            for sensor in self.sensors:
                # Demo failure after 120 seconds for Fuel Flow Sensor
                if sensor.sensor_id == 4 and elapsed_time >= 120:
                    sensor.fuel_flow = 0

                is_healthy, reason = check_health(sensor)

                if is_healthy:
                    sensor.active = True
                    sensor.failure_reason = None
                    self.logger.info(f"{sensor.label} is healthy")
                else:
                    if sensor.active:
                        sensor.active = False
                        sensor.failure_reason = reason
                        self.logger.error(f"{sensor.label} FAILED - {reason}")

                        prediction = None
                        if predict_status is not None:
                            try:
                                prediction = predict_status(sensor)
                                self.logger.info(f"{sensor.label} ML Prediction: {prediction}")
                            except Exception as e:
                                self.logger.warning(f"Prediction skipped for {sensor.label}: {e}")

                        send_email_alert(sensor.label, reason, prediction)
                    else:
                        self.logger.error(f"{sensor.label} FAILED - {sensor.failure_reason}")

                self.save_sensor_data(sensor)

    def list_sensors(self):
        return [s.to_dict() for s in self.sensors]

    def stop_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id and sensor.active:
                sensor.stop("Stopped manually")
                self.logger.info(f"{sensor.label} stopped manually")
                send_email_alert(sensor.label, sensor.failure_reason, None)
                return {
                    "status": "success",
                    "message": f"{sensor.label} stopped"
                }

        return {"status": "error", "message": "Sensor not found or already inactive"}

    def stop_fuel_flow_sensor(self):
        fuel_sensor = next((s for s in self.sensors if s.sensor_id == 4), None)
        if fuel_sensor:
            return {
                "status": "failed" if not fuel_sensor.active else "healthy",
                "message": f"{fuel_sensor.label} status",
                "failure_reason": fuel_sensor.failure_reason
            }
        return {"status": "error", "message": "Fuel Flow Sensor not found"}

    def handle_command(self, cmd):
        if cmd == "list":
            return self.list_sensors()

        elif cmd.startswith("stop"):
            try:
                sensor_id = int(cmd.split()[1])
                return self.stop_sensor(sensor_id)
            except:
                return {"error": "Invalid command"}

        elif cmd == "fuel":
            return self.stop_fuel_flow_sensor()

        else:
            return {"error": "Unknown command"}