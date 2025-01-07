# Telesave

**Telesave** is a Python-based utility designed to download videos (and other media) from Telegram chats using message links. With its seamless user experience and graphical progress bar, Telesave makes downloading Telegram media easy and visually appealing.

---

## Features

- Download videos and media files from Telegram chats using message links.
- Download all media from a channel using channel link.
- Secure and efficient integration with the **Pyrogram** library.
- User-friendly graphical progress bar displaying:
  - File size (downloaded/total)
  - Download speed
  - Estimated time remaining
- Secure two-step verification support for Telegram accounts.

---

## Prerequisites

Before using Telesave, ensure you have the following:

1. **Python 3.7 or higher** installed on your system.
2. Required Python libraries installed. You can install them by running:

   ```bash
   pip install pyrogram rich

## Installation and Usage
Follow these steps to set up and use Telesave:

### Step 1: Clone or Download the Repository

1.  Download or clone the repository from GitHub.
2.  Extract the contents to a folder named `telesave`.

### Step 2: Run the Program

1.  Open a terminal and navigate to the `telesave` folder.
    
2.  Run the program using the following command:

```bash
python main.py
```

### Step 3: Follow the On-Screen Instructions

#### Pyrogram Session Creation:

-   Enter your Telegram phone number or bot token.
-   Verify your account by entering the confirmation code sent to your Telegram app.
-   If two-step verification is enabled for your account, enter your password.

#### Provide the Message Link:

-   Enter the private message link for the Telegram chat in the following format:


## Example Output

Below is an example screenshot of the program in action:
![image](https://iili.io/2g1NEVp.jpg)

## Notes

-   Ensure your Telegram account or bot has access to the chat containing the message link.
-   The session is securely handled using the Pyrogram library.
-   Ensure you have sufficient storage space before starting the download.
-   Telesave supports downloading from private Telegram groups and channels if you have access permissions.
