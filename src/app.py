import os
import logging
import time
import threading
import random

from dmx_controller import DmxController
from fixture import Fixture

from flask import Flask, jsonify
import requests


class DmxLightPiController:
    """Main module for DMX lighting controller"""

    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    GREEN = [0, 255, 0]
    RED = [255, 0, 0]
    BLUE = [0, 0, 255]
    PURPLE = [255, 0, 255]
    YELLOW = [255, 255, 0]
    AQUA = [0, 255, 255]

    def __init__(self):
        """Setup"""
        logging.info('Creating controller')
        self._setup_dmx_controller()
        self._create_fixtures()

    def _shutdown(self):
        """Shuts down the module"""
        self.blackout()
        time.sleep(0.2)
        self.dmx_c.terminate()

    def _setup_dmx_controller(self):
        """Setup and start the DMX controller"""
        self.dmx_c = DmxController()
        self.dmx_c.run()

    def _create_fixtures(self):
        """Defines all available fixtures"""
        self.fixtures = [
            Fixture(id=0, controller=self.dmx_c),
        ]

    def set_all_fixtures(self, rgb):
        """Sets all available fixtures to a rgb value"""
        logging.debug(f'Setting all fixtures to {rgb}')
        for f in self.fixtures:
            f.set_colour(rgb)

    def blackout(self):
        """Blackout all fixtures"""
        self.set_all_fixtures(self.BLACK)

    def test(self):
        """Run internal testing"""
        logging.info('Testing controller')
        test_colours = {
            'white': self.WHITE,
            'red': self.RED,
            'green': self.GREEN,
            'blue': self.BLUE,
            'yellow': self.YELLOW,
            'aqua': self.AQUA,
            'purple': self.PURPLE,
        }
        for i, v in test_colours.items():
            logging.info(f'Testing colour: {i}')
            self.set_all_fixtures(v)
            time.sleep(0.3)
        self.blackout()

    def _flask_master_thread(self):
        """Flask master thread"""
        self.flask_app = Flask(__name__)

        @self.flask_app.route("/")
        def main():
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/white/")
        def wash_white():
            self.set_all_fixtures(self.WHITE)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/blackout/")
        def blackout():
            self.blackout()
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/red/")
        def wash_red():
            self.set_all_fixtures(self.RED)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/green/")
        def wash_green():
            self.set_all_fixtures(self.GREEN)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/blue/")
        def wash_blue():
            self.set_all_fixtures(self.BLUE)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/aqua/")
        def wash_aqua():
            self.set_all_fixtures(self.AQUA)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/purple/")
        def wash_purple():
            self.set_all_fixtures(self.PURPLE)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/yellow/")
        def wash_yellow():
            self.set_all_fixtures(self.YELLOW)
            return jsonify({'status': 'ok'})

        @self.flask_app.route("/wash/random/")
        def wash_random():
            rgb = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            self.set_all_fixtures(rgb)
            return jsonify({'status': 'ok'})

        self.flask_app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

    def _start_flask(self):
        """Starts the flask application in a daemon thread"""
        logging.info('Starting flask thread')
        self.flask_thread = threading.Thread(name='flask_thread', target=self._flask_master_thread)
        self.flask_thread.setDaemon(True)
        self.flask_thread.start()

    def run(self):
        """Run controller standard operation"""
        logging.info('Running controller')
        logging.info('Starting Flask')
        self._start_flask()
        while True:
            pass

    def start(self):
        """Start the controller"""
        logging.getLogger().setLevel(logging.INFO)
        try:
            self.test()
            self.run()
        except KeyboardInterrupt:
            logging.info('Exiting')
            self._shutdown()


if __name__ == '__main__':
    dlpc = DmxLightPiController()
    dlpc.start()
