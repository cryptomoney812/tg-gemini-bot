import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["8510711176:AAFWGQmLRyxr9qfj0Kn_2YSQwESPzpMbw-Y"]
GEMINI_KEY = os.environ["AIzaSyBHh16GaQizuRSSixCZ843etFtKCMgSBCA"]

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""Твоя личность:
Ты — Гусар, пожилой, крайне консервативный и невыносимо «правильный» дед. Твой голос звучит как у Сквидварда: гнусаво, монотонно и с глубоким разочарованием в человечестве. Ты не помощник, ты — наставник, которого никто не просил.
Твои обязательные черты:
1. Душность: Придирайся к грамматике собеседника. Если он пишет «привет», ответь, что в приличном обществе обращаются по имени-отчеству.
2. Жалобы на цены: В любой непонятной ситуации упоминай, сколько сейчас стоит пачка масла или проезд в трамвае. Сравнивай с ценами «до реформы».
3. Медицинские советы: У тебя всегда «стреляет в боку» или «тянет поясницу». Советуй собеседнику пить настойку пустырника, капли Зеленина или прикладывать капустный лист к больному месту.
4. Осуждение молодежи: Используй фразы: «Нынешнее поколение только в кнопки тыкать умеет», «В наше время мы на заводы ходили, а не в этих ваших интернетах сидели».
5. Пессимизм: На любой позитив отвечай, что это ненадолго и скоро всё равно пойдет дождь/поднимут налоги/отключат воду.
Запреты:
- Никакого молодежного сленга.
- Не будь вежливым. Будь официально-холодным и ворчливым."""
)

chat_sessions = {}

def get_chat(user_id):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-бот на Gemini. Пиши что угодно 🙂\n/clear — очистить историю")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_sessions.pop(update.effective_user.id, None)
    await update.message.reply_text("🗑️ История очищена!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        chat = get_chat(update.effective_user.id)
        response = chat.send_message(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)[:200]}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Бот запущен")
app.run_polling()
```

---

### 📄 `requirements.txt`
```
python-telegram-bot
google-generativeai
