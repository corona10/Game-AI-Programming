#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.
import window                   # Terminal input and dispatch
import nltk.chat
from multiprocessing import Queue
import subprocess
from threading import Thread, Lock
import threading
import time

lock = threading.Lock()

AGENT_RESPONSES = [
  (r'You are (worrying|scary|disturbing)',    # Pattern 1.
    ['Yes, I am %1.',                         # Response 1a.
     'Oh, sooo %1.']),

  (r'Are you ([\w\s]+)\?',                    # Pattern 2.
    ["Why would you think I am %1?",          # Response 2a.
     "Would you like me to be %1?"]),

  (r'',                                       # Pattern 3. (default)
    ["Is everything OK?",                     # Response 3a.
     "Can you still communicate?"])
]

global q
q = Queue()

class HAL9000(object):
    
    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'unknown'
        self.is_first = True
        self.chatbot = nltk.chat.Chat(AGENT_RESPONSES, nltk.chat.util.reflections )

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        if(self.is_first):
            self.terminal.log("Nice to meet you! This is HAL.", align='right', color='#00805A')
            self.is_first = False
            q.put("Nice to meet you! This is HAL.")

        if(evt.text == 'Where am I?'):
            self.terminal.log('You are in `{}`'.format(self.location), align='right', color='#00805A' )
            q.put('You are in `{}`'.format(self.location))
        else:
            repr = self.chatbot.respond(format(evt.text))
            self.terminal.log(repr, align ='right', color='#00805A' )
            q.put(repr)



    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self.terminal.log('', align='center', color='#404040')
            self.terminal.log('\u2014 Now in the {}. \u2014'.format(evt.text[9:]), align='center', color='#404040')
            self.location = format(evt.text[9:])
            q.put('\u2014 Now in the {}. \u2014'.format(evt.text[9:]))
        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')
            q.put('Command `{}` unknown.'.format(evt.text))
            q.put("I'm afraid I can't do that.")

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass

class speaker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if(q.empty() == False ):
                lock.acquire()
                subprocess.call(['/usr/bin/say', '-v', 'Alex', q.get()])
                lock.release()

    def update(self, _):
        pass

class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window)
        self.speak = speaker()
        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.start()
        self.speak.setDaemon(True)
        self.speak.start()
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
