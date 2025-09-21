import telebot
from config import token
from logic import Pokemon, Wizard, Fighter
import random

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['go'])
def go(message):
    user_id = message.from_user.id
    if user_id not in Pokemon.pokemons:
        # Выбор класса покемона случайным образом
        pokemon_type = random.choice([Pokemon, Wizard, Fighter])

        if pokemon_type == Pokemon:
            pokemon = Pokemon(user_id)  # Передаем user_id
        elif pokemon_type == Wizard:
            pokemon = Wizard(user_id)  # Передаем user_id
        else:
            pokemon = Fighter(user_id)  # Передаем user_id

        Pokemon.pokemons[user_id] = pokemon
        print(f"Pokemon created for user ID: {user_id}") # Added print
        bot.send_message(message.chat.id, pokemon.info())
        try:
            bot.send_photo(message.chat.id, pokemon.show_img())
        except Exception as e:
            print(f"Error sending photo: {e}")
            bot.send_message(message.chat.id, "Could not display image.")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['attack'], func=lambda message: message.reply_to_message is not None)
def attack(message):
    attacker_id = message.from_user.id
    defender_id = message.reply_to_message.from_user.id

    if attacker_id == defender_id:
        bot.reply_to(message, "Нельзя атаковать самого себя!")
        return

    if attacker_id not in Pokemon.pokemons or defender_id not in Pokemon.pokemons:
        bot.reply_to(message, "У одного из вас нет покемона или пользователя не существует.")
        return

    attacker = Pokemon.pokemons[attacker_id]
    defender = Pokemon.pokemons[defender_id]

    attack_result = attacker.attack(defender)  # Атака с использованием ID
    bot.send_message(message.chat.id, attack_result)

    if defender.hp <= 0:
        bot.send_message(message.chat.id, f"@{message.from_user.username} получает бонус за победу!")  # Используйте username здесь, если хотите
        attacker.receive_victory_bonus()

    # Обновляем информацию
    bot.send_message(message.chat.id, attacker.info())
    bot.send_message(message.chat.id, defender.info())


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id
    if user_id in Pokemon.pokemons:
        pok = Pokemon.pokemons[user_id]
        bot.send_message(message.chat.id, pok.info())
        try:
            bot.send_photo(message.chat.id, pok.show_img())
        except Exception as e:
            print(f"Error sending photo: {e}")
            bot.send_message(message.chat.id, "Could not display image.")
    else:
        bot.reply_to(message, "У тебя еще нет покемона. Создай его с помощью команды /go")


@bot.message_handler(commands=['heal'])
def heal(message):
    user_id = message.from_user.id
    if user_id not in Pokemon.pokemons:
        bot.reply_to(message, "У тебя еще нет покемона!")
        return

    pokemon = Pokemon.pokemons[user_id]
    pokemon.heal()
    bot.send_message(message.chat.id, f"Покемон  восстановил здоровье.")
    bot.send_message(message.chat.id, pokemon.info())


@bot.message_handler(commands=['feed'])
def feed(message):
    user_id = message.from_user.id
    if user_id not in Pokemon.pokemons:
        bot.reply_to(message, "У тебя еще нет покемона!")
        return

    pokemon = Pokemon.pokemons[user_id]
    feed_result = pokemon.feed()
    bot.send_message(message.chat.id, feed_result)
    bot.send_message(message.chat.id, pokemon.info())


print("Бот запущен...")
bot.infinity_polling(none_stop=True)
