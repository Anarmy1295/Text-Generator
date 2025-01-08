import re

def split_input(text):
    """
    Splits the input text into tokens, handling punctuation as separate tokens.
    
    Args:
        text (str): The input string (e.g., extracted PDF content).
        
    Returns:
        list: A list of tokens.
    """
    # print(f"text: {text}")

    # Step 1: Rough tokenization
    # rough_tokens = re.findall(r'\S+', text)  # Splits text into tokens (non-whitespace)
    rough_tokens = re.findall(r'\b\w+\b', text)


    # print(f"rough_tokens: {rough_tokens}")

    # # Step 2: Initialize tokens list
    # tokens = []

    # # Step 3: Process each rough token
    # for tok in rough_tokens:
    #     if len(tok) == 0:  # Skip empty tokens
    #         continue

    #     if len(tok) == 1:  # Single-character tokens are added as is
    #         tokens.append(tok)
    #         continue

    #     # # If the first character is punctuation
    #     # if is_punctuation(tok[0]):
    #     #     tokens.append(tok[0])  # Add the first character as a separate token
    #     #     tokens.append(tok[1:])  # Add the rest of the token
    #     # # If the last character is punctuation
    #     # elif is_punctuation(tok[-1]):
    #     #     tokens.append(tok[:-1])  # Add everything except the last character
    #     #     tokens.append(tok[-1])  # Add the last character as a separate token
    #     # else:
    #     #     tokens.append(tok)  # Add the whole token as is

    #     # If the first character is punctuation
    #     if not is_letter_or_number(tok[0]):
    #         tokens.append(tok[0])  # Add the first character as a separate token
    #         tokens.append(tok[1:])  # Add the rest of the token
    #     # If the last character is punctuation
    #     elif not is_letter_or_number(tok[-1]):
    #         tokens.append(tok[:-1])  # Add everything except the last character
    #         tokens.append(tok[-1])  # Add the last character as a separate token
    #     else:
    #         tokens.append(tok)  # Add the whole token as is

    # print(f"tokens: {tokens}")
    # return tokens
    return rough_tokens

# def split_input(text):
#     """
#     Splits input text into tokens.

#     Args:
#         text (str): The input text to split.

#     Returns:
#         list: A list of tokens.
#     """
    
#     if not isinstance(text, str):
#         raise ValueError(f"Expected text to be a string, but got {type(text)}")

#     # Ensure the text is not empty
#     if not text.strip():
#         raise ValueError("Input text is empty.")

#     # Use re.findall to split into non-whitespace tokens
#     rough_tokens = re.findall(r'\S+', text)
#     return rough_tokens

def is_punctuation(char):
    """
    Checks if a character is a punctuation mark.
    """
    return char in '.,!?;:()[]{}\'"'

def is_letter_or_number(char):
    """
    Checks if a character is a letter or a number.
    """
    return char.isalnum()

# # Example Usage
# text = "Hello, world! Welcome to Python PDF processing."
# tokens = split_input(text)
# print(tokens)

def distinct_words(tokens):
    """
    Finds and returns distinct words from a list of tokens.
    
    Args:
        tokens (list): A list of tokens (words).
        
    Returns:
        list: A sorted list of unique tokens.
    """
    return sorted(set(tokens))

def k_secv(A, k):
    """
    Generates sequences of k consecutive elements from an array and joins them into strings.
    
    Args:
        A (list): Input array of strings.
        k (int): Length of each sequence.
    
    Returns:
        list: A list of k-sequences as concatenated strings.
    """
    n = len(A)
    B = []  # Initialize an empty list to hold the k-sequences

    for i in range(n - k + 1):
        # Extract the k consecutive strings
        strings = A[i : i + k]
        # Join the strings and add to the result
        B.append("".join(strings))

    return B

def distinct_k_secv(cell_array):
    """
    Finds and returns distinct strings from a list of k-sequences.
    
    Args:
        cell_array (list): A list of k-sequences as strings.
    
    Returns:
        list: A sorted list of unique strings.
    """
    return sorted(set(cell_array))

