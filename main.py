import json
import csv
import random
from datetime import datetime, timedelta
from charts import *

import matplotlib.pyplot as plt

from HeatExchanger import HeatExchanger
from FlowMeter import FlowMeter

def random_string(prefix, length=5):
    return f"{prefix}{random.randint(100,999)}"

def generate_heat_exchangers(n=50):
    exchangers = []
    media = ["вода", "масло", "пар", "антифриз", "воздух"]
    for _ in range(n):
        model = random_string("HE")
        area = round(random.uniform(1, 100), 1)
        max_temp = random.randint(80, 300)
        max_pressure = random.randint(5, 50)
        medium = random.choice(media)
        exchangers.append(HeatExchanger(model, area, max_temp, max_pressure, medium))
    return exchangers

def generate_flow_meters(n=50):
    meters = []
    types = ["ультразвуковой", "электромагнитный", "вихревой", "кориолисов", "турбинный"]
    for _ in range(n):
        model = random_string("FM")
        mtype = random.choice(types)
        diameter = random.choice([25, 50, 80, 100, 150, 200])
        min_flow = round(random.uniform(0.1, 2.0), 1)
        max_flow = round(min_flow + random.uniform(2, 20), 1)
        error = round(random.uniform(0.005, 0.05), 3)
        meters.append(FlowMeter(model, mtype, diameter, (min_flow, max_flow), error))
    return meters

def generate_time_series(he, fm, n_points=100, delta_t=10):
    series = []
    start_time = datetime(2025, 3, 8, 0, 0, 0)
    for i in range(n_points):
        timestamp = start_time + timedelta(minutes=i*15)
        flow = fm.get_flow()
        heat = he.calculate_heat_flow(flow, delta_t)
        series.append({
            "time": timestamp.isoformat(),
            "flow": flow,
            "heat_flow": heat,
            "delta_t": delta_t
        })
    return series

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_to_csv(data, filename, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_all_data():
    try:
        with open("heat_exchangers.json", "r"):
            pass
        with open("flow_meters.json", "r"):
            pass
        with open("time_series.csv", "r"):
            pass
        print("Файлы данных уже существуют.")
        return
    except FileNotFoundError:
        print("Генерация новых данных...")

    he_list = generate_heat_exchangers(50)
    fm_list = generate_flow_meters(50)

    he_data = [{"id": he.id, "model": he.model, "area": he.area,
                "max_temp": he.max_temp, "max_pressure": he.max_pressure,
                "medium": he.medium} for he in he_list]
    fm_data = [{"id": fm.id, "model": fm.model, "type": fm.type,
                "diameter": fm.diameter, "flow_min": fm.flow_range[0],
                "flow_max": fm.flow_range[1], "error": fm.error} for fm in fm_list]

    save_to_json(he_data, "heat_exchangers.json")
    save_to_json(fm_data, "flow_meters.json")

    he_sample = he_list[0]
    fm_sample = fm_list[0]
    series = generate_time_series(he_sample, fm_sample, 120, delta_t=12)
    save_to_csv(series, "time_series.csv", ["time", "flow", "heat_flow", "delta_t"])

generate_all_data()
times = []
flows = []
heat_flows = []

with open("time_series.csv", "r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dt = datetime.fromisoformat(row['time'])
        times.append(dt)
        flows.append(float(row['flow']))
        heat_flows.append(float(row['heat_flow']))

plot1 = plot_heat_exchanger_characteristic()
plot2 = plot_flow_meter_time_series()