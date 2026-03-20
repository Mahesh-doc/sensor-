import threading
import time
from sensor import Sensor

class MonitoringService:
    def __init__(self, logger):
        self.logger = logger
        self.sensors = []
        self.running = True

        # Track start time
        self.start_time = time.time()

        self._create_sensors()

    def _create_sensors(self):
        self.sensors = [
            Sensor(1, "Temperature Sensor", "SENSOR-1"),
            Sensor(2, "Pressure Sensor", "SENSOR-2"),
            Sensor(3, "Vibration Sensor", "SENSOR-3"),
            Sensor(4, "Fuel Flow Sensor", "SENSOR-4"),
            Sensor(5, "Voltage Sensor", "SENSOR-5"),
            Sensor(6, "Speed Sensor", "SENSOR-6"),
            Sensor(7, "Brake Pressure Sensor", "SENSOR-7"),
            Sensor(8, "Humidity Sensor", "SENSOR-8"),
            Sensor(9, "Track Alignment Sensor", "SENSOR-9"),
            Sensor(10, "Engine Load Sensor", "SENSOR-10"),
        ]

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

    def _monitor_loop(self):
        while self.running:
            time.sleep(5)

            elapsed_time = time.time() - self.start_time

            for sensor in self.sensors:

                # Fuel Flow Sensor (FAIL AFTER 2 MINUTES)
                if sensor.sensor_id == 4 and elapsed_time >= 120:
                    if sensor.active:
                        sensor.failure_reason = "Fuel flow interrupted"
                        sensor.active = False

                    self.logger.error(f"{sensor.label} FAILED - {sensor.failure_reason}")

                else:
                    if sensor.active:
                        self.logger.info(f"{sensor.label} is healthy")
                    else:
                        self.logger.error(f"{sensor.label} FAILED - {sensor.failure_reason}")

    def list_sensors(self):
        return [s.to_dict() for s in self.sensors]

    def stop_sensor(self, sensor_id):
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id and sensor.active:
                sensor.stop("Stopped manually")
                self.logger.info(f"{sensor.label} stopped manually")
                return {
                    "status": "success",
                    "message": f"{sensor.label} stopped",
                    "failure_reasons": {
                        "Temperature Sensor": "Overheating above 100°C",
                        "Pressure Sensor": "Pressure drop below 50 PSI",
                        "Vibration Sensor": "Vibration above 5 mm/s",
                        "Fuel Flow Sensor": "Fuel flow interrupted",
                        "Voltage Sensor": "Voltage fluctuation beyond safe range",
                        "Speed Sensor": "Overspeed detected",
                        "Brake Pressure Sensor": "Brake pressure below safe limit",
                        "Humidity Sensor": "Humidity above 80%",
                        "Track Alignment Sensor": "Track misalignment detected",
                        "Engine Load Sensor": "Excessive engine load"
                    }
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
                sensor_id = int(cmd.split()[1])   # ✅ FIXED INDENT
                return self.stop_sensor(sensor_id)
            except:
                return {"error": "Invalid command"}

        elif cmd == "fuel":
            return self.stop_fuel_flow_sensor()

        else:
            return {"error": "Unknown command"}