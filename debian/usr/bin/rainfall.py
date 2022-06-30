#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import random
from typing import List
from argparse import Namespace
import curses
from parse_arguments import parse_args
from raindrop import Raindrop


class RainFall:
    DROPSHAPES = ["|", "│", "┃", "╽", "╿", "║", "┆", "┇", "┊", "┋", "╵",
                  "╹",
                  "╻"]
    COLORS = {
        "black": curses.COLOR_BLACK,
        "red": curses.COLOR_RED,
        "green": curses.COLOR_GREEN,
        "yellow": curses.COLOR_YELLOW,
        "blue": curses.COLOR_BLUE,
        "magenta": curses.COLOR_MAGENTA,
        "cyan": curses.COLOR_CYAN,
        "white": curses.COLOR_WHITE,
        "b_black": curses.COLOR_BLACK + curses.A_BOLD,
        "b_red": curses.COLOR_RED + curses.A_BOLD,
        "b_green": curses.COLOR_GREEN + curses.A_BOLD,
        "b_yellow": curses.COLOR_YELLOW + curses.A_BOLD,
        "b_blue": curses.COLOR_BLUE + curses.A_BOLD,
        "b_magenta": curses.COLOR_MAGENTA + curses.A_BOLD,
        "b_cyan": curses.COLOR_CYAN + curses.A_BOLD,
        "b_white": curses.COLOR_WHITE + curses.A_BOLD,
    }

    def __init__(self, intensity: int, drop_colors: List[str] = None):
        """Creates a rainfall effect on the CLI.

        Args:
            intensity: The intensity of the raindrops. Refers to the number of
                raindrops that will be created at each frame.
            drop_colors: The colors of the raindrops.
        """
        for color in drop_colors:
            assert color in self.COLORS, f"{color} is not a valid color"

        self.stdscr = curses.initscr()

        self.height, self.width = self.stdscr.getmaxyx()

        self.weather = 0
        self.rainfall = []

        self.intensity = intensity
        self.drop_colors = drop_colors

    def start_rain(self):
        """Starts the rain animation."""
        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()
        self.stdscr.keypad(True)

        self.new_drops()

        try:
            while True:
                self.rain()
                time.sleep(0.08)
                self.weather_forecast()

        except KeyboardInterrupt:
            pass
        finally:
            self.stdscr.erase()
            curses.curs_set(1)
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.endwin()

    def new_drops(self):
        for i in range(self.intensity):
            shape = random.choice(self.DROPSHAPES)
            color = random.choice(self.drop_colors)
            self.rainfall.append(
                Raindrop(x=random.randint(0, self.width - 2), y=0,
                         drop_str=shape,
                         color=color)
            )

    def rain(self):
        """Creates new raindrops and moves all raindrops down the screen."""
        # Clear out the screen
        self.stdscr.erase()
        new_raindrops = []
        # Go through every raindrop
        for raindrop in self.rainfall:
            # First remove the raindrop from the screen
            # Move every raindrop down by 1
            raindrop.y += 1
            if raindrop.y == self.height - 1:
                # If the raindrop is off the screen, remove it
                continue

            if raindrop.y == self.height - 2:
                # If the raindrop is at the bottom of the screen, make it splash
                raindrop.drop_str = "o"
                self.stdscr.addstr(raindrop.y, raindrop.x,
                                   raindrop.drop_str)
            else:
                self.stdscr.addstr(raindrop.y, raindrop.x,
                                   raindrop.drop_str)
            new_raindrops.append(raindrop)

        # Draw the raindrops that are still on the screen
        self.stdscr.refresh()
        self.rainfall = new_raindrops

        self.new_drops()

    def weather_forecast(self):
        self.weather += 1
        if self.weather == 100:
            self.weather = 0
            self.intensity += random.choice([-1, 1])

            # Clip intensity between 1, 10
            self.intensity = max(1, min(10, self.intensity))


def main(args: Namespace):
    colors = args.COLORS if not args.monochrome else None
    rainfall = RainFall(args.intensity, colors)
    rainfall.start_rain()


if __name__ == '__main__':
    main(parse_args())
