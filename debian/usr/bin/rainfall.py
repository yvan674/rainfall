#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import os
from typing import List
from argparse import ArgumentParser, ArgumentTypeError, Action, Namespace


COLORS = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "reset": "\u001b[0m",

    "b_black": "\u001b[30;1m",
    "b_red": "\u001b[31;1m",
    "b_green": "\u001b[32;1m",
    "b_yellow": "\u001b[33;1m",
    "b_blue": "\u001b[34;1m",
    "b_magenta": "\u001b[35;1m",
    "b_cyan": "\u001b[36;1m",
    "b_white": "\u001b[37;1m",

    "Reset": "\u001b[0m",
}


def range_type(astr, minimum=1, maximum=10):
    value = int(astr)
    if minimum <= value <= maximum:
        return value
    else:
        raise ArgumentTypeError(f'value not in range [{min}-{max}]')


class ValidateColors(Action):
    def __call__(self, parser, args, values, option_string=None):
        valid_colors = list(COLORS.keys())
        chosen_colors = values
        for chosen_color in chosen_colors:
            if chosen_color not in valid_colors:
                raise ValueError(f"Invalid color: {chosen_color}.")
        setattr(args, self.dest, chosen_colors)


def parse_args():
    p = ArgumentParser(description="Creates a rainfall effect in the CLI.")

    p.add_argument('COLORS', nargs='*', action=ValidateColors,
                   default=["blue", "b_blue"],
                   help="Choose which COLORS to use.")
    p.add_argument('--monochrome', '-m', action='store_true',
                   help="Enables monochrome mode.")

    p.add_argument('--intensity', '-i', type=range_type,
                   default=1,
                   help="Intensity of the rainfall in the range of "
                        "[%(minimum)d-%(maximum)d]. Default is %(default).")
    return p.parse_args()


class RainFall:
    DROPSHAPES = ["|", "│", "┃", "╽", "╿", "║", "┆", "┇", "┊", "┋", "╵",
                  "╹",
                  "╻"]

    def __init__(self, intensity: int, drop_colors: List[str],
                 monochrome: bool):
        """Creates a rainfall effect on the CLI."""
        size = os.get_terminal_size()
        self.xmax = size.columns
        self.ymax = int(size.lines)

        self.weather = 0
        self.rainfall = []


        self.intensity = intensity
        self.drop_colors = drop_colors
        self.monochrome = monochrome

    def start_rain(self):
        print('\033[?25l', end="")  # hides the cursor
        self.new_drop()

        try:
            while True:
                self.rain()
                time.sleep(0.08)
                self.clear_screen()
                self.weather_forecast()

        except KeyboardInterrupt:
            self.clear_screen()
            print('\033[?25h', end="")  # makes cursor visible again

    def rain(self):
        # iterate over every line
        for i in range(self.ymax):
            line = " " * self.xmax

            # to avoid splicing of ansi codes, splice in the drops from the
            # end of the line
            this_line_raindrops = [raindrop
                                   for raindrop in self.rainfall
                                   if raindrop["y"] == i]
            this_line_raindrops.sort(key=lambda y: y["x"])
            this_line_raindrops.reverse()

            # insert new drops and shift existing drops
            for raindrop in this_line_raindrops:
                x = raindrop["x"]
                line = line[:x] + raindrop["shape"] + line[x:]

            print(line)

        # update raindrop positions
        for raindrop in self.rainfall:
            raindrop["y"] += 1

            # once a raindrop reaches the ground, they splash
            if raindrop["y"] > self.ymax - 2:
                raindrop["shape"] = self.colorize_string(
                    "o", random.choice(self.drop_colors)
                )

            # raindrops outside the window evaporate
            if raindrop["y"] > self.ymax:
                self.rainfall.remove(raindrop)

        self.new_drop()

    def weather_forecast(self):
        self.weather += 1
        if self.weather == 100:
            self.weather = 0
            self.intensity += random.choice([-1, 1])

            # Clip intensity between 1, 10
            self.intensity = max(1, min(10, self.intensity))

    def colorize_string(self, string, color):
        if self.monochrome:
            return string
        else:
            return COLORS[color] + string + COLORS["Reset"]

    def new_drop(self):
        for i in range(self.intensity):
            shape = random.choice(self.DROPSHAPES)
            color = random.choice(self.drop_colors)

            raindrop = {
                "shape": self.colorize_string(shape, color),
                "x": random.randint(0, self.xmax),
                "y": 0,
            }
            self.rainfall.append(raindrop)

    @staticmethod
    def clear_screen():
        print("\033[2J")  # erase saved lines
        print("\033[3J")  # erase entire screen
        print("\033[H")  # moves cursor to home position


def main(args: Namespace):
    rainfall = RainFall(args.intensity, args.COLORS, args.monochrome)
    rainfall.start_rain()


if __name__ == '__main__':
    main(parse_args())
