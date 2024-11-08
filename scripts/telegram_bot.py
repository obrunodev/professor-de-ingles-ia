import logging, os, django, sys
from decouple import config
from openai import OpenAI
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

# Store bot screaming status
screaming = False

# Configure Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from englishbot.models import Student, Message, TeacherPrompt


# Initialize OpenAI client
client = OpenAI(api_key=config('OPENAI_API_KEY'))


def get_messages(student):
    return [
        {
            'role': c.role,
            'content': c.content,
        } for c in Message.objects.filter(student=student).order_by('-created_at')[:12]
    ][::-1]


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """

    # Print to console
    # print(f'{update.message.from_user.first_name} wrote {update.message.text}')
    prompts = ', '.join([prompt.content for prompt in TeacherPrompt.objects.all()])

    if screaming and update.message.text:
        context.bot.send_message(
            update.message.chat_id,
            update.message.text.upper(),
            entities=update.message.entities
        )
    else:
        """Echo the user message."""
        username = update.message.from_user.username
        student = Student.objects.filter(telegram_username=username).first()
        message = update.message.text
        
        Message.objects.create(
            student=student,
            role=Message.RoleChoices.USER,
            content=message
        )

        messages = get_messages(student)
                
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': f'Você é um professor de inglês, e estes tópicos definem como você deve se comportar { prompts }. Seu aluno(a) é { student.name }, do sexo { student.gender } e tem { student.age } anos de idade. Isso é tudo que sabe sobre ele(a) { student.about } """Nunca utilize a formatação MARKDOWN para construir sua resposta"""',
                },
                *messages,
                {
                    'role': 'user',
                    'content': update.message.text,
                },
            ],
        )
        
        response_text = response.choices[0].message.content
        update.message.reply_text(response_text)
        Message.objects.create(
            student=student,
            role=Message.RoleChoices.ASSISTANT,
            content=response_text,
        )


def scream(update: Update, context: CallbackContext) -> None:
    """
    This function handles the /scream command
    """

    global screaming
    screaming = True


def main() -> None:
    updater = Updater(config('TELEGRAM_BOT_TOKEN'))

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()