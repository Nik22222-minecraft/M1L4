from random import randint
import requests
import random

class Pokemon:
    pokemons = {}  # Словарь для хранения покемонов по user_id

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.name = self.get_pokemon()
        self.hp = randint(50, 100)  # Случайное здоровье
        self.power = randint(10, 20) # Случайная сила

    def get_pokemon(self):
        number = randint(1, 150)
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        response = requests.get(url)
        pokemon = response.json()
        self.img = pokemon['sprites']['front_default']
        return pokemon['name']

    def show_img(self):
        return self.img

    def info(self):
        return (f"Твой покемон: {self.name}\n"
                f"Имя тренера: @{self.pokemon_trainer}\n"
                f"Здоровье: {self.hp}\n"
                f"Сила: {self.power}")

    def attack(self, enemy):
        if isinstance(enemy, Wizard): #Проверка является ли враг Wizard
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "
    
    def receive_victory_bonus(self):
        # Бонус при победе: немного восстанавливаем здоровье и увеличиваем силу
        heal_amount = randint(5, 10)
        power_boost = randint(1, 3)
        self.hp += heal_amount
        self.power += power_boost
        return f"Получен бонус! Восстановлено {heal_amount} здоровья и увеличена сила на {power_boost}!"
    
    def heal(self):
        self.hp = 100 #Восстанавливаем полностью здоровье

class Wizard(Pokemon):  # Наследуемся от Pokemon
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = randint(80, 120) # Больше здоровья
        self.power = randint(5, 15) # Меньше силы
    
    def info(self):
        return "У тебя покемон-волшебник\n" + super().info()

class Fighter(Pokemon):  # Наследуемся от Pokemon
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp = randint(40, 90) # Меньше здоровья
        self.power = randint(20, 30) # Больше силы

    def attack(self, enemy):
        super_sila = randint(5,15)
        self.power += super_sila
        result = super().attack(enemy)
        self.power -= super_sila
        return result + f"\nБоец применил супер-атаку силой:{super_sila} "

    def info(self):
        return "У тебя покемон-боец\n" + super().info()

