import json
import re
import hazm

class DataProcessor:
    def __init__(self):
        self.normalizer = hazm.Normalizer()

    def clean_text(self, text):
        # حذف کاراکترهای خاص و نرمال‌سازی متن
        text = re.sub(r'[^\w\s]', '', text)
        text = self.normalizer.normalize(text)
        return text.strip()

    def process_chat_history(self, input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)

        processed_data = []
        for message in chat_data['messages']:
            if message['type'] == 'message':
                if 'reply_to_message_id' in message:
                    # این یک پاسخ است
                    question = next((m['text'] for m in chat_data['messages'] if m['id'] == message['reply_to_message_id']), None)
                    answer = message['text']
                    if question and answer:
                        processed_data.append({
                            'question': self.clean_text(question),
                            'answer': self.clean_text(answer)
                        })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)

    def create_default_responses(self, output_file):
        default_responses = {
            "سلام": "سلام! چطور می‌توانم به شما کمک کنم؟",
            "خداحافظ": "ممنون از تماس شما. روز خوبی داشته باشید!",
            "قیمت": "برای اطلاع از قیمت‌های به‌روز، لطفاً به وبسایت ما مراجعه کنید یا با پشتیبانی تماس بگیرید.",
            "ساعات کاری": "ساعات کاری ما از شنبه تا پنجشنبه، 9 صبح تا 6 عصر است.",
            "نحوه سفارش": "برای سفارش می‌توانید از طریق وبسایت ما اقدام کنید یا با شماره پشتیبانی تماس بگیرید."
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(default_responses, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    processor = DataProcessor()
    processor.process_chat_history('raw_chat_export.json', 'data/chat_history.json')
    processor.create_default_responses('data/default_responses.json')
