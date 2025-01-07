from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn, TransferSpeedColumn
from pyrogram import Client, errors
from rich.console import Console
import os
from utilities import parse_message_link, DownloadMBColumn


console = Console()

async def download_from_telegram(app: Client, link):
    """
    Download media from a Telegram message or all media from a channel.

    Args:
        app (Client): Pyrogram Client instance.
        link (str): Telegram message link.
    """
    chat_or_username, message_id = parse_message_link(link)
    print(chat_or_username)
    print(message_id)
    if not chat_or_username:
        console.print("[red]Invalid link provided. Please check the link and try again.[/red]")
        return

    console.print("[cyan]Connecting to Telegram...[/cyan]")
    await app.start()
    
    try:
        # Check if the chat is accessible
        try:
            chat = await app.get_chat(chat_or_username)
            console.print(f"[green]Successfully resolved chat: {chat.title}[/green]")
            download_dir = os.path.join(os.getcwd(), chat.title)
            os.makedirs(download_dir, exist_ok=True)
        except errors.RPCError as e:
            console.print(f"[red]Failed to resolve chat: {str(e)}[/red]")
            return

        # If a specific message ID is provided, download that file
        if message_id:
            console.print(f"[cyan]Downloading media from message ID: {message_id}[/cyan]")
            await _download_message_media(app, chat_or_username, message_id, download_dir)
        else:
            # Otherwise, download all media from the channel
            console.print(f"[cyan]Downloading all media from channel: {chat.title}[/cyan]")
            async for message in app.get_chat_history(chat_or_username):
                print(message)
                await _download_message_media(app, chat_or_username, message.id, download_dir)

        console.print("[green]Download completed successfully![/green]")

    except errors.RPCError as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")


async def _download_message_media(app: Client, chat_or_username, message_id, download_dir):
    """
    Helper function to download media from a specific message.

    Args:
        app (Client): Pyrogram Client instance.
        chat_or_username (str): Chat username or ID.
        message_id (int): ID of the message containing media.
        download_dir (str): Directory to save the downloaded file.
    """
    try:
        # Fetch the message
        message = await app.get_messages(chat_or_username, message_ids=message_id)
        
        # Check for media in the message
        media = None
        file_name = None
        if message.document:
            media = message.document
            file_name = f"{message_id}_{message.document.file_name}"
        elif message.video:
            media = message.video
            file_name = f"{message_id}_{message.video.file_name}"
        elif message.photo:
            media = message.photo
            file_name = f"{message_id}_photo.jpg"  # Photos don't have file names
        elif message.audio:
            media = message.audio
            file_name = f"{message_id}_{message.audio.file_name}"
        else:
            console.print(f"[yellow]No downloadable media found in message ID: {message_id}[/yellow]")
            return

        # Construct file path
        file_path = os.path.join(download_dir, file_name or f"unknown_file_{message_id}")

        # Get the size of already downloaded data (for resuming)
        downloaded_size = 0
        if os.path.exists(file_path):
            downloaded_size = os.path.getsize(file_path)

        # Check if the file is already downloaded
        total_size = media.file_size
        if downloaded_size >= total_size:
            console.print(f"[green]File already fully downloaded: {file_path}[/green]")
            return
        elif downloaded_size > 0:
            console.print(f"[green]Resuming download of {file_name} from {downloaded_size} bytes[/green]")

        # Progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadMBColumn(),  # Custom column to show progress in MB
            TransferSpeedColumn(),  # Shows download speed
            TimeRemainingColumn(),  # Shows estimated time remaining
            console=console
        ) as progress:
            task = progress.add_task(
                f"Downloading {file_name}",
                total=total_size,
                completed=downloaded_size,
            )

            # Define buffer size
            buffer_size = 5 * 1024 * 1024  # 5 MB buffer
            buffer = bytearray()

            # Stream and save the media chunk by chunk
            async for chunk in app.stream_media(media, offset=downloaded_size // (1024 * 1024)):
                buffer.extend(chunk)

                # Write to file when buffer exceeds buffer_size or when done
                if len(buffer) >= buffer_size:
                    with open(file_path, "ab") as f:  # Append mode
                        f.write(buffer)
                    buffer.clear()  # Clear the buffer

                # Update progress bar
                downloaded_size += len(chunk)
                progress.update(task, completed=downloaded_size)

            # Write remaining buffer to file
            if buffer:
                with open(file_path, "ab") as f:
                    f.write(buffer)

        console.print(f"[green]Downloaded: {file_path}[/green]")

    except errors.RPCError as e:
        console.print(f"[red]Error downloading message ID {message_id}: {str(e)}[/red]")

