import os
from .trie import Trie
from flask import render_template

class WordChainGame:
    def __init__(self, words_file="words.txt"):
        self.trie = Trie()
        self.used_words = set()
        self.game_over = False
        self.is_paused = False
        self.timer_value = 20
        self.last_ai_word = ""
        self.last_letter = ""
        self.time_exceeded = False
        self.wrong_word = False
        self.load_words(words_file)

    def load_words(self, filename):
        base_dir = os.path.dirname(__file__)  # Path to 'word_chain/' directory
        file_path = os.path.join(base_dir, filename)

        with open(file_path, "r") as f:
            for word in f:
                word = word.strip().lower()
                if len(word) > 2:
                    self.trie.insert(word)

    def reset_game(self):
        self.used_words.clear()
        self.game_over = False
        self.is_paused = False
        self.timer_value = 20
        self.last_ai_word = ""
        self.last_letter = ""
        self.time_exceeded = False
        self.wrong_word = False

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

    def update_timer(self, value):
        self.timer_value = value

    def handle_time_exceeded(self):
        self.game_over = True
        self.time_exceeded = True
        return "Game Over! Time limit exceeded!"

    def handle_wrong_word(self, reason):
        self.game_over = True
        self.wrong_word = True
        return f"Game Over! {reason}"

    def is_valid_word(self, word, expected_start=None):
        if self.game_over:
            return False, "Game is over! Please restart.", False
        if self.is_paused:
            return False, "Game is paused!", False
        
        word = word.lower()
        if word in self.used_words:
            return False, "Word already used!", True
        if expected_start and not word.startswith(expected_start):
            return False, self.handle_wrong_word(f"Word must start with '{expected_start}'"), False
        words_found = self.trie.find_words(word[:3])
        if word not in words_found:
            return False, self.handle_wrong_word("Word not found in dictionary"), False
        return True, "Valid word!", False

    def get_ai_response(self, last_letter):
        if self.game_over or self.is_paused:
            return None
        queue = self.trie.find_words(last_letter)
        for word in queue:
            if word not in self.used_words:
                self.used_words.add(word)
                self.last_ai_word = word
                self.last_letter = word[-1]
                return word
        return None

    def player_move(self, word, expected_start=None):
        word = word.lower()
        valid, msg, is_duplicate = self.is_valid_word(word, expected_start)
        if not valid:
            return False, msg, None, is_duplicate
        self.used_words.add(word)
        self.last_letter = word[-1]
        ai_word = self.get_ai_response(word[-1])
        return True, f"AI played: {ai_word}" if ai_word else "AI has no move!", ai_word, False
