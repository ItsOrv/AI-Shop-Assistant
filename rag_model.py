from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import faiss
import json
from config import MODEL_NAME, MAX_LENGTH, DEVICE, CHAT_HISTORY_PATH, DEFAULT_RESPONSES_PATH
import hazm

class RAGModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(DEVICE)
        self.sentence_transformer = SentenceTransformer(MODEL_NAME)
        self.normalizer = hazm.Normalizer()
        
        self.chat_history = self.load_json(CHAT_HISTORY_PATH)
        self.default_responses = self.load_json(DEFAULT_RESPONSES_PATH)
        
        self.index = self.build_faiss_index()

    def load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def build_faiss_index(self):
        texts = [qa['question'] for qa in self.chat_history]
        embeddings = self.sentence_transformer.encode(texts)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index

    def retrieve_similar_questions(self, query, k=5):
        query_vector = self.sentence_transformer.encode([query])
        _, indices = self.index.search(query_vector, k)
        return [self.chat_history[i] for i in indices[0]]

    async def generate_response(self, user_message):
        normalized_message = self.normalizer.normalize(user_message)
        similar_qa = self.retrieve_similar_questions(normalized_message)
        
        context = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in similar_qa])
        prompt = f"{context}\n\nQ: {normalized_message}\nA:"
        
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
        
        output = self.model.generate(
            input_ids,
            max_length=MAX_LENGTH,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        # اگر پاسخ مناسبی پیدا نشد، از پاسخ‌های پیش‌فرض استفاده کنید
        if not response or response == prompt:
            response = self.default_responses.get(normalized_message, "متأسفم، نمی‌توانم به این سؤال پاسخ دهم. لطفاً با پشتیبانی تماس بگیرید.")
        
        return response
