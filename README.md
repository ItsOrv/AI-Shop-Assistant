# Ai-Shop-Assistant

<p align="center">
  <a href="README.md">English</a> |
  <a href="README-fa.md">فارسی</a>
</p>

![Ai Shop Assistant](https://via.placeholder.com/800x400?text=Ai+Shop+Assistant)

Ai-Shop-Assistant is an AI-powered Telegram bot designed for automated customer support in online stores. It utilizes Telethon and the RAG (Retrieval-Augmented Generation) algorithm to provide intelligent and context-aware responses to customer inquiries.

## Features

- Automated response to user messages on Telegram
- Utilization of RAG algorithm for generating relevant and accurate responses
- Processing and leveraging previous chat history to improve response quality
- Support for Persian language using appropriate language models
- Capability to use default responses for frequently asked questions

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- A Telegram account and access to Telegram API

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/ItsOrv/Ai-Shop-Assistant.git
   cd Ai-Shop-Assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure `config.py`:
   - Obtain your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
   - Enter your Telegram account's phone number in `PHONE_NUMBER`.
   - Adjust other settings as needed.

4. Prepare the data:
   - Place the `raw_chat_export.json` file containing chat history in the project's root directory.
   - Run the data processing script:
     ```
     python data_processor.py
     ```

5. Run the bot:
   ```
   python main.py
   ```

## How to Contribute

Your contributions to this project are highly valued. Please follow these steps to contribute:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Create a Pull Request.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact Us

If you have any questions or suggestions, please feel free to reach out through [Issues](https://github.com/ItsOrv/Ai-Shop-Assistant/issues).
