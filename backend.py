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
    # model_name = "gpt2"  # You can use other models like 'EleutherAI/gpt-neo-125M'
    model_name = "EleutherAI/gpt-neo-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        return_attention_mask=True
        )

    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_new_tokens=250,  # Număr maxim de tokeni generați
        num_return_sequences=1,
        temperature=0.5, 
        do_sample=True,
        top_p=0.7, 
        repetition_penalty=2.0  # Penalizare pentru repetare
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # return response
    return response[len(prompt):].strip()

# Call the main function to run the app
if __name__ == "__main__":
    main()
