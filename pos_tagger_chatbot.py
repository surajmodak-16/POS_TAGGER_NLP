import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("POS_dataset.csv")
    pos_lookup = dict(zip(df['fake'].str.lower(), df['JJ']))
    return pos_lookup

# POS Tag descriptions
pos_full_names = {
    "N_NNP": "Proper Noun",
    "N_NN": "Common Noun",
    "PR_PRP": "Pronoun",
    "V_VM": "Main Verb",
    "V_VP": "Past Verb",
    "V_BG": "Gerund/Verb-ing",
    "JJ": "Adjective",
    "RP_NEG": "Negative Particle",
    "RD_PUNC": "Punctuation",
    "UNK": "Unknown or data not available"
}

# POS Tagging Function with fallback

def pos_tagger_bot(sentence, pos_lookup):
    words = sentence.lower().split()
    tagged = []
    for word in words:
        tag = pos_lookup.get(word)
        if not tag:
            if word.endswith('ing'):
                tag = 'V_BG'
            elif word.endswith('ed'):
                tag = 'V_VP'
            elif word.istitle():
                tag = 'N_NNP'
            else:
                tag = 'UNK'
        tagged.append((word, tag))
    return tagged

# Streamlit App UI
st.title("Mix Code POS Tagger")
st.write("Enter a sentence, and I'll tag each word with its Part of Speech.")

# Load POS data
pos_lookup = load_data()

# User Input
user_input = st.text_input("You:", "")
if user_input:
    result = pos_tagger_bot(user_input, pos_lookup)
    st.write("### POS Tags:")
    for word, tag in result:
        full_name = pos_full_names.get(tag, "Unknown or data not available")
        st.write(f"- **{word}** → `{tag}` ({full_name})")
