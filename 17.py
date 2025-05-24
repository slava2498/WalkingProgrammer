class Engine:
    def __init__(self, engine_size, fuel_type):
        self.engine_size = engine_size
        self.fuel_type = fuel_type

    def check_1(self):
        print('Проверка топлива')

    def check_2(self):
        print('Проверка наличия двигателя')

    def check_3(self, value):
        print('Проверка 3')
        if value > 5:
            print('Успешно')

    def check_4(self):
        print('Проверка 4')

    def start(self):
        self.check_1()
        self.check_2()
        self.check_3()
        self.check_4()

        print(f'запуск двигателя {self.fuel_type}. Объем двигателя {self.engine_size}')

        return True


class Car:
    def __init__(self, brand, color, engine_size, fuel_type, speed=0):
        self.brand = brand
        self.color = color
        self.speed = speed

        self.engine = Engine(engine_size=engine_size, fuel_type=fuel_type)

    def display_info(self):
        print(f'Это {self.brand}, {self.color} цвет')

    def accelerate(self, increment):
        self.speed += increment
        print(f'{self.brand} ускоряется. Текущая скорость {self.speed} км/ч')

    def brake(self, decrement):
        self.speed -= decrement
        print(f'{self.brand} тормозит. Текущая скорость {self.speed} км/ч')

    def start_engine(self):
        self.engine.start()
        print(f'Запуск двигателя {self.brand}')


car_toyota = Car(brand='Toyota', color='Красный', engine_size=2000, fuel_type='Бензин')
car_bmw = Car(brand='Bmw', color='Черный', speed=60, engine_size=2000, fuel_type='Дизель')

car_toyota.display_info()
car_bmw.display_info()

car_toyota.start_engine()
car_bmw.start_engine()

car_toyota.accelerate(increment=60)
car_bmw.brake(decrement=30)

car_toyota.accelerate(increment=30)
car_bmw.accelerate(increment=60)