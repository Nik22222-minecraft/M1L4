from random import randint
import requests
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}  # Словарь для хранения покемонов по user_id

    def __init__(self, pokemon_trainer_id):
        self.pokemon_trainer_id = pokemon_trainer_id # Store User ID
        self.name = self.get_pokemon()
        self.hp = randint(50, 100)
        self.max_hp = self.hp  # Сохраняем максимальное здоровье
        self.power = randint(10, 20)
        self.last_feed_time = datetime.now()  # Время последнего кормления
        self.feed_interval = 24  # Интервал кормления (в часах)
        self.hp_increase = 20  # Количество здоровья, добавляемое при кормлении
        self.last_attack_time = None
        self.attack_cooldown = 10  # Seconds between attacks
        self.bonus = 0  # Бонусные очки за победы

    def get_pokemon(self):
        number = randint(1, 150)
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Вызывает исключение для плохих ответов (4xx или 5xx)
            pokemon = response.json()
            self.img = pokemon['sprites']['front_default']
            return pokemon['name']
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных покемона: {e}")
            return "ErrorPokemon"

    def show_img(self):
        return self.img

    def info(self):
        return (f"Твой покемон: {self.name}\n"
                f"ID тренера: {self.pokemon_trainer_id}\n"  # Используем ID
                f"Здоровье: {self.hp}/{self.max_hp}\n"
                f"Сила: {self.power}\n"
                f"Бонус: {self.bonus}")

    def attack(self, target):
        now = datetime.now()
        if self.last_attack_time is not None and (now - self.last_attack_time).total_seconds() < self.attack_cooldown:
            remaining_cooldown = self.attack_cooldown - (now - self.last_attack_time).total_seconds()
            return f"@{self.pokemon_trainer_id} can't attack yet. Cooldown: {remaining_cooldown:.1f} seconds."

        damage = randint(self.power // 2, self.power)
        target.hp -= damage
        self.last_attack_time = now

        if target.hp < 0:
            target.hp = 0  # Don't let HP go negative

        return f"@{self.pokemon_trainer_id}'s {self.name} attacks @{target.pokemon_trainer_id}'s {target.name} for {damage} damage!"


    def receive_victory_bonus(self):
        self.bonus += 1
        self.power += 2  # Небольшое увеличение силы
        self.hp = min(self.hp + 10, self.max_hp)  # Восстанавливаем немного здоровья, но не выше максимума

    def heal(self):
        self.hp = self.max_hp  # Восстанавливаем здоровье до максимума

    def feed(self):
        """
        Кормит покемона, увеличивая его здоровье, но только если прошло достаточно времени с последнего кормления.

        Возвращает:
            str: Сообщение о результате кормления.
        """
        now = datetime.now()
        time_since_last_feed = now - self.last_feed_time

        if time_since_last_feed >= timedelta(hours=self.feed_interval):
            self.hp = min(self.hp + self.hp_increase, self.max_hp)  # Увеличиваем здоровье, но не выше максимума
            self.last_feed_time = now
            return f"Покемон @{self.pokemon_trainer_id} покормлен. Здоровье увеличено. Текущее здоровье: {self.hp}/{self.max_hp}"
        else:
            next_feed_time = self.last_feed_time + timedelta(hours=self.feed_interval)
            time_to_wait = next_feed_time - now
            hours, remainder = divmod(time_to_wait.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return (f"Покемон @{self.pokemon_trainer_id} еще не голоден. Следующее кормление "
                    f"возможно через {int(hours)} ч {int(minutes)} мин {int(seconds)} сек.")

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer_id):
        super().__init__(pokemon_trainer_id)
        self.name = "Wizard_" + self.get_pokemon()
        self.power += 5
        self.hp += 10

class Fighter(Pokemon):
    def __init__(self, pokemon_trainer_id):
        super().__init__(pokemon_trainer_id)
        self.name = "Fighter_" + self.get_pokemon()
        self.power += 10
        self.hp -= 5
