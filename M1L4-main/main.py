import telebot
from config import token
from logic import Pokemon, Wizard, Fighter
import random

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.id not in Pokemon.pokemons.keys():
        # Выбор класса покемона случайным образом
        pokemon_type = random.choice([Pokemon, Wizard, Fighter])

        if pokemon_type == Pokemon:
            pokemon = Pokemon(message.from_user.id)
        elif pokemon_type == Wizard:
            pokemon = Wizard(message.from_user.id)
        else:
            pokemon = Fighter(message.from_user.id)

        Pokemon.pokemons[message.from_user.id] = pokemon # Сохраняем покемона
        bot.send_message(message.chat.id, pokemon.info())  # Отправляем информацию
        bot.send_photo(message.chat.id, pokemon.show_img())  # Отправляем фото
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'], func=lambda message: message.reply_to_message is not None)
def attack(message):
    attacker_username = message.from_user.username
    defender_username = message.reply_to_message.from_user.username

    attacker_id = None
    defender_id = None

    for user_id, pokemon in Pokemon.pokemons.items():
        if pokemon.pokemon_trainer == attacker_username:
            attacker_id = user_id
        if pokemon.pokemon_trainer == defender_username:
            defender_id = user_id

    if attacker_id is None or defender_id is None:
        bot.reply_to(message, "У одного из вас нет покемона или пользователя не существует.")
        return

    attacker = Pokemon.pokemons[attacker_id]
    defender = Pokemon.pokemons[defender_id]

    attack_result = attacker.attack(defender)
    bot.send_message(message.chat.id, attack_result)

    if defender.hp <= 0:
        bot.send_message(message.chat.id, f"@{attacker.pokemon_trainer} получает бонус за победу!")
        attacker.receive_victory_bonus()

    # Обновляем информацию
    bot.send_message(message.chat.id, attacker.info())
    bot.send_message(message.chat.id, defender.info())


@bot.message_handler(commands=['heal'])
def heal(message):
    user_id = message.from_user.id
    if user_id not in Pokemon.pokemons:
        bot.reply_to(message, "У тебя еще нет покемона!")
        return

    pokemon = Pokemon.pokemons[user_id]
    pokemon.heal()  # Восстанавливаем здоровье
    bot.send_message(message.chat.id, f"Покемон @{pokemon.pokemon_trainer} восстановил здоровье.")
    bot.send_message(message.chat.id, pokemon.info())
bot.infinity_polling(none_stop=True)
