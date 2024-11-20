import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Змінні входу
temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'pressure')

# Змінні виходу
hot_valve = ctrl.Consequent(np.arange(-90, 91, 1), 'hot_valve')
cold_valve = ctrl.Consequent(np.arange(-90, 91, 1), 'cold_valve')

# Функції належності для температури
temperature['cold'] = fuzz.trapmf(temperature.universe, [0, 0, 25, 50])
temperature['cool'] = fuzz.trimf(temperature.universe, [25, 50, 75])
temperature['warm'] = fuzz.trimf(temperature.universe, [50, 75, 100])
temperature['hot'] = fuzz.trapmf(temperature.universe, [75, 100, 100, 100])

# Функції належності для тиску
pressure['low'] = fuzz.trimf(pressure.universe, [0, 0, 50])
pressure['medium'] = fuzz.trimf(pressure.universe, [0, 50, 100])
pressure['high'] = fuzz.trimf(pressure.universe, [50, 100, 100])

# Функції належності для кутів клапанів
hot_valve['big_left'] = fuzz.trimf(hot_valve.universe, [-90, -90, -45])
hot_valve['medium_left'] = fuzz.trimf(hot_valve.universe, [-90, -45, 0])
hot_valve['small_left'] = fuzz.trimf(hot_valve.universe, [-45, 0, 45])
hot_valve['small_right'] = fuzz.trimf(hot_valve.universe, [0, 45, 90])
hot_valve['medium_right'] = fuzz.trimf(hot_valve.universe, [45, 90, 90])
hot_valve['big_right'] = fuzz.trimf(hot_valve.universe, [45, 90, 90])

cold_valve['big_left'] = fuzz.trimf(cold_valve.universe, [-90, -90, -45])
cold_valve['medium_left'] = fuzz.trimf(cold_valve.universe, [-90, -45, 0])
cold_valve['small_left'] = fuzz.trimf(cold_valve.universe, [-45, 0, 45])
cold_valve['small_right'] = fuzz.trimf(cold_valve.universe, [0, 45, 90])
cold_valve['medium_right'] = fuzz.trimf(cold_valve.universe, [45, 90, 90])
cold_valve['big_right'] = fuzz.trimf(cold_valve.universe, [45, 90, 90])

# Визначення нечітких правил
rule1 = ctrl.Rule(temperature['hot'] & pressure['high'], (hot_valve['medium_left'], cold_valve['medium_right']))
rule2 = ctrl.Rule(temperature['hot'] & pressure['medium'], cold_valve['medium_right'])
rule3 = ctrl.Rule(temperature['warm'] & pressure['high'], hot_valve['small_left'])
rule4 = ctrl.Rule(temperature['warm'] & pressure['low'], (hot_valve['small_right'], cold_valve['small_right']))
rule5 = ctrl.Rule(temperature['warm'] & pressure['medium'], (hot_valve['small_left'], cold_valve['small_left']))
rule6 = ctrl.Rule(temperature['cool'] & pressure['high'], (hot_valve['medium_right'], cold_valve['medium_left']))
rule7 = ctrl.Rule(temperature['cool'] & pressure['medium'], (hot_valve['medium_right'], cold_valve['small_left']))
rule8 = ctrl.Rule(temperature['cold'] & pressure['low'], hot_valve['big_right'])
rule9 = ctrl.Rule(temperature['cold'] & pressure['high'], (hot_valve['medium_left'], cold_valve['medium_right']))
rule10 = ctrl.Rule(temperature['warm'] & pressure['high'], (hot_valve['small_left'], cold_valve['small_left']))
rule11 = ctrl.Rule(temperature['warm'] & pressure['low'], (hot_valve['small_right'], cold_valve['small_right']))

# Створення системи керування
valve_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11])
valve_simulation = ctrl.ControlSystemSimulation(valve_ctrl)

# Введення значень з консолі
temp_input = float(input("Введіть температуру води: "))
pressure_input = float(input("Введіть тиск води: "))

# Застосування значень
valve_simulation.input['temperature'] = temp_input
valve_simulation.input['pressure'] = pressure_input

# Виконання симуляції
valve_simulation.compute()

print(f"Кут повороту крану гарячої води: {valve_simulation.output['hot_valve']}")
print(f"Кут повороту крану холодної води: {valve_simulation.output['cold_valve']}")
