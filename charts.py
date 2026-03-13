import matplotlib.pyplot as plt
import numpy as np
from HeatExchanger import HeatExchanger
from FlowMeter import FlowMeter


def plot_heat_exchanger_characteristic():
    he = HeatExchanger("Теплообменник-1", 50, 150, 20, "вода")
    
    flow_rates = np.linspace(0, 100, 20)
    delta_temps = [10, 20, 30, 40]
    
    plt.figure(figsize=(10, 6))
    
    for dt in delta_temps:
        heat_flows = []
        for flow in flow_rates:
            q = he.calculate_heat_flow(flow, dt)
            heat_flows.append(q / 1000)
        
        plt.plot(flow_rates, heat_flows, label=f'ΔT = {dt}°C', linewidth=2)
    
    plt.title('Характеристика теплообменника\nЗависимость теплового потока от расхода', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Расход теплоносителя, кг/с', fontsize=12)
    plt.ylabel('Тепловой поток, кВт', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    max_power = he.theoretical_max_power / 1000
    plt.axhline(y=max_power, color='r', linestyle='--', 
                label=f'Max теоритическая ({max_power:.0f} кВт)', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('heat_exchanger_characteristic.png', dpi=150)
    plt.show()
    
    return he


def plot_flow_meter_time_series():
    fm = FlowMeter("Расходомер-1", "ультразвуковой", 100, (20, 80), 0.03)
    
    time = np.linspace(0, 60, 100)
    true_flow = 50 + 20 * np.sin(2 * np.pi * time / 30)
    
    measured_flow = []
    errors = []
    
    for t, q_true in zip(time, true_flow):
        error_factor = 1 + np.random.uniform(-fm.error, fm.error)
        q_meas = q_true * error_factor
        measured_flow.append(q_meas)
        errors.append(abs(q_meas - q_true))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    ax1.plot(time, true_flow, 'b-', label='Истинный расход', linewidth=2)
    ax1.plot(time, measured_flow, 'r--', label='Измеренный расход', linewidth=1.5, alpha=0.7)
    ax1.fill_between(time, true_flow, measured_flow, alpha=0.2, color='gray')
    
    ax1.set_title('Показания расходомера во времени', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Время, мин', fontsize=12)
    ax1.set_ylabel('Расход, кг/с', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    
    ax1.axhline(y=fm.flow_range[0], color='green', linestyle=':', 
                label=f'Мин диапазон: {fm.flow_range[0]} кг/с')
    ax1.axhline(y=fm.flow_range[1], color='green', linestyle=':', 
                label=f'Макс диапазон: {fm.flow_range[1]} кг/с')
    
    ax2.plot(time, errors, 'purple', linewidth=2)
    ax2.fill_between(time, 0, errors, alpha=0.3, color='purple')
    
    ax2.set_title('Абсолютная погрешность измерения', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Время, мин', fontsize=12)
    ax2.set_ylabel('Погрешность, кг/с', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    mean_error = np.mean(errors)
    ax2.axhline(y=mean_error, color='red', linestyle='--', 
                label=f'Средняя погрешность: {mean_error:.3f} кг/с')
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig('flow_meter_time_series.png', dpi=150)
    plt.show()
    
    return fm