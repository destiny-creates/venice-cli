from openai import OpenAI
import sys

# Initialize the OpenAI client with Venice's base URL
client = OpenAI(
    api_key="REDACTED",
    base_url="https://api.venice.ai/api/v1"
)

# Initialize conversation history
conversation_history = []

def chat_with_venice_streaming(user_message, model="venice-uncensored"):
    global conversation_history
    
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})
    
    try:
        # Create streaming chat completion
        stream = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=0.7,
            max_tokens=2048,
            stream=True
        )
        
        print("Assistant: ", end="", flush=True)
        full_response = ""
        
        # Process each chunk as it arrives
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)  # Print immediately without newline
                full_response += content
        
        print()  # Add newline after complete response
        sys.stdout.flush()  # Ensure output is flushed
        
        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": full_response})
        
        return full_response
        
    except KeyboardInterrupt:
        print("\n\nConversation interrupted by user.")
        return None
    except Exception as e:
        print(f"\nError: {e}")
        return None

def main():
    print("=== Venice AI Conversation ===")
    print("Type 'quit', 'exit', or press Ctrl+C to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("Type 'history' to see conversation history")
    print("=" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                conversation_history.clear()
                print("Conversation history cleared.")
                continue
            elif user_input.lower() == 'history':
                print("\n=== Conversation History ===")
                for i, msg in enumerate(conversation_history):
                    role = msg['role'].capitalize()
                    content = msg['content']
                    print(f"{i+1}. {role}: {content[:100]}{'...' if len(content) > 100 else ''}")
                print("=" * 30)
                continue
            elif not user_input:
                print("Please enter a message.")
                continue
            
            # Send message and get streaming response
            chat_with_venice_streaming(user_input)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()