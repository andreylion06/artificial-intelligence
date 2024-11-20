import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Вхідні нечіткі змінні
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
temperature_change = ctrl.Antecedent(np.arange(-10, 11, 1), 'temperature_change')

# Вихідна нечітка змінна
regulator_angle = ctrl.Consequent(np.arange(-90, 91, 1), 'regulator_angle')

# Терміни для температури
temperature['very_cold'] = fuzz.trimf(temperature.universe, [0, 0, 10])
temperature['cold'] = fuzz.trimf(temperature.universe, [5, 10, 15])
temperature['comfortable'] = fuzz.trimf(temperature.universe, [15, 20, 25])
temperature['warm'] = fuzz.trimf(temperature.universe, [20, 25, 30])
temperature['very_warm'] = fuzz.trimf(temperature.universe, [25, 40, 40])

# Терміни для зміни температури
temperature_change['decreasing'] = fuzz.trimf(temperature_change.universe, [-10, -10, 0])
temperature_change['constant'] = fuzz.trimf(temperature_change.universe, [-1, 0, 1])
temperature_change['increasing'] = fuzz.trimf(temperature_change.universe, [0, 10, 10])

# Терміни для кута повороту регулятора
regulator_angle['large_left'] = fuzz.trimf(regulator_angle.universe, [-90, -90, -45])
regulator_angle['small_left'] = fuzz.trimf(regulator_angle.universe, [-45, -22.5, 0])
regulator_angle['off'] = fuzz.trimf(regulator_angle.universe, [-5, 0, 5])
regulator_angle['small_right'] = fuzz.trimf(regulator_angle.universe, [0, 22.5, 45])
regulator_angle['large_right'] = fuzz.trimf(regulator_angle.universe, [45, 90, 90])

# Правила керування
rule1 = ctrl.Rule(temperature['very_warm'] & temperature_change['increasing'], regulator_angle['large_left'])
rule2 = ctrl.Rule(temperature['very_warm'] & temperature_change['decreasing'], regulator_angle['small_left'])
rule3 = ctrl.Rule(temperature['warm'] & temperature_change['increasing'], regulator_angle['large_left'])
rule4 = ctrl.Rule(temperature['warm'] & temperature_change['decreasing'], regulator_angle['off'])
rule5 = ctrl.Rule(temperature['very_cold'] & temperature_change['decreasing'], regulator_angle['large_right'])
rule6 = ctrl.Rule(temperature['very_cold'] & temperature_change['increasing'], regulator_angle['small_right'])
rule7 = ctrl.Rule(temperature['cold'] & temperature_change['decreasing'], regulator_angle['large_right'])
rule8 = ctrl.Rule(temperature['cold'] & temperature_change['increasing'], regulator_angle['off'])
rule9 = ctrl.Rule(temperature['very_warm'] & temperature_change['constant'], regulator_angle['large_left'])
rule10 = ctrl.Rule(temperature['warm'] & temperature_change['constant'], regulator_angle['small_left'])
rule11 = ctrl.Rule(temperature['very_cold'] & temperature_change['constant'], regulator_angle['large_right'])
rule12 = ctrl.Rule(temperature['cold'] & temperature_change['constant'], regulator_angle['small_right'])
rule13 = ctrl.Rule(temperature['comfortable'] & temperature_change['increasing'], regulator_angle['small_left'])
rule14 = ctrl.Rule(temperature['comfortable'] & temperature_change['decreasing'], regulator_angle['small_right'])
rule15 = ctrl.Rule(temperature['comfortable'] & temperature_change['constant'], regulator_angle['off'])

# Система керування
aircon_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                  rule11, rule12, rule13, rule14, rule15])
aircon = ctrl.ControlSystemSimulation(aircon_ctrl)

# Введення параметрів з консолі
temp_input = float(input("Введіть поточну температуру повітря: "))
temp_change_input = float(input("Введіть швидкість зміни температури (додатня для зростання, від'ємна для зниження): "))

aircon.input['temperature'] = temp_input
aircon.input['temperature_change'] = temp_change_input

# Обчислення результату
aircon.compute()

# Вивід результату з описом
angle_output = aircon.output['regulator_angle']
print(f"Кут повороту регулятора: {angle_output}")
