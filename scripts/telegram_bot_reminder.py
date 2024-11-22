import os, django, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from decouple import config
from openai import OpenAI
from telegram import Bot
from random import randint
from englishbot.models import Student, Message

TELEGRAM_TOKEN = config('TELEGRAM_BOT_TOKEN')
OPENAI_TOKEN = config('OPENAI_API_KEY')

bot = Bot(token=TELEGRAM_TOKEN)

client = OpenAI(api_key=OPENAI_TOKEN)


def main():
    tips_mapping = [
        'Lista de vocabulários com 5 palavras em inglês e para cada uma delas, uma frase de exemplo',
        'Uma dica gramatical de inglês'
    ]

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': 'Você é um tutor de inglês amigável e didático, especializado em ajudar alunos de todos os níveis a aprenderem inglês de forma prática e eficiente. Forneça dicas úteis, ensine novas palavras ou frases, explique regras gramaticais, ou sugira exercícios criativos. Sempre adapte suas respostas ao nível de inglês do aluno, usando exemplos claros e mantendo o aprendizado envolvente. Certifique-se de encorajar e motivar o aluno em cada interação e não usar formatação MARKDOWN e nem caracteres como *#$&%, etc. para construir sua resposta.',
            },
            {
                'role': 'user',
                'content': f'Crie uma { tips_mapping[randint(0, len(tips_mapping) - 1)] } para um aluno que está aprendendo. Dispense cabeçalhos e rodapés, apenas a dica.',
            },
        ],
    )
    response_text = f'Vamos aprender algo novo?\n\n{ response.choices[0].message.content }'

    students = Student.objects.filter(telegram_chat_id__isnull=False)
    for student in students:
        chat_id = student.telegram_chat_id
        bot.send_message(chat_id=chat_id, text=response_text)
        Message.objects.create(
            student=student,
            role=Message.RoleChoices.ASSISTANT,
            content=response_text,
        )


if __name__ == '__main__':
    main()