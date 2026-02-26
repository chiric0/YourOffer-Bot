from config import bot, log
from bots_functions import (
    create_main_menu,
    cover_letter_start,
    resume_bot_start,
    ai_interviewer_start,
    parser_start,
    async_handler,
    user_summary,
    ask_questions_X,
    ask_questions_Y,
    ask_questions_Z,
    user_achievements,
    user_skills,
    return_to_main_menu,
    current_mode,
    restart_cover_letter,
    restart_resume_bot,
    restart_ai_interviewer,
    restart_parser
)
from bots_dicts import *


@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start. Отправляет приветственное сообщение и главное меню.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} started the bot")
    welcome_text = (
        "👋 Привет! Я главный бот YourOffer.\n\n"
        "Я помогу тебе с:\n"
        "📝 Написанием сопроводительного письма\n"
        "📄 Созданием резюме\n"
        "🤖 Подготовкой к собеседованию\n"
        "🔍 Поиском вакансий\n\n"
        "Выбери нужный режим работы:"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_main_menu()
    )


@bot.message_handler(func=lambda message: message.text == "📝 Сопроводительное письмо")
def cover_letter_mode(message):
    """Обработчик выбора режима создания сопроводительного письма.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} selected cover letter mode")
    cover_letter_start(message)


@bot.message_handler(func=lambda message: message.text == "📄 Резюме")
def resume_mode(message):
    """Обработчик выбора режима создания резюме.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} selected resume mode")
    resume_bot_start(message)


@bot.message_handler(func=lambda message: message.text == "🤖 AI Интервьюер")
def ai_interviewer_mode(message):
    """Обработчик выбора режима AI интервьюера.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} selected AI interviewer mode")
    ai_interviewer_start(message)


@bot.message_handler(func=lambda message: message.text == "🔍 Парсер вакансий")
def parser_mode(message):
    """Обработчик выбора режима парсера вакансий.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} selected parser mode")
    parser_start(message)


@bot.message_handler(func=lambda message: message.text == "🏠 Главное меню")
def main_menu_handler(message):
    """Обработчик возврата в главное меню.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    return_to_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "🔄 Рестарт")
def restart_handler(message):
    """Обработчик кнопки рестарта.
    
    Args:
        message (types.Message): Объект сообщения от пользователя
    """
    log.info(f"User {message.from_user.id} pressed restart button")
    
    # Определяем текущий режим из словаря
    current = current_mode.get(message.from_user.id)
    
    if current == "cover_letter":
        restart_cover_letter(message)
    elif current == "resume":
        restart_resume_bot(message)
    elif current == "interviewer":
        restart_ai_interviewer(message)
    elif current == "parser":
        restart_parser(message)
    else:
        # Если режим не определен, возвращаем в главное меню
        return_to_main_menu(message)


user_summary_async = async_handler(user_summary)
ask_questions_X_async = async_handler(ask_questions_X)
ask_questions_Y_async = async_handler(ask_questions_Y)
ask_questions_Z_async = async_handler(ask_questions_Z)
user_achievements_async = async_handler(user_achievements)
user_skills_async = async_handler(user_skills)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    callback_data_parts = callback.data.split("\n")
    user_response = callback_data_parts[0]
    chat_id = int(callback_data_parts[1])

    if user_response == 'да':
        bot.send_message(chat_id, "Расскажи о каком-нибудь своем проекте. Опиши его и расскажи, чем ты в нем занимался.")
        dialogue[chat_id] = "Вопрос №1: Расскажи о каком-нибудь своем проекте. Опиши его и расскажи, чем ты в нем занимался."
        answers_X[chat_id] = "Вопрос №1: Расскажи о каком-нибудь своем проекте. Опиши его и расскажи, чем ты в нем занимался."

        bot.register_next_step_handler(callback.message, ask_questions_X_async)
    elif user_response == 'нет':
        bot.send_message(chat_id, "Расскажи о каких-нибудь своих достижениях")
        bot.register_next_step_handler(callback.message, user_achievements_async)


if __name__ == "__main__":
    """
    Точка входа в программу. Запускает бота и обрабатывает исключения.
    """
    log.info("Starting main bot...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        log.error(f"Error in bot polling: {e}") 