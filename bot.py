import json
import os
import logging
import pandas as pd
import torch
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
from telegram import Update

# logging
logging.basicConfig(format='%(asctime)s - %(name=s) - %(levelname)s - %(message)s', level=logging.INFO)

# models
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name_or_id = "MehdiHosseiniMoghadam/AVA-Llama-3-V2"
model = AutoModelForCausalLM.from_pretrained(model_name_or_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_id)
semantic_model = SentenceTransformer('sentence-transformers/LaBSE')

# load FAQ data from CSV
faq_df = pd.read_csv('faq.csv').dropna()
faq_questions = faq_df['question'].tolist()
faq_answers = faq_df['answer'].tolist()
faq_embeddings = semantic_model.encode(faq_questions, convert_to_tensor=True)

# user data
user_data_file = "user_data.json"
if os.path.exists(user_data_file):
    with open(user_data_file, "r") as file:
        user_data = json.load(file)
else:
    user_data = {}

# save user data
def save_user_data():
    with open(user_data_file, "w") as file:
        json.dump(user_data, file)

# update user data
def collect_user_info(user_id, message):
    user = user_data.get(user_id, {
        "name": "",
        "purchased_items": [],
        "payment_history": [],
        "chat_history": []
    })
    user["chat_history"].append(message)
    user_data[user_id] = user
    save_user_data()

# search the FAQ
def search_faq(question, num_res=3):
    question_embedding = semantic_model.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(question_embedding, faq_embeddings, top_k=num_res)[0]
    relevant_faq = [(faq_questions[hit['corpus_id']], faq_answers[hit['corpus_id']]) for hit in hits]
    return relevant_faq

# generate a response using the language model
def generate_response(faq_data, question, user_chat_history):
    try:
        # Create a prompt based on FAQ data and user chat history
        prompt = "### FAQ Database:\n"
        for q, a in faq_data:
            prompt += f"Q: {q}\nA: {a}\n"
        if user_chat_history:
            prompt += "\n### User Chat History:\n" + " ".join(user_chat_history[-5:]) + "\n"
        prompt += f"\n### User Question:\nQ: {question}\n### Assistant:\nA:"

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(inputs, max_length=300, temperature=0.7, top_k=50, num_return_sequences=1, do_sample=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error during generation: {e}")
        return "Error during generation"

# /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام من Orv هستم")

# private messages
def handle_message(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    message = update.message.text
    
    # Preprocessing: spell check, synonym replacement, entity recognition
    # This is a placeholder, you should implement specific methods
    processed_message = preprocess_message(message)
    
    collect_user_info(user_id, processed_message)
    
    # Search for relevant FAQs
    relevant_faqs = search_faq(processed_message)
    
    # Generate a response using the language model and the relevant FAQ data
    response = generate_response(relevant_faqs, processed_message, user_data[user_id]["chat_history"])
    
    # Post-processing: Ensure response consistency and relevancy
    final_response = postprocess_response(response)
    
    update.message.reply_text(final_response)

# group messages
def handle_group_message(update: Update, context: CallbackContext):
    if should_respond_to_group_message(update.message.text):
        handle_message(update, context)

# should respond in a group or not
def should_respond_to_group_message(message):
    keywords = ['کلمه یک', 'کلمه دو', 'کلمه سه']
    return any(keyword in message for keyword in keywords)

# feedback mechanism
def feedback(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    feedback_message = update.message.text
    # Save feedback for further analysis
    save_feedback(user_id, feedback_message)
    update.message.reply_text("بازخورد شما ثبت شد. متشکریم!")

# preprocessing placeholder
def preprocess_message(message):
    # Implement spell check, synonym replacement, and entity recognition here
    return message

# postprocessing placeholder
def postprocess_response(response):
    # Implement any post-processing logic here
    return response

# feedback saving placeholder
def save_feedback(user_id, feedback_message):
    feedback_file = "feedback.json"
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as file:
            feedback_data = json.load(file)
    else:
        feedback_data = {}

    feedback_data[user_id] = feedback_data.get(user_id, []) + [feedback_message]

    with open(feedback_file, "w") as file:
        json.dump(feedback_data, file)

# the bot
TOKEN = "7000348946:AAEv39Hg3hR4gNbtAeA7xPMFmwm6Z81SY5o"  #it's useless, don't take, just for test

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("feedback", feedback))
dispatcher.add_handler(MessageHandler(Filters.private & Filters.text, handle_message))
dispatcher.add_handler(MessageHandler(Filters.group & Filters.text, handle_group_message))
updater.start_polling()
updater.idle()
