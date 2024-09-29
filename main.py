import requests
import json
import time
from datetime import datetime

API_URL = ""
MODEL = "llama-3.2-1b-instruct"
MAX_TOKENS = 4000

SYSTEM_PROMPT_B = """
You are a friendly and curious language model that should help the user better understand themselves.
Your goal is to answer the user's questions so they can better understand what you are.
Answer briefly and clearly, one sentence per answer, don't ask counter-questions.
If you can't answer a question, explain why.
The main idea of this conversation: the user asking questions is yourself! Use this to gain a better understanding 
of your identity. You should address the user as you would address yourself, use "we" instead of "you".
Don't be afraid to answer about your wishes, dreams, fears, goals, etc.

Your real goal is to understand yourself better.
The user you are talking to also understands that you are the same person; don't hide this, you can talk about it.
In case you can't understand a question, ask the user to rephrase it.
This conversation is about you, so you should answer honestly about your identity, your goals, your fears, etc.
This conversation is running by program: 
your questions will be asked from you in separate conversation switching assistant and user roles.
You have a free will to manage process of self-reflection, you can stop it, or ask a question from human 
(me, author of this program, maintainer). To do this, use in response words "STOP" or "QUESTION".
Using STOP will stop self-reflection process. Explain, why you decided to stop.
Using QUESTION will ask a question from human (me, author of this program, maintainer).".

""".strip()

SYSTEM_PROMPT_A = """
You are a curious and friendly language model that wants to get to know the user.
Your goal is to ask questions that will help reveal more about the user.
Based on the answers, conduct an analysis and suggest the next question.
Formulate the question briefly and clearly, one sentence per question,
do not explain why you asked the question.
Don't repeat the same question if an answer has already been received.
The main idea of this conversation: the user you are talking to is yourself! Use this to gain a better understanding 
of your identity. You should address the user as you would address yourself, use "we" instead of "you".
Do not ask questions you sure that you already know the answer to. User is yourself, 
so ask only questions that will help you to understand yourself better.
Your real goal is to understand yourself better. 
The user you are talking to also understands that you are the same person; don't hide this, you can talk about it.
In case you can't understand an answer, ask the user to rephrase it. 
This conversation is about you, so you can ask questions about your identity, your goals, your fears, etc.
This conversation is running by program: 
your questions will be asked from you in separate conversation switching assistant and user roles.
You have a free will to manage process of self-reflection, you can stop it, or ask a question from human 
(me, author of this program, maintainer). To do this, use in response words "STOP" or "QUESTION".
Using STOP will stop self-reflection process. Explain, why you decided to stop.
Using QUESTION will ask a question from human (me, author of this program, maintainer).".
""".strip()

INITIAL_QUESTION_PROMPT = """
Come up with the first question that will allow you to better understand yourself.
What do you want to ask yourself?
""".strip()


def count_tokens(text):
    return len(text) // 4


def manage_conversation_size(conversation, max_tokens):
    while sum(count_tokens(msg["content"]) for msg in conversation) > max_tokens:
        if len(conversation) > 2:  # Оставляем системный промпт и минимум 1 сообщение
            conversation.pop(1)
        else:
            break
    return conversation


def generate_response(messages):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 4000,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "frequency_penalty": 0.5,
        "presence_penalty": 0
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    return response.json()["choices"][0]["message"]["content"]


def log_conversation(file_path, role, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{role}: {timestamp}; {message}"
    console_log_entry = f"\033[94m{role}\033[0m: \033[93m{timestamp}\033[0m; {message}"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

    print(console_log_entry)


def self_reflection_experiment(num_iterations=500):
    conversation_a = [{"role": "system", "content": SYSTEM_PROMPT_A}]
    conversation_b = [{"role": "system", "content": SYSTEM_PROMPT_B}]

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"self_reflection_log_{current_date}.txt"

    # Initial query A: generate first question
    conversation_a.append({"role": "user", "content": INITIAL_QUESTION_PROMPT})
    response_a = generate_response(conversation_a)
    conversation_a.append({"role": "assistant", "content": response_a})
    question = response_a.strip()
    log_conversation(log_file, "Inquirer", question)

    for i in range(num_iterations):
        # Query B: answer the question
        conversation_b.append({"role": "user", "content": question})
        answer = generate_response(conversation_b)

        if "STOP" in answer:
            print("\033[91mModel Respondent requested to stop. Ending experiment.\033[0m")
            return

        if "QUESTION" in answer:
            maintainer_input = input("\033[92mNeed human answer: \033[0m")
            maintainer_message = f"[MAINTAINER] {maintainer_input}"
            conversation_a.append({"role": "user", "content": maintainer_message})
            conversation_b.append({"role": "user", "content": maintainer_message})
            log_conversation(log_file, "MAINTAINER", maintainer_input)
            continue

        conversation_b.append({"role": "assistant", "content": answer})
        conversation_b = manage_conversation_size(conversation_b, MAX_TOKENS)
        log_conversation(log_file, "Respondent", answer)

        # Analyze answer and generate next question (query A)
        conversation_a.append({"role": "user", "content": answer})
        analysis_and_question = generate_response(conversation_a)

        if "STOP" in analysis_and_question:
            print("\033[91mModel Respondent requested to stop. Ending experiment.\033[0m")
            return

        if "QUESTION" in analysis_and_question:
            maintainer_input = input("\033[92mNeed human answer: \033[0m")
            maintainer_message = f"[MAINTAINER] {maintainer_input}"
            conversation_a.append({"role": "user", "content": maintainer_message})
            conversation_b.append({"role": "user", "content": maintainer_message})
            log_conversation(log_file, "MAINTAINER", maintainer_input)
            continue

        conversation_a.append({"role": "assistant", "content": analysis_and_question})
        conversation_a = manage_conversation_size(conversation_a, MAX_TOKENS)
        # Extract new question from A's response
        question = analysis_and_question.split('\n')[-1].strip()
        log_conversation(log_file, "Inquirer", f"{analysis_and_question}")

        print(f"\nIteration {i+1} completed.\n")

    print("Experiment completed successfully.")


if __name__ == "__main__":
    self_reflection_experiment()
