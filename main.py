from pyrogram import Client
from authorization import api_id, api_hash
from downloader import download_from_telegram
import uvloop

# Main execution
if __name__ == "__main__":
    uvloop.install()
    app = Client(
        "pyrogram_session",
        api_id=api_id,
        api_hash=api_hash,
    )

    link = input("Enter the Telegram message link (private format): ")
    app.run(download_from_telegram(app, link))