def word_idx(distinct_wds):
    """
    Creates a dictionary mapping distinct words to their indices.
    
    Args:
        distinct_wds (list): A list of distinct words.
    
    Returns:
        dict: A dictionary with words as keys and their indices as values.
    """
    return {word: idx + 1 for idx, word in enumerate(distinct_wds)}

def k_secv_idx(distinct_k_sec):
    """
    Creates a dictionary mapping distinct k-sequences to their indices.
    
    Args:
        distinct_k_sec (list): A list of distinct k-sequences.
    
    Returns:
        dict: A dictionary with k-sequences as keys and their indices as values.
    """
    return {k_sec: idx + 1 for idx, k_sec in enumerate(distinct_k_sec)}

import numpy as np
from scipy.sparse import dok_matrix

def word_idx(words_set):
    """
    Maps words to their indices.
    """
    return {word: idx + 1 for idx, word in enumerate(words_set)}

def k_secv_idx(k_secv_set):
    """
    Maps k-sequences to their indices.
    """
    return {k_sec: idx + 1 for idx, k_sec in enumerate(k_secv_set)}

def stochastic_matrix(k_secv_corpus, corpus_words, words_set, k_secv_set, k):
    """
    Builds the stochastic matrix.
    
    Args:
        k_secv_corpus (list): A list of k-sequences from the corpus.
        corpus_words (list): A list of words from the corpus.
        words_set (list): A list of unique words in the corpus.
        k_secv_set (list): A list of unique k-sequences in the corpus.
        k (int): The k-value for the k-sequences.
    
    Returns:
        scipy.sparse.dok_matrix: The stochastic matrix.
    """
    n = len(k_secv_set)  # Number of k-sequences
    m = len(words_set)   # Number of unique words
    p = len(k_secv_corpus)  # Length of the k-sequence corpus

    # Initialize a sparse matrix (efficient for large datasets)
    retval = dok_matrix((n, m), dtype=int)

    # Get index mappings
    widx = word_idx(words_set)
    kscvidx = k_secv_idx(k_secv_set)

    # Iterate through the corpus
    for i in range(p - k):
        # Get the index for the current k-sequence
        line = kscvidx[k_secv_corpus[i]]
        
        # Get the index for the (i + k)-th word
        col = widx[corpus_words[i + k]]
        
        # Increment the corresponding position in the matrix
        retval[line - 1, col - 1] += 1  # Adjust for zero-based indexing in Python

    return retval


# def sample_next_word(text, words_idx, k_secv_idx, k, stoch):
#     """
#     Returns the probabilities (row of the stochastic matrix) corresponding 
#     to the last k-sequence of the text.
    
#     Args:
#         text (list): The input text (sequence of words).
#         words_idx (dict): Dictionary mapping words to their indices.
#         k_secv_idx (dict): Dictionary mapping k-sequences to their indices.
#         k (int): The length of the k-sequences.
#         stoch (scipy.sparse.dok_matrix or np.ndarray): The stochastic matrix.
    
#     Returns:
#         numpy.ndarray: A row of the stochastic matrix corresponding to the last k-sequence.
#     """
#     n = len(text)
    
#     # Concatenate the last k words from the text to form the k-sequence
#     k_secv_text = "".join(text[n - k:])  # Equivalent to strjoin in Octave
    
#     # Get the index of the current k-sequence
#     i = k_secv_idx[k_secv_text]
    
#     # Retrieve the row of the stochastic matrix corresponding to the k-sequence
#     if isinstance(stoch, np.ndarray):
#         probs = stoch[i - 1, :]  # Adjust for zero-based indexing in Python
#     else:
#         probs = stoch.getrow(i - 1).toarray().flatten()  # For sparse matrix
    
#     return probs

def sample_next_word(text, widx, k_secv_idx, k, stoch):
    """
    Returns the probabilities (row of the stochastic matrix) corresponding 
    to the last k-sequence of the text.
    """
    n = len(text)
    
    # Ensure text has at least k tokens
    if n < k:
        raise ValueError("Input text does not contain enough tokens for k-sequence.")

    # Concatenate the last k tokens to form k_secv_text
    strings = text[n - k:]
    k_secv_text = "".join(strings)

    # Debugging: Check if k_secv_text exists in k_secv_idx
    # print(f"k_secv_idx: {k_secv_idx}")
    print(f"k_secv_text: {k_secv_text}")
    print(f"Available keys in k_secv_idx: {list(k_secv_idx.keys())[:10]}")  # Debugging output

    # Handle missing keys
    if k_secv_text not in k_secv_idx:
        # raise KeyError(f"k_secv_text '{k_secv_text}' not found in k_secv_idx")
        probs = []
        return probs

    # Retrieve the index of the k-sequence
    i = k_secv_idx[k_secv_text]

    # Retrieve the row of the stochastic matrix
    probs = stoch[i - 1, :]
    return probs


