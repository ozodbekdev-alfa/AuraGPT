#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import threading
import itertools
import requests
from urllib.parse import quote
from colorama import init as colorama_init, Fore, Style

colorama_init()

API_URL = "https://ozodbekdev.uz/api/deepai/"
SYSTEM_PROMPT = ""
MAX_HISTORY = 15
HISTORY_FILE = "history.json"
REQUEST_TIMEOUT = 60
TYPING_DELAY = 0.04
SPINNER_DELAY = 0.08
SPINNER_CHARS = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except:
        return []
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except:
        pass

def trim_history(history):
    if len(history) > MAX_HISTORY:
        return history[-MAX_HISTORY:]
    return history

def build_prompt(history_prev, user_input):
    lines = []
    for msg in history_prev:
        role = msg.get("role", "")
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            lines.append("User: " + content)
        elif role == "assistant":
            lines.append("Assistant: " + content)
    lines.append("User: " + user_input.strip())
    lines.append("Assistant:")
    return "\n".join(lines)

def spinner_task(stop_event):
    for ch in itertools.cycle(SPINNER_CHARS):
        if stop_event.is_set():
            break
        sys.stdout.write(Fore.GREEN + f"{ch}" + Style.RESET_ALL + "\r")
        sys.stdout.flush()
        time.sleep(SPINNER_DELAY)
    sys.stdout.write(" " * 50 + "\r")
    sys.stdout.flush()

def send_api_request(prompt_text):
    stop_event = threading.Event()
    spinner = threading.Thread(target=spinner_task, args=(stop_event,), daemon=True)
    spinner.start()
    try:
        query = f"?sh={quote(prompt_text)}"
        url = API_URL + query
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        result = data.get("Javob", "Xato: API javobida 'Javob' maydoni topilmadi.")
    except Exception as e:
        stop_event.set()
        spinner.join()
        raise RuntimeError(f"So'rov yuborishda xatolik: {e}")
    stop_event.set()
    spinner.join()
    return str(result)

def typing_print_colored(text, color=Fore.RED, delay=TYPING_DELAY):
    words = text.split()
    for w in words:
        sys.stdout.write(color + w + " " + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def main_loop():
    history = trim_history(load_history())
    print()
    while True:
        try:
            user_input = input(Fore.BLUE + "Siz: " + Style.RESET_ALL).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + Fore.YELLOW + "Sessiyadan chiqilyapti..." + Style.RESET_ALL)
            break
        if not user_input:
            continue
        if user_input.lower() == "/exit":
            print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
            break
        history.append({"role": "user", "content": user_input})
        history = trim_history(history)
        save_history(history)
        history_prev = history[:-1]
        prompt_text = build_prompt(history_prev, user_input)
        try:
            assistant_text = send_api_request(prompt_text)
        except Exception as e:
            print(Fore.RED + f"\nXato: {e}" + Style.RESET_ALL)
            continue
        sys.stdout.write(Style.BRIGHT + Fore.RED + "Aura: " + Style.RESET_ALL)
        sys.stdout.flush()
        typing_print_colored(assistant_text, color=Fore.RED, delay=TYPING_DELAY)
        history.append({"role": "assistant", "content": assistant_text})
        history = trim_history(history)
        save_history(history)
    save_history(history)
    print(Fore.GREEN + "Sessiya saqlandi" + Style.RESET_ALL)

if __name__ == "__main__":
    main_loop()
