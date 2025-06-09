import asyncio
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from mcp_use import MCPAgent, MCPClient

async def run_task_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    
    config_file = "task_manager/tasks_config.json"
    print("Initializing Task Management...")

    # Create client from config file (similar to your weather example)
    client = MCPClient.from_config_file(config_file)
    
    # Setup LLM - you can easily change this to any LangChain LLM
    llm = ChatGroq(model="qwen-qwq-32b")
    
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )
    
    print("\n" + "="*50)
    print("TASK MANAGEMENT ASSISTANT")
    print("="*50)
    print("I can help you manage your tasks! Try saying:")
    print("• 'Add a task to buy groceries with high priority'")
    print("• 'Show me all my tasks'")
    print("• 'Mark task 1 as completed'")
    print("• 'What are my task statistics?'")
    print("• 'Delete task 2'")
    print("\nType 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("="*50)

    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!!")
                break
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue
            print("Assistant: ", end="", flush=True)
            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"Error: {e}")
                print("Make sure the task server is running on http://localhost:8001")
    except KeyboardInterrupt:
        print("\nClosing the server.")
    finally:
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_task_chat())