from dronekit import connect, VehicleMode
import time
import pyrebase

port = '/dev/ttyUSB0' # IF ERROR CHANGE TO /dev/ttyACM0
baudrate = 57600

config = {
    "apiKey": "AIzaSyBi8dJvahsGnlEJxt2XW9CbCVCZ_F8QbIA",
    "authDomain": "eco-enzym.firebaseapp.com",
    "databaseURL": "https://eco-enzym-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "eco-enzym",
    "storageBucket": "eco-enzym.appspot.com",
    "messagingSenderId": "1090135367285",
    "appId": "1:1090135367285:web:024ab437397e3ea199623c",
    "measurementId": "G-57LTEMH91G"
}

firebase = pyrebase.initialize_app(config=config)
db = firebase.database()

def run_motor():
    print("Connecting...")

    vehicle = connect(port, wait_ready=True, baud=baudrate)

    print("Setting to GUIDED")

    vehicle.mode = VehicleMode("GUIDED")
    while not vehicle.mode.name == "GUIDED":
        print("Cant change to GUIDED")
        time.sleep(1)
        
    print("Arming...")
    vehicle.armed = True
    while not vehicle.armed:
        print("Cant arming drone")
        time.sleep(1)
        
    print("Armed!")
    print("Setting throttle to 50%")
    vehicle.channels.overrides['3'] = 1500

    time.sleep(3)

    print("Stopping throttle")
    vehicle.channels.overrides['3'] = 1000
    vehicle.armed = False
    while vehicle.armed:
        print("Wait for disarm...")
        time.sleep(1)
        
    print("Disarmed!")
    vehicle.close()
    print("Koneksi ke Pixhawk ditutup.")
    
    db.child("motor").child("1").child("active").set(False)

def stream_handler(message):
    if message["data"] == True:
        print("Motor active command received")
        run_motor()
    elif message["data"] == False:
        print("Motor is inactive")


my_stream = db.child("motor").child("1").child("active").stream(stream_handler)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stream stopped")
    my_stream.close()