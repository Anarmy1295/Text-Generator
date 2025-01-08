# Import necessary libraries
# import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from functions import split_input, sample_n_words, sample_next_word, stochastic_matrix, k_secv, k_secv_idx, distinct_k_secv, distinct_words, word_idx, prob_choose

# # # Initialize global variables for chat history
# # if "chat_history" not in st.session_state:
# #     st.session_state.chat_history = ""

# # MODEL_NAME = "gpt2-medium"
# # # MODEL_NAME = "gpt2-large"
# # model_name = "EleutherAI/gpt-neo-1.3B"

# # try:
# #     # tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
# #     # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

# #     # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)
# #     # if torch.cuda.is_available():
# #     #     model.to('cuda')

# #     tokenizer = AutoTokenizer.from_pretrained(model_name)
# #     model = AutoModelForCausalLM.from_pretrained(model_name)

# #     model.eval()
# #     if torch.cuda.is_available():
# #         model.to('cuda')
# # except Exception as e:
# #     print(f"Error loading the model: {e}")
# #     raise

# # Streamlit app code
# def main_screen():
#     st.title("ChatGPT-like Application")
#     st.write("Ask anything, and the AI will respond!")

#     # Initialize global variables for chat history
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = ""

#     MODEL_NAME = "gpt2-medium"
#     # MODEL_NAME = "gpt2-large"
#     model_name = "EleutherAI/gpt-neo-1.3B"

#     try:
#         # tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
#         # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

#         # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)
#         # if torch.cuda.is_available():
#         #     model.to('cuda')

#         tokenizer = AutoTokenizer.from_pretrained(model_name)
#         model = AutoModelForCausalLM.from_pretrained(model_name)

#         model.eval()
#         if torch.cuda.is_available():
#             model.to('cuda')
#     except Exception as e:
#         print(f"Error loading the model: {e}")
#         raise

#     # Text input for user query
#     user_input = st.text_input("Your Message:", placeholder="Type your message here...")

#     # Button to submit the query
#     if st.button("Send"):
#         if user_input.strip() == "":
#             st.error("Please enter a message!")
#         else:
#             # Append user query to chat history
#             st.session_state.chat_history += f"\nYou: {user_input}"
            
#             # Generate response
#             response = generate_response(user_input)

#             # Append AI response to chat history
#             st.session_state.chat_history += f"\nAI: {response}"

#     # Display chat history
#     st.header("Chat History")
#     st.text_area("Conversation", value=st.session_state.chat_history, height=300)

# # Function to generate a response using a text-generation model
# # def generate_response(prompt):
# #     # # Initialize the model and tokenizer
# #     # # model_name = "gpt2"  # You can use other models like 'EleutherAI/gpt-neo-125M'
# #     # model_name = "EleutherAI/gpt-neo-1.3B"
# #     # tokenizer = AutoTokenizer.from_pretrained(model_name)
# #     # model = AutoModelForCausalLM.from_pretrained(model_name)

# #     # Tokenize the prompt
# #     inputs = tokenizer(
# #         prompt,
# #         return_tensors="pt",
# #         truncation=True,
# #         return_attention_mask=True
# #         )
    
# #             # Move input_ids to GPU if available
# #     if torch.cuda.is_available():
# #         inputs = inputs.to('cuda')

# #     outputs = model.generate(
# #         inputs['input_ids'],
# #         attention_mask=inputs['attention_mask'],
# #         max_new_tokens=150,  # Număr maxim de tokeni generați
# #         num_return_sequences=1,
# #         temperature=0.7, 
# #         do_sample=True,
# #         top_p=0.9,
# #         top_k=50,
# #         repetition_penalty=1.2,  # Penalizare pentru repetare
# #         eos_token_id=tokenizer.eos_token_id
# #         )

# #     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# #     # Truncate at the first occurrence of a stop sequence
# #     # stop_sequence = "\n"
# #     # if stop_sequence in response:
# #     #     response = response.split(stop_sequence)[0]

# #     # print("response: " + response)

# #     # return response
# #     return response[len(prompt):].strip()

# def generate_response(prompt):
#     # Tokenize the prompt
#     inputs = tokenizer(
#         prompt,
#         return_tensors="pt",
#         truncation=True,
#         return_attention_mask=True
#     )

#     # Move inputs to GPU if available
#     if torch.cuda.is_available():
#         inputs = inputs.to('cuda')

