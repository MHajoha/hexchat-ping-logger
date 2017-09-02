# coding: utf8
"""
ping-logger.py - HexChat script which logs all pings to (mentions of) the user while they are marked away and prints
them out when the user is back.

Copyright (c) 2017 Maximilian "MHajoha" Haye.
All rights reserved.

HexChat is copyright (c) 2009-2014 Berke Viktor.
https://hexchat.github.io/
"""

from collections import namedtuple
from time import strftime

import hexchat

__module_name__ = "Ping Logger"
__module_version__ = "0.5-beta"
__module_description__ = "Logs pings (mentions of the user) whilst they are marked away."


mentions = list()
""" :var: List of all mentions, cleared when the user returns """

away = hexchat.get_info("away") is not None
""" :var: Whether or not the user is currently marked away """

Mention = namedtuple("Mention", ("timestamp", "sender", "message"))
""" :type: Simple data type to hold mention data """


def on_privmsg(word, word_eol, userdata):
    """
    Hook function, called upon PRIVMSG received by the server.
    Appends to `mentions` if the user is away and has been mentioned by another user.

    Official HexChat Python interface documentation: http://hexchat.readthedocs.io/en/latest/script_python.html
    """
    global away
    global mentions

    if away and hexchat.get_info("nick") in word_eol[3].lstrip(":"):
        mentions.append(Mention(strftime("%H:%M:%S"), word[0][1:word[0].find("!")], word_eol[3].lstrip(":")))


def on_away(word, word_eol, userdata):
    """ Hook function, called upon usage of the IRC command /away. """
    global away

    away = True


def on_back(word, word_eol, userdata):
    """
    Hook function, called upon usage of the IRC command /back.
    Sets `away` to False and prints all logged mentions, then clears `mentions` list.
    """

    global away
    global mentions

    if away:
        if len(mentions) > 0:
            print("\nYou were pinged {0} time(s) while you were away.".format(len(mentions)))
            print()
            for mention in mentions:
                print("{0.timestamp}\t\00302{0.sender}: \003{0.message}".format(mention))

            mentions.clear()
        else:
            print("You were not pinged while you were away.")

        away = False


hexchat.hook_server("PRIVMSG", on_privmsg)
hexchat.hook_server("306", on_away)         # Marked as away
hexchat.hook_server("305", on_back)         # No longer marked as away

print(__module_name__ + " loaded successfully.")
