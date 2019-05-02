from datetime import datetime
from queue import Queue

from Simulator import Simulator
from Detector import Detector


def main():
    queue = Queue(1000)

    duration = 24
    toll_count = 20
    connectivity = 0.2
    distance = range(10, 20)
    vehicle_count = 1000
    vehicle_model_dist = ['BMW', 'Audi', 'Fiat', 'Mercedes-Benz', 'Chrysler', 'Nissan', 'Volvo', 'Mazda', 'Mitsubishi',
                          'Ferrari', 'Alfa Romeo', 'Toyota', 'Maybach', 'Porsche', 'Hyundai', 'Honda', 'Suzuki', 'Ford',
                          'Cadillac', 'Kia', 'Bentley', 'Chevrolet', 'Dodge', 'Lamborghini', 'Lincoln', 'Subaru',
                          'Volkswagen', 'Spyker', 'Rolls-Royce', 'Maserati', 'Lexus', 'Aston Martin', 'Land Rover',
                          'Tesla', 'Bugatti', ]
    vehicle_type_dist = {'car': 0.6, 'bus': 0.2, 'truck': 0.2}
    vehicle_luxury_dist = {'yes': 0.4, 'no': 0.6}
    toll_type_dist = {'checkpoint': 0.4, 'net': 0.6}
    toll_position_dist = {'in': 0.1, 'out': 0.1, 'mid': 0.8}
    environment_datetime = datetime.now()

    simulator = Simulator(queue,
                          toll_count, connectivity, distance,
                          vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist,
                          toll_type_dist, toll_position_dist,
                          environment_datetime,
                          duration)

    detector = Detector(queue, toll_count, vehicle_count)

    simulator.start()
    detector.start()
    simulator.join()
    detector.stop()


if __name__ == "__main__":
    main()
