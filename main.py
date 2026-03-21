from logger_config import setup_logger
from monitoring_service import MonitoringService

def main():
    logger = setup_logger()

    service = MonitoringService(logger)
    service.start_monitoring()

    print("All sensors are healthy")

    while True:
        try:
            user_input = input("Enter sensor number to stop: ").strip()

            if not user_input.isdigit():
                print("Please enter a valid number.")
                continue

            sensor_id = int(user_input)

            result = service.stop_sensor(sensor_id)
            print(result["message"])

        except KeyboardInterrupt:
            print("\nExiting system...")
            service.running = False
            break

if __name__ == "__main__":
    main()