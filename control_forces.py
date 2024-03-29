#%%  _ROV scheme_
#%---------------------------
#%    ---                ---
#%   [ 1 ]    ( 2 )     [ 3 ]
#%    ---                ---
#%
#%    ---                ---
#%   [ 4 ]    ( 5 )     [ 6 ]
#%    ---                ---
#%----------------------------
# f1 = f6, f2 = f5, f3 = f4

import math

class MotorControl:
    def __init__(self, min_input, max_input):
        # Минимальный и максимальный углы поворота винта
        self.min_angle = 25
        self.max_angle = 127
        # Минимальное и максимальное значение входного диапазона
        self.min_input = min_input
        self.max_input = max_input

    # Преобразование входного значения в угол поворота винта
    def angle_from_input(self, input_value):
        # Преобразуем входное значение в диапазоне (min_input, max_input) в диапазон (min_angle, max_angle)
        scaled_input = self.min_angle + (self.max_angle - self.min_angle) * ((input_value - self.min_input) / (self.max_input - self.min_input))
        return scaled_input

    # Функции сил для каждого двигателя
    def f1(self, servo_angle):
        return [self.F(servo_angle) * math.sin(math.pi / 4),
                self.F(servo_angle) * math.cos(math.pi / 4),
                0]

    def f2(self, servo_angle):
        return [0, 0, -self.F(servo_angle)]

    def f3(self, servo_angle):
        return [self.F(servo_angle) * math.sin(math.pi / 4),
                -self.F(servo_angle) * math.cos(math.pi / 4),
                0]

    # Функция F для вычисления силы
    def F(self, servo_angle):
        # Ваша функция F, которая зависит от угла сервопривода
        # Здесь можно вставить вашу функцию F
        # Для примера, я просто возвращаю угол сервопривода
        return servo_angle

    # Метод для вычисления угла поворота винта для каждого двигателя на основе векторов сил
    def calculate_motor_controls(self, inputs):
        controls = []
        for input_value in inputs:
            # Преобразовываем входное значение в угол поворота винта
            angle = self.angle_from_input(input_value)

            # Ограничиваем угол в диапазоне от 25 до 127
            angle = max(self.min_angle, min(self.max_angle, angle))

            # Округляем угол до целого числа
            angle = round(angle)

            controls.append(angle)
        return controls

# Пример использования класса MotorControl
if __name__ == "__main__":
    # Задаем пользовательский входной диапазон
    min_input = 0
    max_input = 100

    # Пример входных значений (от min_input до max_input) для каждого двигателя
    inputs = [0, 100, 65, 75, 90]

    # Создаем экземпляр класса MotorControl с пользовательскими значениями диапазона
    motor_control = MotorControl(min_input, max_input)

    # Вычисляем углы поворота винта для каждого двигателя
    motor_controls = motor_control.calculate_motor_controls(inputs)

    # Выводим результаты
    print("Motor Controls:", motor_controls)
