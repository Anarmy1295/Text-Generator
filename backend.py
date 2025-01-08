# Import necessary libraries
# import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from functions import split_input, sample_n_words, sample_next_word, stochastic_matrix, k_secv, k_secv_idx, distinct_k_secv, distinct_words, word_idx, prob_choose

def generate_response(prompt, mode):
    if(mode == "faster"):
        model_name = "gpt2"

        try:
            tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            model = GPT2LMHeadModel.from_pretrained(model_name)

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

    try:
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

    # Generate the response
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_new_tokens=200,  # Number of new tokens to generate
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True,
        top_p=0.95,
        top_k=70,
        repetition_penalty=1.2,
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
    return sample_n_words(split_input(prompt), widx, kscvidx, k, stoch, word_set, 10)
