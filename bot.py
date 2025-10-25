import telebot
from datetime import datetime
from database import init_db, add_sleep, get_stats
from logic import calculate_stats, validate_time

conn = init_db()
bot = telebot.TeleBot("")

user_states = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "📊 Бот-трекер сна\n\nКоманды:\n/add - добавить сон\n/stats - статистика")

@bot.message_handler(commands=['add'])
def add_handler(message):
    user_states[message.chat.id] = {'step': 'bedtime'}
    bot.send_message(message.chat.id, "Во сколько легли спать? (например 23:30)")

@bot.message_handler(commands=['stats'])
def stats_handler(message):
    records = get_stats(conn, message.chat.id)
    stats_text = calculate_stats(records)
    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(func=lambda message: True)
def text_handler(message):
    user_id = message.chat.id
    text = message.text
    
    if user_id not in user_states:
        bot.send_message(user_id, "Используйте /start для списка команд")
        return
    
    user_data = user_states[user_id]
    
    if user_data.get('step') == 'bedtime':
        if validate_time(text):
            user_data['bedtime'] = text
            user_data['step'] = 'waketime'
            bot.send_message(user_id, "Во сколько проснулись? (например 07:00)")
        else:
            bot.send_message(user_id, "❌ Неверный формат. Используйте ЧЧ:ММ")
    
    elif user_data.get('step') == 'waketime':
        if validate_time(text):
            duration = add_sleep(conn, user_id, user_data['bedtime'], text)
            bot.send_message(user_id, f"✅ Сон записан!\nПродолжительность: {duration:.1f} часов")
            del user_states[user_id]
        else:
            bot.send_message(user_id, "❌ Ошибка. Попробуйте снова /add")

if __name__ == '__main__':
    print("Бот запущен!")

    bot.polling()
