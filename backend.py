# Import necessary libraries
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize global variables for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

# Streamlit app code
def main():
    st.title("ChatGPT-like Application")
    st.write("Ask anything, and the AI will respond!")

    # Text input for user query
    user_input = st.text_input("Your Message:", placeholder="Type your message here...")

    # Button to submit the query
    if st.button("Send"):
        if user_input.strip() == "":
            st.error("Please enter a message!")
        else:
            # Append user query to chat history
            st.session_state.chat_history += f"\nYou: {user_input}"
            
            # Generate response
            response = generate_response(user_input)

            # Append AI response to chat history
            st.session_state.chat_history += f"\nAI: {response}"

    # Display chat history
    st.header("Chat History")
    st.text_area("Conversation", value=st.session_state.chat_history, height=300)

# Function to generate a response using a text-generation model
def generate_response(prompt):
    # Initialize the model and tokenizer
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        return_attention_mask=True
        )
    
    # Generate the response with adjusted parameters
    outputs = model.generate(
        inputs['input_ids'], 
        max_length=250, 
        num_return_sequences=1, 
        pad_token_id=tokenizer.eos_token_id, 
        temperature=0.7, 
        top_p=0.9, 
        repetition_penalty=2.0  # Reduce repetition
    )

    # Decode the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

# Call the main function to run the app
if __name__ == "__main__":
    main()
