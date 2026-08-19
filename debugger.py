import ollama

def get_text(user_ins):
    print(user_ins)
    print ("(Paste your text, then type 'DONE' on a new line)")

    lines = []
    while True:
        line = input()
        if line == "DONE":
            break
        lines.append(line)

    return "\n".join(lines)

print("Syntax Heal \nThe Local AI Debugging Companion!")

while True:
    user_error = get_text("\n Paste error text:")
    user_code = get_text("\n Paste your code:")

    model_comm = [
        {
            "role": "system",
            "content": "You are a python debugger. Based on the error given, suggest a fix and why the error occured as two seperate labelled lines of text of the format \n Why it happened: <Tell user why> \n How to fix it: <suggest a fix without making it convuluded and keep it short without compromising on program functionality>"
        },
        {
            "role": "user",
            "content": f"Code:\n{user_code}\n\nError:\n{user_error}"
        }
    ]

    print("\nThinking...")

    stream = ollama.chat(
        model="qwen3:8b",
        messages=model_comm,
        stream=True
    )

    print("\nSolution:")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)