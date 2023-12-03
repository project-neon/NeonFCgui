"""
Main body of code. Execute to start program.
"""

from app import App

class GUI(object):
    def __init__(self):
        self.app = App(self)
    
    def start(self):
        self.app.start()

gui = GUI()
gui.start()
