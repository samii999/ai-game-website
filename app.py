from flask import Flask
from word_chain.app import word_chain_bp

app = Flask(__name__)

# Register the blueprint under '/word-chain'
app.register_blueprint(word_chain_bp, url_prefix='/word-chain')

if __name__ == "__main__":
    app.run(debug=True)
