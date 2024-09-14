import os
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import readline

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Rich console
console = Console()

def load_system_prompt():
    with open('./system.yaml', 'r') as file:
        system_data = yaml.safe_load(file)
    return system_data

def get_user_input(prompt):
    return input(prompt)

def chat_with_ai():
    console.print("Welcome to CLISim - Command Line Interface Simulator", style="bold green")
    console.print("Type 'quit' to exit the chat.", style="italic")
    console.print("Use the up arrow key to access previous queries.", style="italic")
    
    conversation = []
    system_prompt = load_system_prompt()
    
    # Add system prompt as a user message to proxy the system message
    conversation.append({"role": "user", "content": str(system_prompt)})
    
    # Initialize readline history
    readline.clear_history()
    
    while True:
        user_input = get_user_input("clisim$ ").strip()
        
        if user_input.lower() == 'quit':
            console.print("Exiting CLISim. Goodbye!!", style="bold green")
            break

        # Add the user input to readline history
        readline.add_history(user_input)

        assistant_message = """
Initializing systems... ✅                                                                                                                                                                                                                │
                                                                                                                                                                                                                                           │
Greetings! Welcome to CLISim - Command Line Interface Simulator?  
"""
        conversation.append({"role": "assistant", "content": assistant_message})
        conversation.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="o1-preview",
                messages=conversation,
                max_completion_tokens=4096
            )
            
            ai_response = response.choices[0].message.content
            
            if ai_response.strip():
                # Format AI response as markdown
                md = Markdown(ai_response)
                ai_panel = Panel(md, border_style="green", expand=False)
                console.print(ai_panel)
            else:
                console.print("Error: Received an empty response from the API.", style="bold red")
            
            conversation.append({"role": "assistant", "content": ai_response})
        
        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="bold red")

if __name__ == "__main__":
    chat_with_ai()