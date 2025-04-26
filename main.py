from Gui import *
from AppController import *

user_config = password_window()

if user_config:
    initialize_app(user_config)
    # start_network()