import serial
import time
import os

SERIAL_PORT = "/dev/ttyUSB0"  # Adjust as needed
BAUD_RATE = 115200
LOG_FILE = "temperature_readings.log"

def send_command(ser, command):
    ser.write(command.encode('utf-8'))
    ser.flush()

def start_system(ser):
    send_command(ser, "START\n")
    print("System started...")

def stop_system(ser):
    send_command(ser, "STOP\n")
    print("System stopped...")

def preview_live_readings(ser):
    print("Previewing live readings (press Ctrl+C to stop)...")
    try:
        while True:
            if ser.in_waiting:
                reading = ser.readline().decode('utf-8').strip()
                print(f"Temperature: {reading}°C")
                with open(LOG_FILE, "a") as log:
                    log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {reading}°C\n")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped live preview.")

def view_past_readings():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            print("\n--- Past Temperature Readings ---")
            print(log.read())
    else:
        print("No past readings available.")

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow serial connection to establish

    menu = """
    1. Start System
    2. Stop System
    3. Preview Live Readings
    4. View Past Readings
    5. Exit
    """

    while True:
        print(menu)
        choice = input("Enter your choice: ")

        if choice == '1':
            start_system(ser)
        elif choice == '2':
            stop_system(ser)
        elif choice == '3':
            preview_live_readings(ser)
        elif choice == '4':
            view_past_readings()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

    ser.close()

if __name__ == "__main__":
    main()