import random

# def prob_choose(weights, wset):
#     """
#     Chooses an element from the set `wset` based on the given weights.

#     Args:
#         weights (list or numpy.ndarray): A list of weights for each element in `wset`.
#         wset (list): A list of elements to choose from.

#     Returns:
#         object: A randomly selected element from `wset`, based on the normalized weights.
#     """
#     # Normalize the weight vector
#     total_weight = sum(weights)
#     probabilities = [w / total_weight for w in weights]

#     # Generate a random number between 0 and 1
#     rand_num = random.random()

#     # Initialize cumulative probability
#     cumulative_prob = 0

#     # Iterate over elements of the normalized weight vector
#     for i, prob in enumerate(probabilities):
#         # Check if the random number falls into the range
#         if rand_num >= cumulative_prob and rand_num < cumulative_prob + prob:
#             return wset[i]
#         # Update cumulative probability
#         cumulative_prob += prob

#     # If no element was selected due to rounding issues, return the last element
#     return wset[-1]

import numpy as np

# def prob_choose(weights, wset):
#     """
#     Chooses an element from the set `wset` based on the given weights.

#     Args:
#         weights (list or numpy.ndarray): A list or array of weights for each element in `wset`.
#         wset (list): A list of elements to choose from.

#     Returns:
#         object: A randomly selected element from `wset`, based on the normalized weights.
#     """
#     # Flatten weights if it is a NumPy array
#     if isinstance(weights, np.ndarray):
#         weights = weights.flatten().tolist()

#     # Normalize the weight vector
#     total_weight = sum(weights)
#     probabilities = [w / total_weight for w in weights]

#     # Generate a random number between 0 and 1
#     rand_num = np.random.rand()

#     # Initialize cumulative probability
#     cumulative_prob = 0

#     # Iterate over elements of the normalized weight vector
#     for i, prob in enumerate(probabilities):
#         # Check if the random number falls into the range
#         if cumulative_prob <= rand_num < cumulative_prob + prob:
#             return wset[i]
#         # Update cumulative probability
#         cumulative_prob += prob

#     # Fallback: return the last element
#     return wset[-1]

import random

# def prob_choose(weights, wset):
#     # Normalize the weight vector
#     probabilities = [w / sum(weights) for w in weights]

#     # Generate a random number between 0 and 1
#     rand_num = random.random()

#     # Initialize cumulative probability
#     cumulative_prob = 0

#     # Iterate over elements of the normalized weight vector
#     for i, prob in enumerate(probabilities):
#         # Check if the random number falls into the range
#         if rand_num >= cumulative_prob and rand_num < cumulative_prob + prob:
#             random_number = i
#             return wset[random_number]
#         # Update cumulative probability
#         cumulative_prob += prob

#     return wset[len(probabilities) - 1]

import random

# def prob_choose(weights, wset):
#     # Normalize the weight vector (ensure weights is a list of scalars)
#     weights = list(weights)  # Convert to a list if it's not already
#     probabilities = [w / sum(weights) for w in weights]

#     # Generate a random number between 0 and 1
#     rand_num = random.random()

#     # Initialize cumulative probability
#     cumulative_prob = 0

#     # Iterate over elements of the normalized weight vector
#     for i, prob in enumerate(probabilities):
#         # Check if the random number falls into the range
#         if rand_num >= cumulative_prob and rand_num < (cumulative_prob + prob):
#             return wset[i]
#         # Update cumulative probability
#         cumulative_prob += prob

#     # Fallback return: return the last element of wset
#     return wset[len(probabilities) - 1]

import random
import numpy as np

