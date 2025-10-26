import os
from  openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pptx import Presentation
import os
BOT_TOKEN = os.getenv("8146516889:AAFbvGE3_Hr2xh-j5IvZmaF9E9y-4jzMxlQ")
OPENAI_API_KEY = os.getenv("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")
client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga taqdimot mavzusini yuboring 🎓")

async def create_presentation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("⏳ Taqdimot tayyorlanmoqda...")

    prompt = f"{topic} mavzusi bo'yicha 5 slayddan iborat taqdimot yozing. Har slaydda sarlavha va 3-4 punkt bo'lsin."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    slides_text = response.choices[0].message.content

    prs = Presentation()
    for slide_text in slides_text.split("Slayd"):
        if slide_text.strip():
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            lines = slide_text.strip().split("\n")
            title = lines[0]
            content = "\n".join(lines[1:])
            slide.shapes.title.text = title
            slide.placeholders[1].text = content

    file_name = "presentation.pptx"
    prs.save(file_name)
    await update.message.reply_document(document=open(file_name, "rb"))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_presentation))

print("✅ Bot ishga tushdi...")
app.run_polling()
