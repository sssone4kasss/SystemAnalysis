import argparse
import json
import numpy as np
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def parse_membership_functions(mf_data, target_variable):
    """
    Функция для настройки функций принадлежности для переменной
    :param mf_data: данные для функций принадлежности
    :param target_variable: переменная, к которой будут применяться функции принадлежности
    :return: None
    """
    for mf in mf_data:
        points = np.array(mf['points'])
        target_variable[mf['id']] = fuzz.trapmf(target_variable.universe, [points[0][0], points[1][0], points[2][0], points[3][0]])


def task(temp_mf_json, heat_mf_json, rules_json, current_temp):
    """
    Основная функция для вычисления оптимального уровня нагрева
    :param temp_mf_json: данные для функции принадлежности температуры
    :param heat_mf_json: данные для функции принадлежности нагрева
    :param rules_json: список правил
    :param current_temp: текущая температура
    :return: оптимальный уровень нагрева
    """
    temp_mfs = json.loads(temp_mf_json)
    heat_mfs = json.loads(heat_mf_json)
    rules = json.loads(rules_json)

    # Получение минимальных и максимальных значений для температуры и нагрева
    min_temp, max_temp = float('inf'), float('-inf')
    min_heat, max_heat = float('inf'), float('-inf')

    for state in temp_mfs["температура"]:
        for point in state["points"]:
            min_temp = min(min_temp, point[0])
            max_temp = max(max_temp, point[0])

    for state in heat_mfs["уровень нагрева"]:
        for point in state["points"]:
            min_heat = min(min_heat, point[0])
            max_heat = max(max_heat, point[0])

    # Создаем объекты Antecedent и Consequent для fuzzy-системы
    temperature = ctrl.Antecedent(np.arange(min_temp, max_temp, 1), 'temperature')
    heating = ctrl.Consequent(np.arange(min_heat, max_heat, 0.1), 'heating')

    # Настроим функции принадлежности для температуры и нагрева
    parse_membership_functions(temp_mfs['температура'], temperature)
    parse_membership_functions(heat_mfs['уровень нагрева'], heating)

    # Активируем правила
    activated_rules = []
    for rule in rules:
        if rule[0] in temperature.terms and rule[1] in heating.terms:
            temp_level = fuzz.interp_membership(temperature.universe, temperature[rule[0]].mf, current_temp)
            if temp_level > 0:
                activated_rules.append((temp_level, rule[1]))

    # Вычисляем результат, объединяя активированные правила
    output_mf = np.zeros_like(heating.universe)
    for activation_level, heat_term in activated_rules:
        heat_mf = heating[heat_term].mf
        output_mf = np.maximum(output_mf, np.minimum(activation_level, heat_mf))

    if np.any(output_mf):
        return fuzz.defuzz(heating.universe, output_mf, 'centroid')
    else:
        raise ValueError("Выходная область пуста")


def load_json_from_source(source, default_value):
    """
    Функция для загрузки JSON данных
    :param source: источник данных (путь к файлу или строка JSON)
    :param default_value: значение по умолчанию в случае ошибки
    :return: загруженные данные
    """
    try:
        if os.path.isfile(source):
            with open(source, 'r') as file:
                return json.load(file)
        return json.loads(source)
    except Exception:
        return default_value


if __name__ == "__main__":
    # Стандартные значения для функции принадлежности и правил
    temperature_mf_default = {
        "температура": [
            {"id": "холодно", "points": [[0, 0], [5, 1], [10, 1], [12, 0]]},
            {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
            {"id": "жарко", "points": [[0, 0], [24, 0], [26, 1], [40, 1], [50, 0]]}
        ]
    }

    heating_mf_default = {
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [0, 1], [5, 1], [8, 0]]},
            {"id": "умеренный", "points": [[5, 0], [8, 1], [13, 1], [16, 0]]},
            {"id": "интенсивный", "points": [[13, 0], [18, 1], [23, 1], [26, 0]]}
        ]
    }

    rules_default = [
        ['холодно', 'интенсивный'],
        ['комфортно', 'умеренный'],
        ['жарко', 'слабый']
    ]

    current_temp_default = 15

    parser = argparse.ArgumentParser()
    parser.add_argument('--temp_file', type=str)
    parser.add_argument('--heat_file', type=str)
    parser.add_argument('--rules_file', type=str)
    parser.add_argument('--current_temp', type=int, default=current_temp_default)
    args = parser.parse_args()

    # Загрузка данных
    temp_mf_data = load_json_from_source(args.temp_file, json.dumps(temperature_mf_default))
    heat_mf_data = load_json_from_source(args.heat_file, json.dumps(heating_mf_default))
    rules_data = load_json_from_source(args.rules_file, json.dumps(rules_default))
    current_temp = args.current_temp

    try:
        optimal_heating = task(temp_mf_data, heat_mf_data, rules_data, current_temp)
        print(f"{optimal_heating:.2f}")
    except ValueError as e:
        print(f"Ошибка: {e}")
