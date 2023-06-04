from telebot import *
import sqlite3

token = '5933053131:AAF9H99p8W9LSndk8o1GIkwYOQ7GKnwAmIo'

bot = telebot.TeleBot(token)

user_states = {}

"""conn = sqlite3.connect('Answers.db')
cursor = conn.cursor()"""   # Если будет большой поток


@bot.message_handler(commands=['start'])
def start_message(message):
    user_states[message.chat.id] = 0
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Да", callback_data="1")
    btn2 = types.InlineKeyboardButton("Нет", callback_data="2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Для того чтобы начать работу, скажи, можно ли передать ваш username найденному человеку?".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("/start")
    markup.add(btn)
    bot.send_message(message.chat.id,
                     text="За помощью обратитесь к @nastyaaa_sla".format(
                         message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "1":
        if call.message.from_user.username == None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("/start")
            markup.add(btn)
            bot.send_message(call.message.chat.id,
                             text="Извините, но для того, чтобы продолжить, вам нужно задать username для вашего аккаунта в Telegram".format(
                                 call.message.from_user), reply_markup=markup)
        else:
            user_states[call.message.chat.id] = 1
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Окей, давай начнём!")
            btn2 = types.KeyboardButton("Хорошо, я приду, как потребуется помощь")
            markup.add(btn1, btn2)
            bot.send_message(call.message.chat.id,
                             text="Привет! Ищешь единомышленников для создания стартапа? Хочешь найти команду под проект? Мечтаешь познакомиться с профи, работающими в твоей сфере? Ты на правильном пути! Скорее регистрируйся, я помогу найти нужных людей.".format(
                                 call.message.from_user), reply_markup=markup)
    elif call.data == "2":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("/start")
        btn2 = types.KeyboardButton("/help")
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id,
                         text="Простите, но тогда вы не сможете воспользоваться ботом. Начните сначала, если хотите продолжить.".format(
                             call.message.from_user), reply_markup=markup)
    else:
        user_info = bot.get_chat(call.data)
        bot.send_message(call.message.chat.id, f'@{user_info.username}')


@bot.message_handler(func=lambda message: message.text == "Хорошо, я приду, как потребуется помощь"
                                          and user_states[message.chat.id] == 1)
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Окей, давай начнём!")
    markup.add(btn)
    bot.send_message(message.chat.id,
                     text="Для продолжения нажми кнопку".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Окей, давай начнём!"
                                          and user_states[message.chat.id] == 1)
def func(message):

    del user_states[message.chat.id]
    remove_markup = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, "Итак, как тебя зовут?", reply_markup=remove_markup)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    name = message.text
    msg = bot.send_message(message.chat.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(msg, process_age_step, name)


def process_age_step(message, name):
    age = message.text
    msg = bot.send_message(message.chat.id, 'Из какого ты города?')
    bot.register_next_step_handler(msg, process_city_step, name, age)


def process_city_step(message, name, age):
    city = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("iOS разработчик")
    btn2 = types.KeyboardButton("Android разработчик")
    btn3 = types.KeyboardButton("Web разработчик")
    btn4 = types.KeyboardButton("Python разработчик")
    btn5 = types.KeyboardButton("Никто")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    msg = bot.send_message(message.chat.id,
                           'Кто тебе интересен? Кого ты ищешь?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_partner_step, name, age, city)


def process_partner_step(message, name, age, city):
    partner_prof = message.text

    remove_markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id,
                           'Расскажи о себе, своём проекте, кого хочешь найти и чем планируешь заняться', reply_markup=remove_markup)
    bot.register_next_step_handler(msg, process_about_step, name, age, city, partner_prof)


def process_about_step(message, name, age, city, partner_prof):
    about = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("iOS разработчик")
    btn2 = types.KeyboardButton("Android разработчик")
    btn3 = types.KeyboardButton("Web разработчик")
    btn4 = types.KeyboardButton("Python разработчик")
    btn5 = types.KeyboardButton("Никто")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    msg = bot.send_message(message.chat.id,
                           'Кем из предложенных специалистов являешся ты сам?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_profession_step, name, age, city, partner_prof, about)


def process_profession_step(message, name, age, city, partner_prof, about):
    profession = message.text

    bot.send_message(message.chat.id, "<b>Ваша анкета</b>", parse_mode="HTML")
    bot.send_message(message.chat.id, f'<u>Имя</u>: {name} \n <u>Возраст</u>: {age} \n <u>Место проживания</u>: {city} \n <u>Ваша профессия</u>: {profession} \n <u>О себе</u>: {about}', parse_mode="HTML")

    conn = sqlite3.connect('Answers.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO Answers (ID, Name, Age, City, About, Profession, State) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (message.chat.id, name, age, city, about, profession, 0))
        conn.commit()
    except:
        c.execute('''
                       UPDATE Answers
                       SET Name = ?, Age = ?, City = ?, About = ?, Profession = ?, State = 0
                       WHERE ID = ?
                   ''', (name, age, city, about, profession, message.chat.id))

    conn.commit()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать поиск")
    btn2 = types.KeyboardButton("Пока не ищу партнера")
    markup.add(btn1, btn2)

    msg = bot.send_message(message.chat.id, "Большое спасибо за ответы. Теперь вы можете найти партнера.", reply_markup=markup)
    bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number = 0)


def find_partner(message, partner_prof, partner_number):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать поиск")
    btn2 = types.KeyboardButton("Пока не ищу партнера")
    markup.add(btn1, btn2)

    conn = sqlite3.connect('Answers.db')
    c = conn.cursor()

    if message.text == "Начать поиск":
        c.execute("SELECT * FROM Answers WHERE Profession = ? AND ID != ? AND State == 0",
                  (partner_prof, message.chat.id))
        if c is None:
            msg = bot.send_message(message.chat.id, 'Извините, напарник не найден. Просим набраться терпения.')
            bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number)
        else:
            try:
                partner = c.fetchone()
                for i in range(partner_number):
                    partner = c.fetchone()

                markup_later = types.InlineKeyboardMarkup()
                btn_later = types.InlineKeyboardButton("USERNAME", callback_data=partner[0])
                markup_later.add(btn_later)

                msg = bot.send_message(message.chat.id, f'Имя: {partner[1]} \n Возраст: {partner[2]} \n Место проживания: {partner[3]} \n О себе: {partner[4]}', reply_markup=markup_later)

                bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number=partner_number+1)
            except TypeError:
                msg = bot.send_message(message.chat.id, 'Извините, напарник не найден. Просим набраться терпения. Или попробуйте еще раз.')
                bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number)
    elif message.text == "Пока не ищу партнера":
        c.execute('''
                        UPDATE Answers
                        SET State = 1
                        WHERE ID = ?
                    ''', (message.chat.id,))
        conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Стать видимым")
        markup.add(btn)
        msg = bot.send_message(message.chat.id, "Вы не будете видны другим пользователям",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number)
    elif message.text == "Стать видимым":
        c.execute('''
                        UPDATE Answers
                        SET State = 0
                        WHERE ID = ?
                    ''', (message.chat.id,))
        conn.commit()

        msg = bot.send_message(message.chat.id, "Поиск снова включен", reply_markup=markup)
        bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number)

    conn.close()


def start_find(message, partner_prof, partner_number):
    conn = sqlite3.connect('Answers.db')
    c = conn.cursor()

    c.execute('''
                    UPDATE Answers
                    SET State = 0
                    WHERE ID = ?
                ''', (message.chat.id,))
    conn.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Стать видимым")
    markup.add(btn)
    msg = bot.send_message(message.chat.id, "Вы не будете видны другим пользователям",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, find_partner, partner_prof, partner_number)


bot.infinity_polling()