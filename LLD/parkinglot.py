from enum import Enum
from datetime import datetime, timedelta
import uuid

class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

class Vehicle:
    def __init__(self, plate_number: str, vehicle_type: VehicleType):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

class ParkingSpot:
    def __init__(self, spot_id: str, vehicle_type: VehicleType):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_free = True
        self.vehicle = None

    def park_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_free = False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_free = True

class ParkingLevel:
    def __init__(self, level_id: int, spots: list[ParkingSpot]):
        self.level_id = level_id
        self.spots = spots

    def find_free_spot(self, vehicle_type: VehicleType):
        for spot in self.spots:
            if spot.is_free and spot.vehicle_type == vehicle_type:
                return spot
        return None

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot, level_id: int):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot_id = spot.spot_id
        self.level_id = level_id
        self.issue_time = datetime.now()

    def calculate_fee(self, exit_time: datetime):
        duration = exit_time - self.issue_time
        hours = max(1, duration.total_seconds() // 3600)
        rate = {VehicleType.BIKE: 10, VehicleType.CAR: 20, VehicleType.TRUCK: 30}
        return rate[self.vehicle.vehicle_type] * hours

class ParkingLot:
    def __init__(self, levels: list[ParkingLevel]):
        self.levels = levels
        self.active_tickets = {}  # ticket_id -> Ticket

    def park_vehicle(self, vehicle: Vehicle):
        for level in self.levels:
            spot = level.find_free_spot(vehicle.vehicle_type)
            if spot:
                spot.park_vehicle(vehicle)
                ticket = Ticket(vehicle, spot, level.level_id)
                self.active_tickets[ticket.ticket_id] = ticket
                print(f"Vehicle parked. Ticket ID: {ticket.ticket_id}")
                return ticket
        print("Parking Full")
        return None

    def exit_vehicle(self, ticket_id: str):
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            print("Invalid Ticket ID")
            return None

        level = self.levels[ticket.level_id]
        spot = next((s for s in level.spots if s.spot_id == ticket.spot_id), None)
        if spot:
            spot.remove_vehicle()
            fee = ticket.calculate_fee(datetime.now())
            del self.active_tickets[ticket_id]
            print(f"Vehicle exited. Fee: {fee}")
            return fee
        print("Spot not found")
        return None



# Create spots
spots_level_0 = [ParkingSpot(f"S0{i}", VehicleType.CAR) for i in range(5)] + \
                [ParkingSpot(f"S0b{i}", VehicleType.BIKE) for i in range(3)]

spots_level_1 = [ParkingSpot(f"S1{i}", VehicleType.CAR) for i in range(5)] + \
                [ParkingSpot(f"S1t{i}", VehicleType.TRUCK) for i in range(2)]

# Create levels
level_0 = ParkingLevel(0, spots_level_0)
level_1 = ParkingLevel(1, spots_level_1)

# Create lot
lot = ParkingLot([level_0, level_1])

# Park vehicles
v1 = Vehicle("KA-01-HH-1234", VehicleType.CAR)
ticket1 = lot.park_vehicle(v1)

# Simulate exit after some time
import time
time.sleep(2)
lot.exit_vehicle(ticket1.ticket_id)
