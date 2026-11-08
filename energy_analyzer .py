import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class EnergyAnalyzer:
    def __init__(self, rooms_file="rooms.csv", readings_file="readings.csv"):
        self.rooms_file = rooms_file
        self.readings_file = readings_file
        self.df = self.load_and_clean_data()
        self.last_price = None

    def load_and_clean_data(self):
        rooms_df = pd.read_csv(self.rooms_file)
        readings_df = pd.read_csv(self.readings_file)

        readings_df = readings_df.drop_duplicates()

        readings_df["actual_kwh"] = pd.to_numeric(readings_df["actual_kwh"], errors="coerce")
        readings_df["date"] = pd.to_datetime(readings_df["date"], errors="coerce")

        readings_df = readings_df.dropna(subset=["room_id", "date"])
        readings_df.loc[readings_df["actual_kwh"] < 0, "actual_kwh"] = np.nan

        readings_df["actual_kwh"] = readings_df.groupby("room_id")["actual_kwh"] \
                                               .transform(lambda s: s.fillna(s.median()))
        readings_df = readings_df.dropna(subset=["actual_kwh"])

        merged_df = pd.merge(readings_df, rooms_df, on="room_id", how="inner")
        merged_df["month"] = merged_df["date"].dt.to_period("M").astype(str)
        return merged_df.reset_index(drop=True)

    def calculate_cost_and_consumption(self, price_per_kwh):
        price_per_kwh = float(price_per_kwh)
        if price_per_kwh <= 0:
            raise ValueError("Price per kWh must be greater than zero.")
        self.last_price = price_per_kwh
        self.df["cost"] = self.df["actual_kwh"] * price_per_kwh

        room_summary = self.df.groupby(["room_id", "room_name"])[["actual_kwh", "cost"]].sum().round(2)
        building_summary = self.df.groupby("building")[["actual_kwh", "cost"]].sum().round(2)
        monthly_summary = self.df.groupby("month")[["actual_kwh", "cost"]].sum().round(2)
        return room_summary, building_summary, monthly_summary

    def simulate_ac_reduction(self, percentage):
        percentage = float(percentage)
        if not (0 <= percentage <= 100):
            raise ValueError("Reduction percentage must be between 0 and 100.")

        ac_power = self.df["ac_kw"].to_numpy()
        other_power = (self.df["lighting_kw"] + self.df["equipment_kw"]).to_numpy()
        hours = self.df["hours_per_day"].to_numpy()

        consumption_before = (ac_power + other_power) * hours
        reduced_ac_power = ac_power * (1 - percentage / 100)
        consumption_after = (reduced_ac_power + other_power) * hours

        comparison = pd.DataFrame({
            "room_id": self.df["room_id"],
            "date": self.df["date"],
            "consumption_before_kwh": consumption_before,
            "consumption_after_kwh": consumption_after,
            "savings_kwh": consumption_before - consumption_after
        })
        return comparison

    def export_reports(self, price_per_kwh, ac_percentage=15, output_dir="./reports"):
        os.makedirs(output_dir, exist_ok=True)
        room_sum, building_sum, monthly_sum = self.calculate_cost_and_consumption(price_per_kwh)
        sim = self.simulate_ac_reduction(ac_percentage)

        room_sum.to_csv(os.path.join(output_dir, "report_by_room.csv"))
        building_sum.to_csv(os.path.join(output_dir, "report_by_building.csv"))
        monthly_sum.to_csv(os.path.join(output_dir, "report_by_month.csv"))
        sim.to_csv(os.path.join(output_dir, "report_ac_simulation.csv"), index=False)
        self.df.to_csv(os.path.join(output_dir, "cleaned_merged_data.csv"), index=False)
        return sorted(os.listdir(output_dir))

    def generate_charts(self, output_dir="./charts", show=True):
        os.makedirs(output_dir, exist_ok=True)

        plt.figure(figsize=(10, 5))
        daily_trend = self.df.groupby("date")["actual_kwh"].sum()
        plt.plot(daily_trend.index, daily_trend.values, marker='o', color='b')
        plt.title("Total Daily Energy Consumption Over Time")
        plt.xlabel("Date")
        plt.ylabel("Energy Consumption (kWh)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "line_chart_trend.png"))
        if show:
            plt.show()
        plt.close()

        plt.figure(figsize=(8, 5))
        building_sum = self.df.groupby("building")["actual_kwh"].sum()
        building_sum.plot(kind="bar", color="orange")
        plt.title("Total Energy Consumption by Building")
        plt.xlabel("Building")
        plt.ylabel("Energy Consumption (kWh)")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "bar_chart_building.png"))
        if show:
            plt.show()
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.scatter(self.df["area_m2"], self.df["actual_kwh"], color="green", alpha=0.7)
        plt.title("Room Area vs Daily Energy Consumption")
        plt.xlabel("Area (m²)")
        plt.ylabel("Daily Consumption (kWh)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter_area_vs_consumption.png"))
        if show:
            plt.show()
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.hist(self.df["actual_kwh"], bins=15, color="purple", edgecolor="black")
        plt.title("Distribution of Daily Energy Consumption")
        plt.xlabel("Daily Consumption (kWh)")
        plt.ylabel("Frequency (number of days)")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "histogram_consumption.png"))
        if show:
            plt.show()
        plt.close()

        print(f"All charts generated and saved in '{output_dir}'.")
