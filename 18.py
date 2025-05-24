class Character:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def display_info(self):
        print(f'Имя: {self.name}, Здоровье {self.health}, Сила: {self.strength}')

    def attack(self, other):
        print(f'{self.name} атакует {other.name} и наносит {self.strength} урон!')
        other.health -= self.strength
        if other.health <= 0:
            print(f'{other.name} умер')
        else:
            print(f'{other.name} осталось {other.health} здоровья')


# hero = Character(name='Герой', health=100, strength=20)
# villain = Character(name='Злодей', health=80, strength=15)
#
# hero.display_info()
# villain.display_info()

# hero.attack(other=villain)
# villain.attack(other=hero)
# hero.attack(other=villain)
# hero.attack(other=villain)
# hero.attack(other=villain)


class Warrior(Character):
    def heavy_attack(self, other):
        print(f'{self.name} использует мощную атаку на {other.name}')
        other.health -= self.strength * 2
        if other.health <= 0:
            print(f'{other.name} умер')
        else:
            print(f'{other.name} осталось {other.health} здоровья')


class Mage(Character):
    def cast_spell(self, other):
        print(f'{self.name} колдует заклинание на {other.name}')
        other.health -= self.strength // 2
        print(f'{other.name} парализован и не может атаковать')


warrior = Warrior(name='Воин', health=120, strength=25)
mage = Mage(name='Маг', health=70, strength=30)

warrior.display_info()
mage.display_info()

warrior.attack(mage)
mage.attack(warrior)

mage.cast_spell(warrior)
warrior.heavy_attack(mage)