# def prob_choose(weights, wset):
#     # Normalize the weight vector (convert weights to a NumPy array for safety)
#     weights = np.array(weights)
#     probabilities = weights / np.sum(weights)

#     # Generate a random number between 0 and 1
#     rand_num = random.random()

#     # Initialize cumulative probability
#     cumulative_prob = 0

#     # Iterate over elements of the normalized weight vector
#     for i, prob in enumerate(probabilities):
#         # Check if the random number falls into the range
#         if (rand_num >= cumulative_prob).all() and (rand_num < cumulative_prob + prob).all():
#             return wset[i]
#         # Update cumulative probability
#         cumulative_prob += prob

#     # Fallback return: return the last element of wset
#     return wset[len(probabilities) - 1]

import random
import numpy as np
from scipy.sparse import dok_matrix

def prob_choose(weights, wset):
    # Convert weights to a dense array if it's a sparse matrix
    if isinstance(weights, dok_matrix):
        weights = weights.toarray().flatten()  # Convert to a dense 1D array

    # Normalize the weight vector (ensure weights is a NumPy array)
    weights = np.array(weights, dtype=float)  # Convert to a NumPy array
    probabilities = weights / np.sum(weights)  # Normalize the weights

    # Generate a random number between 0 and 1
    rand_num = random.random()

    # Initialize cumulative probability
    cumulative_prob = 0

    # Iterate over elements of the normalized weight vector
    for i, prob in enumerate(probabilities):
        # Check if the random number falls into the range
        if rand_num >= cumulative_prob and rand_num < cumulative_prob + prob:
            return wset[i]
        # Update cumulative probability
        cumulative_prob += prob

    # Fallback return: return the last element of wset
    return wset[len(probabilities) - 1]



def sample_n_words(text, widx, kscvidx, k, stoch, word_set, n):
    """
    Samples `n` words using `sample_next_word` and appends them to the input text.

    Args:
        text (list): A list of initial words.
        widx (dict): Dictionary mapping words to their indices.
        kscvidx (dict): Dictionary mapping k-sequences to their indices.
        k (int): Length of k-sequences.
        stoch (scipy.sparse.dok_matrix or np.ndarray): Stochastic matrix.
        word_set (list): List of all possible words to sample from.
        n (int): Number of words to sample.

    Returns:
        str: The final text after appending `n` sampled words.
    """
    # Start with the initial text joined as a string
    # joined_text = " ".join(text)
    joined_text = " ".join(text[-k:])
    print(f"joined_text: {joined_text}")

    for i in range(n):
        # Get the probabilities for the next word based on the last k-sequence
        probs = sample_next_word(text, widx, kscvidx, k, stoch)

        print(f"joined_text: {joined_text}")

        # if probs == []:
        #     return joined_text

        # Choose the next word using the probabilities
        next_word = prob_choose(probs, word_set)

        if text and text[-1] == next_word:
            print(f"Skipping word '{next_word}' as it is the same as the last word.")
            i = i + 1
            print(f"i: {i}  n: {n}")
            next_word = prob_choose(probs, word_set)
            continue

        # Append the next word to the joined_text
        joined_text += f" {next_word}"

        # Split the joined_text into words for further processing
        text = joined_text.split(" ")

    return joined_text

    # max_retries = n

    # for _ in range(n):
    #     # Get the probabilities for the next word based on the last k-sequence
    #     probs = sample_next_word(text, widx, kscvidx, k, stoch)

    #     # Choose the next word using the probabilities
    #     next_word = prob_choose(probs, word_set)

    #     # Retry to avoid duplicates, up to max_retries
    #     retries = 0
    #     while text and text[-1] == next_word and retries < max_retries:
    #         print(f"Retrying: Skipping word '{next_word}' as it is the same as the last word.")
    #         next_word = prob_choose(probs, word_set)
    #         retries += 1

    #     # If retries exceeded, accept the duplicate and warn
    #     if retries == max_retries:
    #         print(f"Max retries reached. Adding word '{next_word}' even though it is a duplicate.")

    #     # Append the next word to the joined_text
    #     joined_text += f" {next_word}"

    #     # Split the joined_text into words for further processing
    #     text = joined_text.split(" ")

    # return joined_text