#     # # Generate the response
#     # outputs = model.generate(
#     #     inputs['input_ids'],
#     #     attention_mask=inputs['attention_mask'],
#     #     max_new_tokens=150,  # Number of new tokens to generate
#     #     num_return_sequences=1,
#     #     temperature=0.7,
#     #     do_sample=True,
#     #     top_p=0.9,
#     #     top_k=50,
#     #     repetition_penalty=1.2,
#     #     eos_token_id=tokenizer.eos_token_id
#     # )

#     # Generate the response
#     outputs = model.generate(
#         inputs['input_ids'],
#         attention_mask=inputs['attention_mask'],
#         max_new_tokens=200,  # Number of new tokens to generate
#         num_return_sequences=1,
#         temperature=1,
#         do_sample=True,
#         top_p=0.95,
#         top_k=100,
#         repetition_penalty=1.1,
#         eos_token_id=tokenizer.eos_token_id
#     )

#     # Decode and clean up the response
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Ensure the output doesn't repeat the input
#     response = response[len(prompt):].strip()

#     # # Truncate at a stop sequence if one exists (e.g., newline)
#     # stop_sequence = "\n"
#     # if stop_sequence in response:
#     #     response = response.split(stop_sequence)[0]

#     return response


# # Call the main function to run the app
# if __name__ == "__main__":
#     main_screen()

def generate_response(prompt, mode):
    if(mode == "faster"):
        model_name = "gpt2"

        try:
            tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            model = GPT2LMHeadModel.from_pretrained(model_name)

            # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)

            model.eval()
            if torch.cuda.is_available():
                model.to('cuda')
        except Exception as e:
            print(f"Error loading the model: {e}")
            raise
    else:
        model_name = "EleutherAI/gpt-neo-1.3B"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name)

            model.eval()
            if torch.cuda.is_available():
                model.to('cuda')
        except Exception as e:
            print(f"Error loading the model: {e}")
            raise

# # MODEL_NAME = "gpt2-medium"
# # # MODEL_NAME = "gpt2-large"
# # model_name = "EleutherAI/gpt-neo-1.3B"

    try:
        # tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
        # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

        # model = GPT2LMHeadModel.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)
        # if torch.cuda.is_available():
        #     model.to('cuda')

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        model.eval()
        if torch.cuda.is_available():
            model.to('cuda')
    except Exception as e:
        print(f"Error loading the model: {e}")
        raise

    # Tokenize the prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        return_attention_mask=True
    )

    # Move inputs to GPU if available
    if torch.cuda.is_available():
        inputs = inputs.to('cuda')

    # # Generate the response
    # outputs = model.generate(
    #     inputs['input_ids'],
    #     attention_mask=inputs['attention_mask'],
    #     max_new_tokens=150,  # Number of new tokens to generate
    #     num_return_sequences=1,
    #     temperature=0.7,
    #     do_sample=True,
    #     top_p=0.9,
    #     top_k=50,
    #     repetition_penalty=1.2,
    #     eos_token_id=tokenizer.eos_token_id
    # )

    # Generate the response
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_new_tokens=200,  # Number of new tokens to generate
        num_return_sequences=1,
        temperature=1,
        do_sample=True,
        top_p=0.95,
        top_k=100,
        repetition_penalty=1.1,
        eos_token_id=tokenizer.eos_token_id
    )

    # Decode and clean up the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Ensure the output doesn't repeat the input
    response = response[len(prompt):].strip()

    # # Truncate at a stop sequence if one exists (e.g., newline)
    # stop_sequence = "\n"
    # if stop_sequence in response:
    #     response = response.split(stop_sequence)[0]

    return response

def generate_response_pdf(text, prompt):
    corpus = split_input(text)
    k = 2
    word_set = distinct_words(corpus)
    k_secv_corpus = k_secv(corpus, k)
    k_secv_set = distinct_k_secv(k_secv_corpus)
    widx = word_idx(word_set)
    kscvidx = k_secv_idx(k_secv_set)
    stoch = stochastic_matrix(k_secv_corpus, corpus, word_set, k_secv_set, k)
    probs = sample_next_word(split_input(prompt), widx, kscvidx, k, stoch)
    prob_choose(probs, word_set)
    sample_n_words(split_input(prompt), widx, kscvidx, k, stoch, word_set, 10)
