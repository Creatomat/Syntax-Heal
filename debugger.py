import ollama
import os

BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
GRAY = '\033[90m'
BOLD = '\033[1m'
RESET = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_text(user_ins):
    print(user_ins)
    print (f"{GRAY}Type 'DONE' on a new line to continue\nType 'RETRY' if you want to start over\nType 'EXIT' to exit at any time{RESET}")

    lines = []
    while True:
        line = input()
        if line == "DONE":
            break
        if line == "RETRY":
            return "RETRY"
        if line == "EXIT":
            return "EXIT"

        lines.append(line)

    return "\n".join(lines)

clear_screen()
print(f"{BOLD}{YELLOW}Syntax Heal {RESET}\n{CYAN}The Local AI Debugging Companion!")

while True:
    user_code = get_text(f"{GREEN}\nPaste your code:")
    if user_code == "RETRY":
        print(f"{GREEN}\nTry again:")
        continue
    if user_code == "EXIT":
        print(f"{CYAN}\nExiting...")
        break
    user_error = get_text(f"{GREEN}\nPaste error text:")
    if user_error == "RETRY":
        print(f"{GREEN}\nTry again:")
        continue
    if user_error == "EXIT":
        print(f"{CYAN}\nExiting...")
        break
    
    user_lang = input(f"{GREEN}\nWhat programming language is this? {RESET}")

    model_comm = [
        {
            "role": "system",
            "content": f"You are an expert debugger in {user_lang}. Based on the error given, suggest a fix and why the error occured as two seperate labelled lines of text of the format \n Why it happened: <Tell user why> \n How to fix it: <suggest a fix without making it convuluded and keep it short without compromising on program functionality>"
        },
        {
            "role": "user",
            "content": f"Code:\n{user_code}\n\nError:\n{user_error}"
        }
    ]

    stream = ollama.chat(
        model="qwen3:8b",
        messages=model_comm,
        stream=True
    )

    print(f"\n{BOLD}{GREEN}Solution:{RESET}")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

    print("\nTime to solve something else!")