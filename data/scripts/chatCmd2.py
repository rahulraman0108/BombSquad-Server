# -*- coding: utf-8 -*-
import bs
import bsInternal
import bsUtils
import json


class chatOptions(object):
    def __init__(self, nick, msg):
        """For help, stats and other public commands"""
        m = msg.split(' ')[0]  # command
        a = msg.split(' ')[1:]  # arguments

        activity = bsInternal._getForegroundHostActivity()
        with bs.Context(activity):
            if m == "/help":
                partyName = "Cobra |EPICS|"
                bsInternal._chatMessage(partyName + " party\'s help message:")
                bsInternal._chatMessage("Party by TheGreat.")
                if ("rules" not in a) and ("stats" not in a):
                    bsInternal._chatMessage("Send `/help <command>` to get help of a particular command.")
                    bsInternal._chatMessage("Send `/rules` to get rules of playing in this party.")
                    bsInternal._chatMessage("Send `/stats` to get your stats in this party.")
                    bsInternal._chatMessage("Send `/stats <player i digit ID>` to get someone\'s stats of this party.")
                if "stats" in a:
                    bsInternal._chatMessage("This command is used to get a player\'s stats in this party.")
                    bsInternal._chatMessage("Syntax: `/stats <player\'s i digit ID (optional)>`.")
                if "rules" in a:
                    bsInternal._chatMessage("This command is used to get the rules of playing in this party.")
                    bsInternal._chatMessage("Syntax: `/rules`.")
            elif m == '/stats':
                if a == []:
                    for player in activity.players:
                        if player.getName().encode('utf-8').find(
                                nick.encode('utf-8').replace('...', '').replace(':', '')) != -1:
                            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
                            pats = json.loads(f.read())
                            if player.get_account_id() in pats:
                                bsInternal._chatMessage(("Player: " + player.getName() + ", this season's rank: " +
                                                         pats[str(player.get_account_id())]["rank"]))
                                bsInternal._chatMessage(("Games played: " + pats[str(player.get_account_id())][
                                    "games"] + ", Total scores: " + pats[str(player.get_account_id())]["scores"]))
                                bsInternal._chatMessage(("Kills: " + pats[str(player.get_account_id())][
                                    "kills"] + ",Deaths: " + pats[str(player.get_account_id())]["deaths"]))
                            else:
                                bsInternal._chatMessage(
                                    "The player " + str(player.getName()) + " is not yet registered")
                else:
                    player = activity.players[int(a[0])]
                    f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
                    pats = json.loads(f.read())
                    if player.get_account_id() in pats:
                        bsInternal._chatMessage(("Player: " + player.getName() + ", this season's rank: " +
                                                 pats[str(player.get_account_id())]["rank"]))
                        bsInternal._chatMessage(("Games played: " + pats[str(player.get_account_id())][
                            "games"] + ", Total scores: " + pats[str(player.get_account_id())]["scores"]))
                        bsInternal._chatMessage(("Kills: " + pats[str(player.get_account_id())][
                            "kills"] + ",Deaths: " + pats[str(player.get_account_id())]["deaths"]))
                    else:
                        bsInternal._chatMessage(
                            "The player " + str(player.getName()) + " is not yet registered")
            elif m == '/rules':
                bsInternal._chatMessage("1) Never betray teammates")
                bsInternal._chatMessage("2) Do not vote kick without reason")
                bsInternal._chatMessage("3) Do not abuse in chat")
                bsInternal._chatMessage("Disobedience of any rule will result in kick and might be ban")
                bsInternal._chatMessage("Report any disobedience in the discord server:")
                bsInternal._chatMessage("Invite link: https://discord.gg/")


def cmd(msg):
    if bsInternal._getForegroundHostActivity() is not None:
        n = msg.split(': ')
        chatOptions(n[0], n[1])
