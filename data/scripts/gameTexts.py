# -*- coding: utf-8 -*-
import bs
import settings
import random
import json


class TopCornerScores(bs.Actor):
    def __init__(self):
        bs.Actor.__init__(self)
        self.players = settings.return_players_yielded(bs)
        player = next(self.players)
        aid = player.get_account_id()
        try:
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/stats.json", "r")
        except IOError:
            pass
        else:
            self.stats = json.loads(f.read())
            f.close()
            if str(aid) in self.stats:
                player_stat = self.stats[str(aid)]
                text = str(player.getName(full=True).encode("utf-8")) + "\'s stats of the season:\n" + str(
                    player_stat["scores"]) + " scores, " + str(
                    player_stat["kills"]) + " kills, " + str(player_stat["deaths"]) + " deaths."
            else:
                text = str(player.getName(full=True).encode("utf-8")) + " is not registered"
            self.node = bs.newNode('text',
                                   attrs={'text': str(text),
                                          'scale': 1.0,
                                          'maxWidth': 0,
                                          'position': (250, 650),
                                          'shadow': 0.5,
                                          'color': (
                                              (0 + random.random() * 1.0), (0 + random.random() * 1.0),
                                              (0 + random.random() * 1.0)),
                                          'flatness': 0.5,
                                          'hAlign': 'center',
                                          'vAttach': 'bottom'})
            bs.animate(self.node, 'opacity', {0: 0.0, 1000: 1.0, 5000: 1.0, 6000: 0.0}, loop=True)
            self.textChangeTimer = bs.Timer(6000, self.nextText, repeat=True)

    def nextText(self):
        try:
            player = next(self.players)
            aid = player.get_account_id()
            if str(aid) in self.stats:
                player_stat = self.stats[str(aid)]
                text = str(player.getName(full=True).encode("utf-8")) + "\'s stats of the season:\n" + str(
                    player_stat["scores"]) + " scores, " + str(
                    player_stat["kills"]) + " kills, " + str(player_stat["deaths"]) + " deaths."
            else:
                text = str(player.getName(full=True).encode("utf-8")) + " is not registered"
        except StopIteration:
            self.players.close()
            self.players = settings.return_players_yielded(bs)
            try:
                player = next(self.players)
            except StopIteration:
                self.node.text = ""
                return
            aid = player.get_account_id()
            if str(aid) in self.stats:
                player_stat = self.stats[str(aid)]
                text = str(player.getName(full=True).encode("utf-8")) + "\'s stats of the season:\n" + str(
                    player_stat["scores"]) + " scores, " + str(
                    player_stat["kills"]) + " kills, " + str(player_stat["deaths"]) + " deaths."
            else:
                text = str(player.getName(full=True).encode("utf-8")) + " is not registered"
        self.node.text = str(text)
        self.node.color = ((0 + random.random() * 1.0), (0 + random.random() * 1.0), (0 + random.random() * 1.0))

    def handleMessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            try:
                self.node.delete()
                self.textChangeTimer = None
            except:
                pass
        else:
            bs.Actor.handleMessage(self, msg)

    def delete(self):
        self.handleMessage(bs.DieMessage())


class BottomTexts(bs.Actor):
    def __init__(self):
        bs.Actor.__init__(self)
        self.texts = settings.return_yielded_game_texts()
        text = next(self.texts)
        self.node = bs.newNode('text',
                               attrs={'text': str(text),
                                      'scale': 1.2,
                                      'maxWidth': 0,
                                      'position': (0, 137),
                                      'shadow': 0.5,
                                      'color': (
                                          (0 + random.random() * 1.0), (0 + random.random() * 1.0),
                                          (0 + random.random() * 1.0)),
                                      'flatness': 0.5,
                                      'hAlign': 'center',
                                      'vAttach': 'bottom'})
        bs.animate(self.node, 'opacity', {0: 0.0, 500: 1.0, 4500: 1.0, 5000: 0.0}, loop=True)
        self.textChangeTimer = bs.Timer(5000, self.nextText, repeat=True)

    def nextText(self):
        try:
            text = next(self.texts)
        except StopIteration:
            self.texts.close()
            self.texts = settings.return_yielded_game_texts()
            text = next(self.texts)
        self.node.text = str(text)
        self.node.color = ((0 + random.random() * 1.0), (0 + random.random() * 1.0), (0 + random.random() * 1.0))

    def handleMessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            self.node.delete()
            self.textChangeTimer = None
        else:
            bs.Actor.handleMessage(self, msg)

    def delete(self):
        self.handleMessage(bs.DieMessage())
