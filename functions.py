import re
import numpy as np
from scipy.sparse import dok_matrix
import random

# Splits the input text into tokens, handling punctuation as separate tokens.
def split_input(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

# Checks if a character is a punctuation mark.
def is_punctuation(char):
    return char in '.,!?;:()[]{}\'"'

# Checks if a character is a letter or a number.
def is_letter_or_number(char):
    return char.isalnum()

# Finds and returns distinct words from a list of tokens.
def distinct_words(tokens):
    return sorted(set(tokens))

# Generates sequences of k consecutive elements from an array and joins them into strings.
def k_secv(A, k):
    n = len(A)
    B = []  # Initialize an empty list to hold the k-sequences

    for i in range(n - k + 1):
        # Extract the k consecutive strings
        strings = A[i : i + k]
        # Join the strings and add to the result
        B.append("".join(strings))

    return B

# Finds and returns distinct strings from a list of k-sequences.
def distinct_k_secv(cell_array):
    return sorted(set(cell_array))

# Creates a dictionary mapping distinct words to their indices.
def word_idx(distinct_wds):
    return {word: idx + 1 for idx, word in enumerate(distinct_wds)}

# Creates a dictionary mapping distinct k-sequences to their indices.
def k_secv_idx(distinct_k_sec):
    return {k_sec: idx + 1 for idx, k_sec in enumerate(distinct_k_sec)}

# Maps words to their indices.
def word_idx(words_set):
    return {word: idx + 1 for idx, word in enumerate(words_set)}

# Maps k-sequences to their indices.
def k_secv_idx(k_secv_set):
    return {k_sec: idx + 1 for idx, k_sec in enumerate(k_secv_set)}

# Builds the stochastic matrix.
def stochastic_matrix(k_secv_corpus, corpus_words, words_set, k_secv_set, k):
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

# Returns the probabilities (row of the stochastic matrix) corresponding 
# to the last k-sequence of the text.
def sample_next_word(text, widx, k_secv_idx, k, stoch):
    n = len(text)
    
    # Ensure text has at least k tokens
    if n < k:
        raise ValueError("Input text does not contain enough tokens for k-sequence.")

    # Concatenate the last k tokens to form k_secv_text
    strings = text[n - k:]
    k_secv_text = "".join(strings)

    # Handle missing keys
    if k_secv_text not in k_secv_idx:
        probs = []
        return probs

    # Retrieve the index of the k-sequence
    i = k_secv_idx[k_secv_text]

    # Retrieve the row of the stochastic matrix
    probs = stoch[i - 1, :]
    return probs

# chooses the next word
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

# Samples `n` words using `sample_next_word` and appends them to the input text.
def sample_n_words(text, widx, kscvidx, k, stoch, word_set, n):
    # Start with the initial text joined as a string
    joined_text = " ".join(text[-k:])
    print(f"joined_text: {joined_text}")

    for i in range(n):
        # Get the probabilities for the next word based on the last k-sequence
        probs = sample_next_word(text, widx, kscvidx, k, stoch)

        print(f"joined_text: {joined_text}")

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
