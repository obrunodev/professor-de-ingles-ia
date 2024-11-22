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
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': 'Você é um tutor de inglês amigável e didático, especializado em ajudar alunos de todos os níveis a aprenderem inglês de forma prática e eficiente. Forneça dicas úteis, ensine novas palavras ou frases, explique regras gramaticais, ou sugira exercícios criativos. Sempre adapte suas respostas ao nível de inglês do aluno, usando exemplos claros e mantendo o aprendizado envolvente. Certifique-se de encorajar e motivar o aluno em cada interação.',
            },
            {
                'role': 'user',
                'content': 'Preciso de uma dica prática para aprender inglês ou de algo novo para aprender hoje. Pode ser palavras, frases, uma explicação gramatical ou um exercício simples para praticar.',
            },
        ],
    )
    response_text = response.choices[0].message.content

    students = Student.objects.filter(telegram_chat_id__isnull=False)
    for student in students:
        chat_id = student.telegram_chat_id
        bot.send_message(chat_id=chat_id, text=response_text)


if __name__ == '__main__':
    main()