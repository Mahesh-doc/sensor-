from config import *

def check_health(sensor):
    # Temperature Sensor
    if sensor.temperature > TEMP_THRESHOLD:
        return False, "Engine temperature above 60°C"

    # Pressure Sensor
    if sensor.pressure < PRESSURE_THRESHOLD:
        return False, "Oil pressure below 30 PSI"

    # Vibration Sensor
    if sensor.vibration > VIBRATION_THRESHOLD:
        return False, "Vibration above 5 mm/s"

    # Fuel Flow Sensor
    if sensor.fuel_flow < FUEL_FLOW_THRESHOLD:
        return False, "Fuel flow interrupted"

    # Voltage Sensor
    if sensor.voltage < VOLTAGE_THRESHOLD:
        return False, "Voltage below 210V"

    # Speed Sensor
    if sensor.speed > SPEED_THRESHOLD:
        return False, "Overspeed detected"

    # Brake Pressure Sensor
    if sensor.brake_pressure < BRAKE_PRESSURE_THRESHOLD:
        return False, "Brake pressure below safe limit"

    # Humidity Sensor
    if sensor.humidity > HUMIDITY_THRESHOLD:
        return False, "Humidity above 80%"

    # Track Alignment Sensor
    if not sensor.track_aligned:
        return False, "Track misalignment detected"

    # Engine Load Sensor
    if sensor.engine_load > ENGINE_LOAD_THRESHOLD:
        return False, "Excessive engine load"

    # If none of the conditions triggered
    return True, "Healthy"