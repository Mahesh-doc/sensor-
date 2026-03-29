class Sensor:
    def __init__(
        self,
        sensor_id,
        label,
        code,
        temperature=50,
        pressure=40,
        vibration=2.0,
        fuel_flow=20,
        voltage=220,
        speed=70,
        brake_pressure=60,
        humidity=45,
        track_aligned=True,
        engine_load=55
    ):
        self.sensor_id = sensor_id
        self.label = label
        self.code = code
        self.active = True

        self.temperature = temperature
        self.pressure = pressure
        self.vibration = vibration
        self.fuel_flow = fuel_flow
        self.voltage = voltage
        self.speed = speed
        self.brake_pressure = brake_pressure
        self.humidity = humidity
        self.track_aligned = track_aligned
        self.engine_load = engine_load

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
            "temperature": self.temperature,
            "pressure": self.pressure,
            "vibration": self.vibration,
            "fuel_flow": self.fuel_flow,
            "voltage": self.voltage,
            "speed": self.speed,
            "brake_pressure": self.brake_pressure,
            "humidity": self.humidity,
            "track_aligned": self.track_aligned,
            "engine_load": self.engine_load,
            "failure_reason": self.failure_reason
        }