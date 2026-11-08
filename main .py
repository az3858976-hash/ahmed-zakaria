from room_manager import Room, RoomManager
from energy_analyzer import EnergyAnalyzer


def ask_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def add_room_menu(manager):
    print("\n--- Add a new room ---")
    try:
        room = Room(
            input("Room ID (e.g. R09): "),
            input("Room name: "),
            input("Building: "),
            ask_float("Area (m2): "),
            ask_float("Lighting power (kW): "),
            ask_float("AC power (kW): "),
            ask_float("Equipment power (kW): "),
            ask_float("Operating hours per day (0-24): "),
        )
        manager.add_room(room)
        print("Room added and saved to rooms.csv.")
    except ValueError as e:
        print(f"Error: {e}")


def search_room_menu(manager):
    text = input("\nEnter room ID, name or building: ")
    room = manager.search_room(text)
    results = [room] if room else manager.search_by_name_or_building(text)
    if not results:
        print("No matching room found.")
        return
    for r in results:
        print(f"{r.room_id} | {r.room_name} | {r.building} | {r.area_m2} m2 | "
              f"L={r.lighting_kw} kW, AC={r.ac_kw} kW, Eq={r.equipment_kw} kW | {r.hours_per_day} h/day | "
              f"{r.daily_energy_consumption():.2f} kWh/day | {r.consumption_per_square_meter():.2f} kWh/m2")


def update_room_menu(manager):
    room_id = input("\nRoom ID to update: ").strip()
    if manager.search_room(room_id) is None:
        print("Room ID not found.")
        return
    field = input("Field (room_name, building, area_m2, lighting_kw, ac_kw, equipment_kw, hours_per_day): ").strip()
    value = input("New value: ")
    try:
        manager.update_room(room_id, **{field: value})
        print("Room updated and saved.")
    except ValueError as e:
        print(f"Error: {e}")


def analysis_menu(price):
    analyzer = EnergyAnalyzer(rooms_file="rooms.csv", readings_file="readings.csv")
    room_sum, building_sum, monthly_sum = analyzer.calculate_cost_and_consumption(price)
    print("\n--- Consumption & cost by room ---")
    print(room_sum)
    print("\n--- Consumption & cost by building ---")
    print(building_sum)
    print("\n--- Consumption & cost by month ---")
    print(monthly_sum)


def simulation_menu(percentage):
    analyzer = EnergyAnalyzer(rooms_file="rooms.csv", readings_file="readings.csv")
    result = analyzer.simulate_ac_reduction(percentage)
    print(result.head())
    print(f"\nTotal before: {result['consumption_before_kwh'].sum():.2f} kWh")
    print(f"Total after : {result['consumption_after_kwh'].sum():.2f} kWh")
    print(f"Total saved : {result['savings_kwh'].sum():.2f} kWh")


def main():
    print("   -- Starting Building Energy Analyzer --   ")

    manager = RoomManager("rooms.csv")

    while True:
        print("\n--- MENU ---")
        print("1. List rooms")
        print("2. Add room")
        print("3. Search room")
        print("4. Update room")
        print("5. Room energy report (daily kWh, kWh/m2, total)")
        print("6. Consumption & cost analysis")
        print("7. Simulate AC power reduction")
        print("8. Generate & show charts (PNG)")
        print("9. Export CSV reports")
        print("0. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                manager.list_rooms()
            elif choice == "2":
                add_room_menu(manager)
            elif choice == "3":
                search_room_menu(manager)
            elif choice == "4":
                update_room_menu(manager)
            elif choice == "5":
                manager.print_energy_report()
            elif choice == "6":
                analysis_menu(ask_float("Price per kWh: "))
            elif choice == "7":
                simulation_menu(ask_float("AC reduction percentage (0-100): "))
            elif choice == "8":
                EnergyAnalyzer("rooms.csv", "readings.csv").generate_charts()
            elif choice == "9":
                price = ask_float("Price per kWh: ")
                pct = ask_float("AC reduction percentage (0-100): ")
                files = EnergyAnalyzer("rooms.csv", "readings.csv").export_reports(price, pct)
                print("Reports saved in ./reports :", files)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")
        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
