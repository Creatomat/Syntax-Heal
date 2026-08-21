import ollama
import os
import threading
import time
import sys

BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
GRAY = '\033[90m'
BOLD = '\033[1m'
RESET = '\033[0m'
is_thinking = True

def spin():
    chars = "|/-\\"
    i = 0
    while is_thinking:
        print(f"\r{CYAN}Thinking {chars[i % 4]}{RESET}", end="", flush=True)
        time.sleep(0.1)
        i += 1

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

def main():
    global is_thinking
    clear_screen()
    print(f"{BOLD}{YELLOW}Syntax Heal {RESET}\n{CYAN}The Local AI Debugging Companion!")

    try:
        while True:
            user_code = get_text(f"{GREEN}\nPaste your code:")
            if user_code == "RETRY":
                print(f"{GREEN}\nTry again:")
                continue
            if user_code == "EXIT":
                print(f"{CYAN}\nExiting...")
                clear_screen()
                break
            user_error = get_text(f"{GREEN}\nPaste error text:")
            if user_error == "RETRY":
                print(f"{GREEN}\nTry again:")
                continue
            if user_error == "EXIT":
                print(f"{CYAN}\nExiting...")
                clear_screen()
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

            is_thinking = True
            threading.Thread(target=spin, daemon=True).start()

            try:
                stream = ollama.chat(
                    model="qwen3:8b",
                    messages=model_comm,
                    options={
                        'temperature': 0.0
                    },
                    stream=True
                )

                first_word = True
                
                for chunk in stream:
                    content = chunk["message"]["content"]
                    if first_word and content:
                        is_thinking = False
                        print(f"\r{' ' * 20}\r{BOLD}{GREEN}Solution:{RESET}\n")
                        first_word = False
                
                    print(content, end="", flush=True)

                print(f"\n\n\n{YELLOW}Time to solve something else!")
            
            except ollama.ResponseError as e:
                if "not found" in str(e).lower():
                    print(f"\n{RED}Error: Model 'qwen3:8b' not found{RESET}")
                    print(f"\n{GRAY}Please run 'ollama pull qwen3:8b' before proceeding{RESET}")
                else:
                    print(f"\n{RED}Ollama API Error: {e}{RESET}")

            except ConnectionError:
                print(f"\n{RED}Could not connect to the Ollama Service{RESET}")
                print(f"\n{GRAY}Please ensure the ollama background service is running!{RESET}")
            
            except Exception as e:
                if "connection refused" in str(e).lower():
                    print(f"\n{RED}Error: Ollama connection refused. Is the ollama running?{RESET}")
                else:
                    print(f"\n{RED}An unexpected error occurred: {e}{RESET}")
    
    except KeyboardInterrupt:# Clears the current line and prints a clean exit message
        print(f"\n\n{RED}Session interrupted (Ctrl+C). Exiting...{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()