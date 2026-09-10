import collections
import re
from shared.contracts import EvidenceCandidate

FUNCTION_WORDS = {"the", "and", "a", "of", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as", "with", "his", "they", "i"}

def extract_style_features(text: str) -> dict:
    if not text:
        return {"function_words": {}, "char_ngrams": {}}
        
    # Function words frequency
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = collections.Counter(words)
    func_freq = {w: word_counts[w] for w in FUNCTION_WORDS if w in word_counts}
    
    # Character 3-grams frequency
    text_clean = re.sub(r'\s+', ' ', text)
    ngrams = [text_clean[i:i+3] for i in range(len(text_clean)-2)]
    ngram_counts = dict(collections.Counter(ngrams).most_common(50)) # top 50 to keep it small
    
    return {
        "function_words": func_freq,
        "char_ngrams": ngram_counts
    }
