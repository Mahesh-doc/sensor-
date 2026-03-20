class Sensor:
    def __init__(self, sensor_id, label, code):
        self.sensor_id = sensor_id
        self.label = label   # "Temperature Sensor"
        self.code = code     # "SENSOR-1"
        self.active = True

        self.temperature = 50
        self.pressure = 40
        self.vibration = 2.0
        self.voltage = 220

        self.failure_reason = None

    def stop(self, reason):
        self.active = False
        self.failure_reason = reason

    def to_dict(self):
        return {
            "id": self.sensor_id,
            "label": self.label,
            "code": self.code,
            "active": self.active,
            "failure_reason": self.failure_reason
        }