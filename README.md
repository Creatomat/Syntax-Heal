# Syntax-Heal
> Local AI-powered code debugging, suggestions, and error corrector right in your terminal.

## What It Can Do
*   **Completely Offline:** Runs entirely on your local hardware via Ollama. Your source code and error logs never leave your machine.
*   **Multi-Language Support:** Dynamically adjusts its debugging logic and system prompts based on the specific programming language you input.

## How to Run (Precompiled Releases)

### Windows
* Download the `syntaxheal.exe` release.
* Double-click the `.exe` file directly.

### Linux
* Download the `syntaxheal` binary from releases.
* Make the binary executable:
  ```bash
  chmod +x syntaxheal

## Setup & Installation
To run Syntax-Heal, ensure your system meets the following prerequisites:

1. Install **Python 3** on your system.
2. Install **Ollama** and start the background service. 
3. Pull the required language model by running `ollama run qwen3:8b` in your terminal.
4. Install the Python integration library by running `pip install ollama`.
5. Run the tool directly using `python3 syntaxheal.py` or compile it into a standalone binary using PyInstaller for global terminal access.

## AI Usage Disclaimer
*   **Verification Required:** This tool utilizes a local Large Language Model to generate debugging suggestions. AI models can occasionally produce inaccurate, incomplete, or highly confident but incorrect solutions (hallucinations).
*   **Human Oversight:** The generated explanations should be used as a supplementary guide. Always review the logic and test the suggested code fixes independently before implementing them into your projects.
