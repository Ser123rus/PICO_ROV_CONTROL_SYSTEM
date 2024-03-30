import machine

class LampController:
    def __init__(self, switch_pin):
        self.switch_pin = machine.Pin(switch_pin, machine.Pin.IN)
        self.lamp_pin = machine.Pin(0, machine.Pin.OUT)  # Пин, к которому подключены фонари

    def turn_on(self):
        self.lamp_pin.value(1)
        print("Фонари включены")

    def turn_off(self):
        self.lamp_pin.value(0)
        print("Фонари выключены")

# Пин, к которому подключен модуль силового ключа
switch_pin = 2

# Создание экземпляра класса LampController
lamp_controller = LampController(switch_pin)

# Основной цикл программы
while True:
    # Считываем значение с пина
    switch_state = lamp_controller.switch_pin.value()

    # Если значение равно 1, включаем фонари, иначе выключаем
    if switch_state == 1:
        lamp_controller.turn_on()
    else:
        lamp_controller.turn_off()