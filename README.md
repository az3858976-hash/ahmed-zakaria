
NAME/ AHMED ZAKARIA FAYZ

# Building Energy Analyzer

 Assignment 01 – Building Energy Analyzer

## Project Description

A Python application that calculates and analyzes the energy consumption of rooms in a building.
It is made of two connected modules, linked together by a menu in `main.py`.

**Module 1 – Energy Consumption Calculator (`room_manager.py`)**
- `Room` class: name, building, area, lighting / AC / equipment power (kW) and daily operating hours.
- `RoomManager` class: add, list, search and update rooms, saved to `rooms.csv`.
- Calculates daily energy consumption, total consumption and consumption per square meter.
- Input validation: area > 0, power values >= 0, operating hours between 0 and 24.

**Module 2 – Consumption and Cost Analysis (`energy_analyzer.py`)**
- Reads `readings.csv` (room ID, date, actual daily kWh) and cleans it with pandas
  (removes duplicates, handles missing/negative values) then merges it with the room data.
- Calculates consumption and cost per room, per building and per month using a user-entered price per kWh.
- Uses NumPy to compare consumption before and after reducing AC power by a user-selected percentage
  (operating hours, lighting and equipment stay unchanged).
- Creates 4 Matplotlib charts (line, bar, scatter, histogram) and saves them as PNG files.
- Exports reports as CSV files.

## Project Structure

```
├── main.py                  # menu that connects both modules
├── room_manager.py          # Module 1
├── energy_analyzer.py       # Module 2
├── room_manager.ipynb       # notebook for Module 1 + tests
├── energy_analyzer.ipynb    # notebook for Module 2 + analysis + tests
├── main.ipynb               # notebook to run the full program
├── rooms.csv                # sample dataset: 8 rooms, 2 buildings
├── readings.csv             # sample dataset: daily readings, Aug–Sep 2026
├── reports/                 # exported CSV reports (created when you run the program)
└── charts/                  # exported PNG charts (created when you run the program)
```

## Required Libraries

- Python 3.9+
- pandas
- numpy
- matplotlib
- jupyter (only to run the notebooks)

Install them with:

```bash
pip install pandas numpy matplotlib jupyter
```

## How to Run

Keep all files in the same folder (`rooms.csv` and `readings.csv` must be next to the code).

**Option 1 – From the terminal**

```bash
python main.py
```

**Option 2 – From Jupyter Notebook**

```bash
jupyter notebook
```

Then open and run the notebooks in this order:
1. `room_manager.ipynb`
2. `energy_analyzer.ipynb`
3. `main.ipynb` (type the menu number in the box under the cell)

If Jupyter shows an old error after you edit a `.py` file, use **Kernel → Restart**.

## Menu Options

| Option | Action |
|--------|--------|
| 1 | List rooms |
| 2 | Add room |
| 3 | Search room (by ID, name or building) |
| 4 | Update room |
| 5 | Room energy report (daily kWh, kWh/m², total) |
| 6 | Consumption & cost analysis (asks for price per kWh) |
| 7 | Simulate AC power reduction (asks for percentage) |
| 8 | Generate and show charts (saved as PNG in `charts/`) |
| 9 | Export CSV reports (saved in `reports/`) |
| 0 | Exit |

## Formulas

- Daily energy consumption (kWh) = total power (kW) × operating hours
- Consumption per square meter = daily energy consumption ÷ room area

## Tests

The notebooks contain 3 valid and 3 invalid test cases for each module,
with the expected and actual results.

## Repository Link

https://github.com/az3858976-hash/ahmed-zakaria.git
