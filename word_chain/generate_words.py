import nltk
nltk.download('words')
from nltk.corpus import words

word_list = words.words()
filtered_words = set(w.lower() for w in word_list if w.isalpha() and len(w) > 2)

with open("words.txt", "w") as f:
    for word in sorted(filtered_words):
        f.write(word + "\n")

print(f"✅ Saved {len(filtered_words)} words to words.txt")
