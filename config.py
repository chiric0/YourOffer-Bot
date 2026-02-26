import logging
import os
from dotenv import load_dotenv, find_dotenv
import telebot
import redis

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Добавляем поддержку UTF-8 для эмодзи
)
log = logging.getLogger('config')

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Инициализация бота
bot = telebot.TeleBot(token=os.getenv('TOKEN'))
api_key = os.getenv('API_GPT')

# Инициализация Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0) 