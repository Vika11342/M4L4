import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, DATABASE
from logic import DB_Manager

bot = telebot.TeleBot(TOKEN)
manager = DB_Manager(DATABASE)

@bot.message_handler(commands=['start'])
def start_command(message):
    predmets = manager.get_predmet()
    markup = InlineKeyboardMarkup()
    for p in predmets:
        predmet_name = p[0]
        btn = InlineKeyboardButton(text= predmet_name,callback_data=f"sub_{predmet_name}")
        markup.add(btn)

    bot.send_message(message.chat.id, "Выбери предмет для проекта:", reply_markup= markup)

@bot.callback_query_handler(func= lambda call: call.data.startswith('sub_'))
def handle_subject_click(call):
    subject_name = call.data.replace('sub_', '')
    subject_id = manager.get_predmet_id(subject_name)
    temas = manager.get_tema("SELECT tema FROM tema WHERE predmet_id = ?", (subject_id,))
    markup = InlineKeyboardMarkup()
    for t in temas:
        tema_name = t[0]
        btn = InlineKeyboardButton(text=tema_name, callback_data=f"top_{tema_name}")
        markup.add(btn)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Предмет: {subject_name}\nВыбери тему:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('top_'))
def handle_topic(call):
    topic_name = call.data.replace('top_', '')

    bot.send_message(
        chat_id=call.message.chat.id,
        text=f" Материалы по теме «{topic_name}» скоро появятся!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

    if __name__ == '__main__':
        bot.polling(none_stop=True)