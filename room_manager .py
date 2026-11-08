import os
import csv


class Room:
    def __init__(self, room_id, room_name, building, area_m2, lighting_kw, ac_kw, equipment_kw, hours_per_day):
        self.room_id = str(room_id).strip()
        self.room_name = str(room_name).strip()
        self.building = str(building).strip()
        self.area_m2 = float(area_m2)
        self.lighting_kw = float(lighting_kw)
        self.ac_kw = float(ac_kw)
        self.equipment_kw = float(equipment_kw)
        self.hours_per_day = float(hours_per_day)

        self.validate()

    def validate(self):
        if not self.room_id:
            raise ValueError("Room ID cannot be empty.")
        if self.area_m2 <= 0:
            raise ValueError("Room area must be greater than zero.")
        if any(p < 0 for p in [self.lighting_kw, self.ac_kw, self.equipment_kw]):
            raise ValueError("Power values must be nonnegative.")
        if not (0 <= self.hours_per_day <= 24):
            raise ValueError("Operating hours must be between 0 and 24.")

    def total_power(self):
        return self.lighting_kw + self.ac_kw + self.equipment_kw

    def daily_energy_consumption(self):
        return self.total_power() * self.hours_per_day

    def consumption_per_square_meter(self):
        return self.daily_energy_consumption() / self.area_m2

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_name": self.room_name,
            "building": self.building,
            "area_m2": self.area_m2,
            "lighting_kw": self.lighting_kw,
            "ac_kw": self.ac_kw,
            "equipment_kw": self.equipment_kw,
            "hours_per_day": self.hours_per_day
        }


class RoomManager:
    FIELDNAMES = ["room_id", "room_name", "building", "area_m2",
                  "lighting_kw", "ac_kw", "equipment_kw", "hours_per_day"]
    TEXT_FIELDS = ("room_name", "building")      
    NUMBER_FIELDS = ("area_m2", "lighting_kw", "ac_kw", "equipment_kw", "hours_per_day")

    def __init__(self, filename="rooms.csv"):
        self.filename = filename
        self.rooms = {}         
        self.load_rooms()

    def load_rooms(self):
        self.rooms = {}
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        room = Room(
                            row["room_id"], row["room_name"], row["building"],
                            row["area_m2"], row["lighting_kw"], row["ac_kw"],
                            row["equipment_kw"], row["hours_per_day"]
                        )
                        self.rooms[room.room_id] = room
                    except (ValueError, KeyError, TypeError) as e:
                        print(f"Skipping invalid room: {e}")

    def save_rooms(self):
        with open(self.filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            for room in self.rooms.values():
                writer.writerow(room.to_dict())

    def add_room(self, room):
        if room.room_id in self.rooms:
            raise ValueError(f"Room ID {room.room_id} already exists.")
        self.rooms[room.room_id] = room
        self.save_rooms()

    def list_rooms(self, limit=None):
        if not self.rooms:
            print("No rooms available.")
            return
        rooms = list(self.rooms.values())
        if limit is not None:
            rooms = rooms[:limit]           
        for room in rooms:
            print(f"ID: {room.room_id} | Name: {room.room_name} | Building: {room.building} | "
                  f"Daily Energy: {room.daily_energy_consumption():.2f} kWh")

    def search_room(self, keyword):
        return self.rooms.get(str(keyword).strip())

    def search_by_name_or_building(self, text):
        text = str(text).strip().lower()
        return [r for r in self.rooms.values()
                if text in r.room_name.lower() or text in r.building.lower()]

    def update_room(self, room_id, **kwargs):
        if room_id not in self.rooms:
            raise ValueError("Room ID not found.")
        room = self.rooms[room_id]
        backup = room.to_dict()               
        try:
            for key, value in kwargs.items():
                if key in self.TEXT_FIELDS:
                    setattr(room, key, str(value).strip())
                elif key in self.NUMBER_FIELDS:
                    setattr(room, key, float(value))
                else:
                    raise ValueError(f"Field '{key}' cannot be updated.")
            room.validate()
        except ValueError:
            for key, value in backup.items():  # rollback
                setattr(room, key, value)
            raise
        self.save_rooms()


    def total_daily_consumption(self):
        return sum(r.daily_energy_consumption() for r in self.rooms.values())

    def buildings(self):
        return {r.building for r in self.rooms.values()}

    def print_energy_report(self):
        if not self.rooms:
            print("No rooms available.")
            return
        print(f"{'ID':<5}{'Room':<18}{'Building':<16}{'kWh/day':>10}{'kWh/m2':>10}")
        for r in self.rooms.values():
            print(f"{r.room_id:<5}{r.room_name:<18}{r.building:<16}"
                  f"{r.daily_energy_consumption():>10.2f}{r.consumption_per_square_meter():>10.2f}")
        print(f"\nTotal daily consumption of all rooms: {self.total_daily_consumption():.2f} kWh")
        print(f"Buildings: {', '.join(sorted(self.buildings()))}")
