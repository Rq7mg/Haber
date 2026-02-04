import os
import feedparser
import time
from telegram import Bot

# Heroku Config Vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Örn: "-1001234567890"

# Hazır RSS listesi (Türkiye güncel haber siteleri)
RSS_URLS = [
    "https://www.guncel-haber.com/rss/guncel",
    "https://www.guncel-haber.com/rss/siyaset",
    "https://www.guncel-haber.com/rss/dunya",
    "https://www.guncel-haber.com/rss/teknoloji",
    "https://www.ht-haber.com/rss/turkiye",
    "https://www.ht-haber.com/rss/spor",
    "https://www.gophaber.com/rss.xml"
]

bot = Bot(token=BOT_TOKEN)
posted = set()  # Daha önce gönderilen haberleri tutacak

def check_feeds():
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            link = entry.link
            if link not in posted:
                title = entry.title
                # Resim alma (RSS varsa)
                image = None
                if 'media_content' in entry:
                    image = entry.media_content[0]['url']

                # Mesaj oluştur
                caption = f"<b>{title}</b>\n{link}"

                try:
                    if image:
                        bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption=caption, parse_mode="HTML")
                    else:
                        bot.send_message(chat_id=CHANNEL_ID, text=caption, parse_mode="HTML")
                    print(f"Haber gönderildi: {title}")
                except Exception as e:
                    print("Gönderilemedi:", e)

                posted.add(link)

# Bot sürekli çalışacak
while True:
    check_feeds()
    time.sleep(60 * 5)  # 5 dakikada bir kontrol
