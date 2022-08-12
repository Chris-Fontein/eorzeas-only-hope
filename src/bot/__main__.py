#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Benedict Harcourt <ben.harcourt@harcourtprogramming.co.uk>
#
# SPDX-License-Identifier: BSD-2-Clause

"""Only Hope Bot"""

from __future__ import annotations

from typing import Any, Generator, List

import asyncio
import os
import signal
import yaml

from commands import (
    animals,
    order,
    minecraft,
    prosegen,
    selfcare,
    timekeeping,
    twitch as twitch_commands,
)

import eorzea
import eorzea.lodestone

import ffxiv_quotes

from eorzea.storage import SQLite
from bot import DiscordBot, TwitchBot
from bot.commands import Command, RateLimitCommand, RandomCommand, RegexCommand


def main() -> None:
    """Run the bots!"""

    prose_data = ffxiv_quotes.get_ffxiv_quotes("ALISAIE", "URIANGER")

    with SQLite("list.db") as storage:
        commands: List[Command] = [
            # Memes.
            order.TeamOrder(),
            order.TeamOrderBid(),
            order.TeamOrderDonate(),
            order.DesertBusOrder(),
            # Animals.
            RateLimitCommand(animals.Cat(), 2),
            RateLimitCommand(animals.Dog(), 2),
            RateLimitCommand(animals.Fox(), 2),
            RateLimitCommand(animals.Bun(), 2),
            RateLimitCommand(animals.Bird("bird"), 2),
            RateLimitCommand(animals.Bird("birb"), 2),
            RateLimitCommand(animals.Panda(), 2),
            # Minecraft.
            minecraft.Pillars(),
            minecraft.Stack(),
            minecraft.NetherLocation(),
            minecraft.OverworldLocation(),
            # Self care.
            selfcare.BadSelfCare(),
            # Final Fantasy XIV (characters).
            eorzea.OnlyHope(storage),
            eorzea.Party(storage),
            eorzea.Stats(storage),
            eorzea.lodestone.PlayerLookup(),
            prosegen.ProseGenCommand("alisaie", prose_data["ALISAIE"]),
            prosegen.ProseGenCommand("urianger", prose_data["URIANGER"]),
            # Fake / fun dates.
            RateLimitCommand(timekeeping.March(), 2),
            RateLimitCommand(timekeeping.BusIsComing(), 2),
            RateLimitCommand(timekeeping.BusStop(), 2),
            # Twitch commands for sugarsh0t.
            twitch_commands.SassPlan(),
            twitch_commands.Cardinal(),
        ]
        commands += list(load_commands_from_yaml())
        discord_commands: List[Command] = [eorzea.HopeAdder(storage)]

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, loop.stop)
        loop.add_signal_handler(signal.SIGTERM, loop.stop)

        with open("twitch.token", "rt", encoding="utf-8") as token_handle:
            [nick, token, *channels] = token_handle.read().strip().split("::")

        irc = TwitchBot(loop, token, nick, commands, channels)
        irc_task = loop.create_task(irc.connect(), name="irc")

        with open("discord.token", "rt", encoding="utf-8") as token_handle:
            token = token_handle.read().strip()

        if not token:
            raise Exception("Unable to load token from token file")

        discord = DiscordBot(loop, discord_commands + commands)
        discord_task = loop.create_task(discord.start(token), name="discord")

        try:
            print("Starting main loop")
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        loop.run_until_complete(irc.close())
        loop.run_until_complete(discord.close())
        loop.run_until_complete(irc_task)
        loop.run_until_complete(discord_task)
        loop.close()


def load_commands_from_yaml() -> Generator[Command, None, None]:
    cwd = os.curdir
    command_dir = os.path.join(cwd, "commands")

    for file in os.listdir(command_dir):
        path = os.path.join(command_dir, file)

        with open(path, "rb") as stream:
            for block in yaml.load_all(stream, yaml.CSafeLoader):
                yield from load_command(block)


def load_command(data: Any) -> Generator[Command, None, None]:
    if not isinstance(data, dict):
        return

    if "commands" in data:
        yield RandomCommand(
            data.get("commands", []), data.get("formats", []), data.get("args", {})
        )

    if "regexp" in data:
        if isinstance(data["regexp"], str):
            yield RegexCommand(data["regexp"], data.get("formats", []), data.get("args", {}))


if __name__ == "__main__":
    main()
