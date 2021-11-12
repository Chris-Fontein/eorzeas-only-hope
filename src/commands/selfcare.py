#!/usr/bin/env python3
# vim: ts=4 expandtab

"""Self care commands"""

from __future__ import annotations

import random

import bot.commands

BIG_REMINDERS = [
    "take your meds",
    "check your medication",
]

REGULAR_THINGS = [
    "eat a meal",
    "have something to eat",
    "drink some water",
    "grab a refreshing drink",
    "stretch your body",
    "raise you heart rate",
]

DAILY_THINGS = [
    "reaching out to someone",
    "tend to a living/growing thing",
    "take a shower or bath",
    "clean one space or surface",
]

FORMATS = [
    "Looking after yourself is key: {reminder}, {regular}, and consider {daily}. 💜",
    "Looking after yourself is key: {reminder}, {regular}, and consider {daily}. 💜",
    "Looking after yourself is key: {reminder}, {regular}, and consider {daily}. 💜",
    "Time to {regular}? Maybe {daily}? Also, {reminder}. 🧡",
    "In the words of dear community member Baron Samedi: meds reminder for those who may need it.",
    "Remember to {reminder}",
]

CUTES = [
    "Apply Bun directly to forehead (https://i.redd.it/nn3q6ttz3qs21.jpg)",
    "Form a snugg pile!",
]


class SelfCare(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self) -> None:
        super().__init__("selfcare", SelfCare.message)

    @staticmethod
    def message() -> str:
        layout = random.choice(FORMATS)
        reminder = random.choice(BIG_REMINDERS)
        regular = random.choice(REGULAR_THINGS)
        daily = random.choice(DAILY_THINGS)

        return layout.format(reminder=reminder, regular=regular, daily=daily)


class BusCare(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self) -> None:
        super().__init__("buscare", BusCare.message)

    @staticmethod
    def message() -> str:
        return (
            "The Bus can wait! "
            "Get a drink, have some food, and get some rest. "
            "The VST will clip it for you. <3"
        )


class SelfCute(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "selfcute") -> None:
        super().__init__(command, SelfCute.message)

    @staticmethod
    def message() -> str:
        return random.choice(CUTES)


class SelfChair(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "selfchair") -> None:
        super().__init__(command, SelfChair.message)

    @staticmethod
    def message() -> str:
        return (
            "Be like a chair: back upright. weight firmly"
            "over your legs, well padded, comfy for a cat."
        )


class ShelfCare(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "shelfcare") -> None:
        super().__init__(command, ShelfCare.message)

    @staticmethod
    def message() -> str:
        return "Dust every three to four weeks. Do not overload."


class ShelfChair(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "shelfchair") -> None:
        super().__init__(command, ShelfChair.message)

    @staticmethod
    def message() -> str:
        return "...this is nonsense. Nonsense, I say!"


class ShelfCute(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "shelfcute") -> None:
        super().__init__(command, ShelfCute.message)

    @staticmethod
    def message() -> str:
        return "Don't put cuties on the shelf!"


class ShelfCat(bot.commands.SimpleCommand):
    """Reminds our dear friends to look after themselves."""

    def __init__(self, command: str = "shelfcat") -> None:
        super().__init__(command, ShelfCat.message)

    @staticmethod
    def message() -> str:
        return "Kitty! Kitty! Kitty on a shelf!"