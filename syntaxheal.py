import ollama
import os
import sys
from rich import print as rprint
from rich.panel import Panel
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.prompt import Prompt

Prompt.prompt_suffix = ""

console = Console()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_text(user_ins):
    rprint(user_ins)
    rprint ("[#808080]Type 'DONE' on a new line to continue\nType 'RETRY' if you want to start over\nType 'EXIT' to exit at any time[/#808080]")

    lines = []
    while True:
        line = Prompt.ask("[bold cyan]>[/]")
        if line == "DONE":
            break
        if line == "RETRY":
            return "RETRY"
        if line == "EXIT":
            return "EXIT"

        lines.append(line)

    return "\n".join(lines)

def main():
    clear_screen()
    rprint(Panel.fit("[bold yellow]Syntax Heal [/bold yellow]\n[italic cyan]The Local AI Debugging Companion![/italic cyan]", title="Hello user!", border_style="green"))

    try:
        while True:
            user_code = get_text("[green]\nPaste your code:")
            if user_code == "RETRY":
                rprint("[green]\nTry again")
                continue
            if user_code == "EXIT":
                rprint("[cyan]\nExiting...")
                clear_screen()
                break
            user_error = get_text("[green]\nPaste error text:")
            if user_error == "RETRY":
                rprint("[green]\nTry again")
                continue
            if user_error == "EXIT":
                rprint("[cyan]\nExiting...")
                clear_screen()
                break
            
            user_lang = Prompt.ask("[green]\nWhat programming language is this? [/green]")

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

            try:
                stream = ollama.chat(
                    model="qwen3:8b",
                    messages=model_comm,
                    options={
                        'temperature': 0.0
                    },
                    stream=True
                )

                full_response = ""

                with Live(Panel("Thinking...", border_style="cyan"), console=console, refresh_per_second=15) as live:
                    
                    for chunk in stream:
                        content = chunk["message"]["content"]
                        if content:
                            full_response += content
                            
                            rendered_markdown = Markdown(full_response)
                            
                            live_panel = Panel(
                                rendered_markdown, 
                                title="[bold green]Solution", 
                                border_style="green"
                            )
                            live.update(live_panel)

                rprint("\n\n\n[yellow]Time to solve something else![/yellow]")
            
            except ollama.ResponseError as e:
                if "not found" in str(e).lower():
                    rprint("\n[red]Error: Model 'qwen3:8b' not found[/red]")
                    rprint("\n[#808080]Please run 'ollama pull qwen3:8b' before proceeding[/#808080]")
                else:
                    rprint(f"\n[red]Ollama API Error: {escape(str(e))}[/red]")

            except ConnectionError:
                rprint("\n[red]Could not connect to the Ollama Service[/red]")
                rprint("\n[#808080]Please ensure the ollama background service is running![/#808080]")
            
            except Exception as e:
                if "connection refused" in str(e).lower():
                    rprint("\n[red]Error: Ollama connection refused. Is ollama running?[/red]")
                else:
                    rprint(f"\n[red]An unexpected error occurred: {escape(str(e))}[/red]")
    
    except KeyboardInterrupt:# Clears the current line and prints a clean exit message
        rprint("\n\n[red]Session interrupted (Ctrl+C). Exiting...[/red]")
        sys.exit(0)

if __name__ == "__main__":
    main()