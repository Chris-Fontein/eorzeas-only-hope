#!/usr/bin/env python3
# vim: ts=4 expandtab

"""Commands specifically for the sugarsh0t twitch channel"""

from __future__ import annotations

import abc

import bot.commands
from bot.twitch import TwitchMessageContext


class TwitchCommand(bot.commands.Command):
    async def process(self, context: bot.commands.MessageContext, message: str) -> bool:
        if not isinstance(context, TwitchMessageContext):
            return False

        if str(context.channel()) != "sugarsh0t":
            return False

        return await self.respond(context, message)

    @abc.abstractmethod
    async def respond(self, context: TwitchMessageContext, message: str) -> bool:
        pass


class Plan(TwitchCommand):
    def matches(self, message: str) -> bool:
        return message.startswith("!plan")

    async def respond(self, context: TwitchMessageContext, message: str) -> bool:
        await context.reply_all(
            "Dice Forge is off, we'll spend the next 40 minutes coming up with a cunning !plan -- Elrad"
        )

        return True


class SassPlan(TwitchCommand):
    def matches(self, message: str) -> bool:
        return (
            message.startswith("!sassplan")
            or message.startswith("!flan")
            or message.startswith("!sassflan")
        )

    async def respond(self, context: TwitchMessageContext, message: str) -> bool:
        await context.reply_all("This ain't a Serge stream, @" + context.sender())

        return True
