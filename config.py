API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'
SESSION_NAME = 'support_bot_session'

# تنظیمات مربوط به مدل زبانی
MODEL_NAME = 'HooshvareLab/bert-fa-base-uncased'
MAX_LENGTH = 512
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# مسیر فایل‌های داده
CHAT_HISTORY_PATH = 'data/chat_history.json'
DEFAULT_RESPONSES_PATH = 'data/default_responses.json'
