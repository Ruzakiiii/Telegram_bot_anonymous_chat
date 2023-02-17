import telebot
from telebot import types
from database import Database

TOKEN = ""
admin_id = 583411442
db = Database('db.db')
bot = telebot.TeleBot(TOKEN)


def admin():
	pass


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск собеседника')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Отправить свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Остановить поиск')
    markup.add(item1)
    return markup


@bot.message_handler(commands = ['admin'])
def start(message):
    o = db.get_users(message.from_user.id)

    bot.send_message(message.chat.id, 'Всего {} пользователей\n\n{}'.format(len(o), o))



@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Я Парень 👨')
    item2 = types.KeyboardButton('Я Девушка 👩‍🦱')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Укажите ваш пол! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск собеседника')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Меню'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Следующий диалог')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Собеседник покинул чат', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Вы вышли из чата', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌ Вы не начали чат!', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Поиск собеседника' or message.text == '✏️ Следующий диалог':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
            item1 = types.KeyboardButton('🔎 Парень')
            item2 = types.KeyboardButton('🔎 Девушка')
            item3 = types.KeyboardButton('👩‍👨 Рандом')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Кого ищем?', reply_markup = markup)

            
        elif message.text == '❌ Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен', reply_markup = main_menu())

        
        elif message.text == '🔎 Парень':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Девушка':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Рандом':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Отправить свой профиль':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Вы сказали свой профиль')
                else:
                    bot.send_message(message.chat.id, '❌ В вашем аккаунте не указан username')
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

        

        elif message.text == 'Я Парень 👨':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш пол. Обратитесь в поддержку @yungcoder1')
        
        elif message.text == 'Я Девушка 👩‍🦱':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Вы уже указали ваш пол. Обратитесь в поддержку @yungcoder1')
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')


@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')



bot.polling(none_stop = True)