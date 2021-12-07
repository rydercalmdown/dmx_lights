import os
import logging


class Fixture:
    """Class for representing a particular DMX fixture"""

    def __init__(self, **kwargs):
        """Set up the particular fixture"""
        self.dmx_id = kwargs['id']
        logging.debug(f'instantiating fixture {self.dmx_id}')
        self.dmx_controller = kwargs['controller']
        self.rgb = [0, 0, 0]

    def _update_dmx_controller(self):
        """Updates the DMX controller"""
        self.dmx_controller.set_fixture_colour(self.dmx_id, self.rgb)

    def set_colour(self, rgb):
        """Sets the RGB colour of the lights"""
        self.rgb = rgb
        self._update_dmx_controller()

    def clear(self):
        """Clears the fixture - turns it off"""
        self.rgb = [0, 0, 0]
        self._update_dmx_controller()

    def set_white(self):
        """Sets the fixture to white with full intensity"""
        self.rgb = [255, 255, 255]
        self._update_dmx_controller()
