class SensorRegistry:
    def __init__(self):
        self.sensors = {}

    def get(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError(f"Sensor with ID '{sensor_id}' not found.")
        return self.sensors[sensor_id]

class SensorNotFoundError(Exception):
    pass