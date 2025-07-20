from flask import Blueprint

word_chain_bp = Blueprint('word_chain', __name__, template_folder='templates', static_folder='static')

from . import app  # this will register routes
