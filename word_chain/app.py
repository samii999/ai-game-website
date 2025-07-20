from flask import Blueprint, render_template, request, redirect, url_for
from .game import WordChainGame
import time

# Blueprint for modular integration
word_chain_bp = Blueprint('word_chain', __name__, template_folder='templates', static_folder='static')

# Create a single instance of the game
game = WordChainGame()

@word_chain_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action", "play")

        if action == "reset":
            game.reset_game()
            return redirect(url_for('word_chain.index'))

        elif action == "pause":
            is_paused = game.toggle_pause()
            timer_value = int(request.form.get("timer_value", 20))
            game.update_timer(timer_value)
            return redirect(url_for('word_chain.index'))

        elif action == "play":
            player_word = request.form.get("player_word", "").strip().lower()
            expected_start = request.form.get("last_letter")
            start_time = float(request.form.get("start_time", 0))
            current_time = time.time()

            # Check for time exceeded
            if start_time > 0 and current_time - start_time > game.timer_value:
                return render_template('time_exceeded.html',
                                       last_word=player_word,
                                       words_used=len(game.used_words))

            success, message, ai_word, is_duplicate = game.player_move(player_word, expected_start)

            if not success:
                if is_duplicate:
                    return render_template('duplicate_word.html',
                                           last_word=player_word,
                                           words_used=len(game.used_words))
                else:
                    return render_template('wrong_word.html',
                                           error_message=message,
                                           last_word=player_word,
                                           words_used=len(game.used_words))

    return render_template("index.html",
                           player_word="",
                           ai_word=game.last_ai_word if hasattr(game, 'last_ai_word') else "",
                           message="",
                           last_letter=game.last_letter if hasattr(game, 'last_letter') else "",
                           game_state={
                               "game_over": game.game_over,
                               "is_paused": game.is_paused,
                               "timer_value": game.timer_value
                           })
