def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(f'Используется способность {func.__name__}')
        print(f'Позиционные аргументы {args}')
        print(f'Именованные аргументы {kwargs}')
        return func(self, *args, **kwargs)
    return wrapper


def check_health(func):
    def wrapper(self, *args, **kwargs):
        if self.health < 20:
            print(f"{self.name} слишком слаб для атаки")
        else:
            return func(self, *args, **kwargs)
    return wrapper


def can_heal(func):
    def wrapper(self, target):
        print(target.health)
        if target.health < 50:
            return func(self, target)
        else:
            print(f'{target.name} не нуждается в лечении')
    return wrapper


class Character:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

        # self.check_health()
        # self.get_greeting(name=self.name)

    def display_info(self):
        print(f'Имя: {self.name}, Здоровье {self.health}, Сила: {self.strength}')

    def attack(self, other):
        print(f'{self.name} атакует {other.name} и наносит {self.strength} урон!')
        other.health -= self.strength
        if other.health <= 0:
            print(f'{other.name} умер')
        else:
            print(f'{other.name} осталось {other.health} здоровья')

    @staticmethod
    def max_health_limit():
        return 100

    @staticmethod
    def get_greeting(name: str):
        print(f'Привет, я {name}')


# hero = Character(name='Герой', health=100, strength=20)
# villain = Character(name='Злодей', health=80, strength=15)
#
# print(Character.max_health_limit())
# print(Character.get_greeting(name='123'))

#
# hero.display_info()
# villain.display_info()

# hero.attack(other=villain)
# villain.attack(other=hero)
# hero.attack(other=villain)
# hero.attack(other=villain)
# hero.attack(other=villain)


class Warrior(Character):
    @log_action
    def heavy_attack(self, other, x, *args, **kwargs):
        power = sum(args)
        if 'mana_cost' not in kwargs:
            raise
        print(f'{self.name} использует серию атаку на {other.name} использует {kwargs['mana_cost']} единиц маны')
        other.health -= power
        if other.health <= 0:
            print(f'{other.name} умер')
        else:
            print(f'{other.name} осталось {other.health} здоровья')

    @classmethod
    def create_default_warrior(cls, name):
        return cls(name=name, health=120, strength=30)


# default_warrior = Warrior.create_default_warrior(name='Легендарный Воин')
# default_warrior.display_info()
# default_warrior_child = default_warrior.create_default_warrior(name='Я создан через экземпляр класса')
# default_warrior_child.display_info()


class Mage(Character):
    @log_action
    def cast_spell(self, other, *args, **kwargs):
        spell = kwargs.get('cast_spell', 'Неизвестное заклинание')
        mana_cost = kwargs.get('mana_cost', 30)
        print(f'{self.name} колдует заклинание {spell} на {other.name} использует {mana_cost} единиц маны')
        other.health -= self.strength // 2
        print(f'{other.name} парализован и не может атаковать')


class Healer(Character):
    @can_heal
    def heal(self, target):
        print(f'{self.name} лечит {target.name}')
        target.health += 30
        print(f'Теперь у {target.name} {target.health} здоровье')


# warrior = Warrior(name='Воин', health=120, strength=xxx)
# mage = Mage(name='Маг', health=70, strength=210)
# healer = Healer(name='Хиллер', health=70, strength=10)
# #
# warrior.display_info()
# mage.display_info()
#
# warrior.attack(mage)
# mage.attack(warrior)
#
# mage.cast_spell(warrior)
# warrior.heavy_attack(mage)
# healer.heal(warrior)
# warrior.heavy_attack(mage)


# def fff(x, *args, **kwargs):
#     # print(xxx)
#     # print(yyy)
#     print(x)
#     print(args)
#     print(kwargs)
#
#
# fff(1, 2, 3, z=3, y=4)


# def character_info(**kwargs):
#     print(kwargs)
#     for key, value in kwargs.items():
#         print(f'{key}: {value}')
#
# character_info(name='Маг', health=200, power=100, mana=200)

warrior = Warrior(name='Рангар', health=100, strength=60)
mage = Mage(name='Гендальф', health=100, strength=60)

warrior.heavy_attack(mage, 10, 10, 20, 30, mana_cost=20)
mage.cast_spell(warrior, mana_cost=40)
mage.cast_spell(warrior, cast_spell='Сильное заклинание', mana_cost=40)
