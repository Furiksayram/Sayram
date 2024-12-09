import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# API-ключ для работы с курсами валют
EXCHANGE_API_KEY = "30b66a3dd939fc68d67fe692"


# Функция для получения курса валют
def get_exchange_rate(base, target):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if target in data["conversion_rates"]:
            rate = data["conversion_rates"][target]
            return float(rate)
        else:
            return None
    else:
        return None


# Функция для обработки сообщений
async def handle_message(update: Update, context):
    text = update.message.text.lower()
    chat_id = update.effective_chat.id

    # Формируем ответ в зависимости от содержимого сообщения
    responses = []

    if "ассалому алейкум" in text or "assalomu aleykum" in text or "салом" in text or "Salom" in text or "салом" in text or "салом" in text:
        responses.append("Ва Алейкум Ассалом")
    if "яхшимисилар" in text or "хамма яхшими" in text:
        responses.append("яхши рахмат, узинглар кандайсилар")

    # Если сообщение содержит запрос на курсы валют
    if any(word in text for word in ["тенге", "сум", "доллар", "dollar", "$", "tanga", "tenge", "sum", "som"]):
        usd_to_kzt = get_exchange_rate("USD", "KZT")
        usd_to_uzs = get_exchange_rate("USD", "UZS")
        kzt_to_uzs = get_exchange_rate("KZT", "UZS")

        if usd_to_kzt is not None and usd_to_uzs is not None and kzt_to_uzs is not None:
            currency_reply = (
                "Актуальные курсы валют:\n"
                f"- 1 $ = {usd_to_kzt:.2f} тенге\n"
                f"- 1 $ = {usd_to_uzs:.2f} сум\n"
                f"- 1 тнг = {kzt_to_uzs:.2f} сум"
            )
        else:
            currency_reply = "Не удалось получить актуальные курсы валют. Пожалуйста, попробуйте позже."
        responses.append(currency_reply)

    # Если ответы сформированы, отправляем их, иначе отправляем сообщение по умолчанию
    if responses:
        await context.bot.send_message(chat_id=chat_id, text="\n".join(responses))



# Создание и настройка бота
app = ApplicationBuilder().token("6971667579:AAEXR0eM3hvniAxUjB_yXgyubiSA6DPuiBY").build()

# Добавляем обработчик сообщений
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()
