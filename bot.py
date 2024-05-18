from typing import Final
from telegram import Update
import json
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token: Final = '6677684168:AAEJjHYFm6Ef0XxSjMgPlAmWFJkbsAtWf3E'
name: Final = '@languesser_bot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! This bot can define languages of your input texts. Put some text in here.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Start with the /start command. The list of supported languages: English, German, French, Swedish, Finnish, '
        'Norwegian, Dannish, Icelandic, Faroese, Dutch, Italian, Spanish, Portugese, Romanian, Hungarian, Latvian, '
        'Lithuanian, Czech, Slovak, Serbian, (Cyrillic), Serbian, (Latin), Polish, Estonian, Bulgarian, Slovenian, '
        'Croatian, Macedonian, Russian, Ukrainian, Belarusian, Ingush, Chechen, Georgian, Greek, Cherokee, Hindi, '
        'Tatar, Ossetian, Hebrew, Persian, Lezgian, Udmurt, Moksha, Chukchi, Chinese, (simplified), Japanese, Korean, '
        'Turkish, Kazarh(Cyrillic), Kazarh(Latin), Buryat, Yiddish, Afrikaans, Karelian, Bengali, Telugu, '
        'Azerbaijani, Indonesian, Vietnamese, Catalan, Sardinian, Tajik, Uzbek, Kyrgyz, Malay, Thai, Burmese, Khmer, '
        'Amharic, Tamil')


def handle_response(text: str) -> str:

    words = text.lower().split()

    intermediate = [list(elem) for elem in words]

    letters = [elem for sub in intermediate for elem in sub]

    alphabet = set(letters)

    final = sorted(alphabet)

    final = [elem for elem in final if elem.isalpha() == True]

    with open("alphabeths.json", "r", encoding="utf-8") as output:
        alphabet = json.load(output)

    freq = {language: len(set(let).intersection(set(final))) for language, let in alphabet.items()}

    maximum = max(freq.values())

    getting = [i for i in freq if freq[i] == maximum]

    if len(getting) == 1:
        return getting
    else:
        with open("Top.json", "r", encoding="utf-8") as frequent:
            dic_freq = json.load(frequent)

        extracting = {key: val for key, val in dic_freq.items() if key in getting}
        count = {key: 0 for key in extracting}
        for elem in words:
            for k, v in extracting.items():
                if elem in v:
                    count[k] += 1
                else:
                    pass
        if count:
            maximum = max(count.values())
            language = [key for key, value in count.items() if value == maximum]
            if len(language) == 1:
                print(*language)
            else:
                return f'{language}'
        else:
            return 'No matching frequent words found in the specified languages.'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if name in text:
            new_text: str = text.replace(name, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


if __name__ == '__main__':
    print("1 test")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_error_handler(error)
    print("2 test")
    app.run_polling(poll_interval=1)
