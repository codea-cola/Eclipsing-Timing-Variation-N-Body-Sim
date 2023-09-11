import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Constants for scaling to solar units
solar_mass = 1.989e30  # kg
solar_radius = 6.9634e8  # meters
au = 1.496e11  # meters
seconds_in_year = 3.154e7  # seconds
minutes_in_year = 525600  # minutes

# Function to calculate the period change of the binary system due to the third body (planet)
def calculate_period_change(m1, m2, m3, d12, d13):
    G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)

    # Convert parameters to SI units
    m1 *= solar_mass
    m2 *= solar_mass
    m3 *= solar_mass
    d12 *= au
    d13 *= au

    a12 = d12
    a13 = d13
    a23 = a12 + a13

    # Calculate semi-major axes
    a1 = a12 * (m2 / (m1 + m2))
    a2 = a12 * (m1 / (m1 + m2))
    a3 = a13

    # Calculate the change in period of the binary system
    delta_period = 2 * np.pi * (a23 ** 3) / (G * (m1 + m2) * (m1 + m2 + m3))

    return delta_period

# Function to calculate eclipsing timing variation
def calculate_etv(m1, m2, m3, d12, d13, ecc12, ecc13, period_binary, period_planet):
    delta_period = calculate_period_change(m1, m2, m3, d12, d13)

    # Convert periods to minutes
    period_binary *= minutes_in_year
    period_planet *= minutes_in_year
    delta_period *= minutes_in_year

    # Calculate ETV
    etv = []
    planet_periods = np.linspace(0.1 * period_planet, 2 * period_planet, 100)
    for planet_period in planet_periods:
        delta_t = delta_period * (ecc12 * np.sin((2 * np.pi * planet_period) / period_binary) + ecc13 * np.sin((2 * np.pi * planet_period) / period_planet))
        etv.append(delta_t)

    return planet_periods / minutes_in_year, etv

# Function to update the plot
def update_plot():
    m1 = float(mass1_entry.get())
    m2 = float(mass2_entry.get())
    m3 = float(mass3_entry.get())
    d12 = float(distance12_entry.get())
    d13 = float(distance13_entry.get())
    ecc12 = float(eccentricity12_entry.get())
    ecc13 = float(eccentricity13_entry.get())
    period_binary = float(period_binary_entry.get())
    period_planet = float(period_planet_entry.get())

    planet_periods, etv = calculate_etv(m1, m2, m3, d12, d13, ecc12, ecc13, period_binary, period_planet)

    ax.clear()
    ax.plot(planet_periods, etv)
    ax.set_xlabel('Period of the Planet (minutes)')
    ax.set_ylabel('ETV (Observed - Calculated) (minutes)')
    ax.set_title('Eclipsing Timing Variation\nETV = ΔP × (ecc12 * sin(2π * Tp / Pb) + ecc13 * sin(2π * Tp / Pp))')
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Eclipsing Timing Variation Simulator")

# Create input fields and labels
mass1_label = ttk.Label(root, text="Mass of Star 1 (solar masses):")
mass1_label.pack()
mass1_entry = ttk.Entry(root)
mass1_entry.pack()

mass2_label = ttk.Label(root, text="Mass of Star 2 (solar masses):")
mass2_label.pack()
mass2_entry = ttk.Entry(root)
mass2_entry.pack()

mass3_label = ttk.Label(root, text="Mass of Planet (solar masses):")
mass3_label.pack()
mass3_entry = ttk.Entry(root)
mass3_entry.pack()

distance12_label = ttk.Label(root, text="Distance between Star 1 and Star 2 (AU):")
distance12_label.pack()
distance12_entry = ttk.Entry(root)
distance12_entry.pack()

distance13_label = ttk.Label(root, text="Distance between Star 1 and Planet (AU):")
distance13_label.pack()
distance13_entry = ttk.Entry(root)
distance13_entry.pack()

eccentricity12_label = ttk.Label(root, text="Eccentricity of Star 1 and Star 2:")
eccentricity12_label.pack()
eccentricity12_entry = ttk.Entry(root)
eccentricity12_entry.pack()

eccentricity13_label = ttk.Label(root, text="Eccentricity of Star 1 and Planet:")
eccentricity13_label.pack()
eccentricity13_entry = ttk.Entry(root)
eccentricity13_entry.pack()

period_binary_label = ttk.Label(root, text="Period of Binary Star System (minutes):")
period_binary_label.pack()
period_binary_entry = ttk.Entry(root)
period_binary_entry.pack()

period_planet_label = ttk.Label(root, text="Period of Planet (minutes):")
period_planet_label.pack()
period_planet_entry = ttk.Entry(root)
period_planet_entry.pack()

calculate_button = ttk.Button(root, text="Calculate ETV", command=update_plot)
calculate_button.pack()

# Create a larger Matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
