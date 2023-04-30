import os
import numpy as np
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the LSTM model
lstm_model = load_model('models/lstm_model.h5')

# Function to preprocess the essay text
def preprocess_essay(essay, max_len=500):
    # Tokenize, pad, and preprocess the essay here
    # This function should return a sequence of token ids, based on your text preprocessing
    # Here's a simple example, replace it with your actual preprocessing
    token_ids = [ord(c) for c in essay]
    padded_token_ids = pad_sequences([token_ids], maxlen=max_len, padding='post')
    return padded_token_ids

def parse_rubric(file_path):
    # Assuming the rubric is stored in JSON format, parse it and return the parsed data
    # Modify this function to support other formats (CSV, XML) if necessary
    with open(file_path, 'r') as file:
        rubric = json.load(file)
    return rubric

def calculate_consensus_score(peer_marks):
    # Convert the peer marks to float and calculate the consensus score
    # You can use different approaches to calculate the consensus score (e.g., mean, median)
    peer_marks_float = [float(mark) for mark in peer_marks]
    consensus_score = sum(peer_marks_float) / len(peer_marks_float)
    return consensus_score

def get_essay_score(essay, rubric_file_path, peer_marks):
    # Preprocess the essay
    essay_preprocessed = preprocess_essay(essay)
    
    # Parse the marking rubric
    rubric = parse_rubric(rubric_file_path)

    # Calculate the consensus score using peer-assessed marks
    consensus_score = calculate_consensus_score(peer_marks)

    # Get the score from the LSTM model
    model_score = lstm_model.predict(essay_preprocessed)[0][0]

    # Combine the LSTM model score with the consensus score (e.g., weighted average)
    # You can use different approaches to combine the scores
    final_score = 0.7 * model_score + 0.3 * consensus_score
    return round(final_score, 2)



