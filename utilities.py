from pyrogram import Client, errors, utils
from rich.text import Text
from rich.console import Console
import re 
from rich.progress import  ProgressColumn

console = Console()

# Monkey-patch Pyrogram's get_peer_type function
def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

utils.get_peer_type = get_peer_type_new


# Custom column for showing download progress in MB
class DownloadMBColumn(ProgressColumn):
    """Custom column for showing download progress in MB."""

    def render(self, task):
        completed_mb = task.completed / (1024 * 1024)
        total_mb = task.total / (1024 * 1024) if task.total else 0
        if task.total:
            return Text(f"{completed_mb:.2f} MB/{total_mb:.2f} MB")
        else:
            return Text(f"{completed_mb:.2f} MB/? MB")


def parse_message_link(link):
    """
    Extract chat ID and message ID from a Telegram message link.
    
    Args:
        link (str): The Telegram link to parse.
    
    Returns:
        tuple: (chat_id, message_id) if both are present, otherwise (chat_id, None).
    """
    match = re.match(r"https?://t\.me/c/(\d+)(?:/(\d+))?", link)
    if match:
        chat_id = int(f"-100{match.group(1)}")  # Convert to full chat ID with -100 prefix
        message_id = int(match.group(2)) if match.group(2) else None
        return chat_id, message_id
    else:
        console.print("[red]Invalid Telegram message link format.[/red]")
        return None, None
    
