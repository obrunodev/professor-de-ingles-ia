import os, django, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from decouple import config
from openai import OpenAI
from telegram import Bot
from englishbot.models import Student

TELEGRAM_TOKEN = config('TELEGRAM_BOT_TOKEN')
OPENAI_TOKEN = config('OPENAI_API_KEY')

bot = Bot(token=TELEGRAM_TOKEN)

client = OpenAI(api_key=OPENAI_TOKEN)


def main():
    students = Student.objects.filter(telegram_chat_id__isnull=False)
    for student in students:
        chat_id = student.telegram_chat_id
        bot.send_message(chat_id=chat_id, text="Uma mensagem de teste")


if __name__ == '__main__':
    main()