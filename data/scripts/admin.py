import os
import json
from bsSpaz import *
import bsSpaz
import bsUtils
import random
import bsInternal
import getPermissionsHashes as gph


class PermissionEffect(object):
    def __init__(self, position=(0, 1, 0), owner=None, prefix='ADMIN', prefixColor=(1, 1, 1),
                 prefixAnim=None, prefixAnimate=True, particles=True, particles2=False, type=1):
        if prefixAnim is None:
            prefixAnim = {0: (1, 1, 1), 500: (0.5, 0.5, 0.5)}
        self.position = position
        self.owner = owner

        # nick
        # text
        # color
        # anim
        # animCurve
        # particles

        def a():
            self.emit()
            self.ice_smoke()

        def b():
            self.emit2()
            self.ice_smoke()

        def c():
            self.emit3()
            self.ice_smoke()

        def d():
            self.emit4()
            self.ice_smoke()

        # particles
        if particles:
            self.timer = bs.Timer(5, bs.Call(a), repeat=True)

        # particles2
        if particles2:
            self.timer = bs.Timer(8, bs.Call(b), repeat=True)

        # prefix
        if type == 1:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.80, 0), 'operation': 'add'})
        else:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.50, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')

        self._Text = bs.newNode('text',
                                owner=self.owner,
                                attrs={'text': prefix,  # prefix text
                                       'inWorld': True,
                                       'shadow': 1.2,
                                       'flatness': 1.0,
                                       'color': prefixColor,
                                       'scale': 0.0,
                                       'hAlign': 'center'})

        m.connectAttr('output', self._Text, 'position')

        bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01})  # smooth prefix spawn

        # animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color', 3, prefixAnim, True)  # animate prefix color

    def ice_smoke(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=3, scale=0.8, emitType='tendrils', tendrilType='smoke')
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=int(5 + random.random() * 5),
                              scale=random.random() * 2, spread=random.random() * 0.2, chunkType='sweat')

    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=3,
                              scale=0.8,
                              spread=0.1,
                              chunkType='spark')

    def emit2(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=3,
                              scale=0.5,
                              spread=0.1,
                              chunkType='sweat')

    def emit3(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=5,
                              scale=0.3,
                              spread=0.1,
                              chunkType='sweat')

    def emit4(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[1] - 0.25 + random.random() * 0.5,
                                        self.owner.torsoPosition[2] - 0.25 + random.random() * 0.8),
                              velocity=((-vel + (random.random() * (vel * 2))) + self.owner.velocity[0] * 2,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[1] * 4,
                                        (-vel + (random.random() * (vel * 2))) + self.owner.velocity[2] * 2),
                              count=1,
                              scale=0.1,
                              spread=0.1,
                              chunkType='sweat')


def __init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5), character="Spaz", player=None, powerupsExpire=True):
    """
    Create a spaz for the provided bs.Player.
    Note: this does not wire up any controls;
    you must call connectControlsToPlayer() to do so.
    """
    # convert None to an empty player-ref
    if player is None: player = bs.Player(None)

    Spaz.__init__(self, color=color, highlight=highlight, character=character, sourcePlayer=player,
                  startInvincible=True, powerupsExpire=powerupsExpire)
    self.lastPlayerAttackedBy = None  # FIXME - should use empty player ref
    self.lastAttackedTime = 0
    self.lastAttackedType = None
    self.heldCount = 0
    self.lastPlayerHeldBy = None  # FIXME - should use empty player ref here
    self._player = player

    profiles = []
    profiles = self._player.getInputDevice()._getPlayerProfiles()
    if os.path.exists(bs.getEnvironment()['systemScriptsDirectory'] + "/toppers.json"):
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/toppers.json", "r")
        aid = str(self._player.get_account_id())
        jd = {}
        try:
            jd = json.loads(f.read())
        except Exception:
            bs.printException()
        if jd.get(str(aid), None) is not None:
            PermissionEffect(owner=self.node, prefix=str(jd[str(aid)]),
                             prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)},
                             particles=False, particles2=True, type=2)
    clID = self._player.getInputDevice().getClientID()
    cl_str = []
    for client in bsInternal._getGameRoster():
        if client['clientID'] == clID:
            cl_str = client['displayString']

    if profiles == [] or profiles == {}:
        profiles = bs.getConfig()['Player Profiles']

    for p in profiles:
        try:
            if cl_str in gph.co:
                PermissionEffect(owner=self.node, prefix='~<CO-LEADER>~',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
            if cl_str in gph.chutiya:
                PermissionEffect(owner=self.node, prefix='#Chutiya', prefixAnim=None, prefixAnimate=False,
                                 particles=False)
                break
            if cl_str in gph.assholes:
                PermissionEffect(owner=self.node, prefix='#Asshole', prefixAnim=None, prefixAnimate=False,
                                 particles=False)
                break
            if cl_str in gph.elder:
                PermissionEffect(owner=self.node, prefix='{Elder}',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
            if cl_str in gph.member:
                PermissionEffect(owner=self.node, prefix='-Member-',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
            if cl_str in gph.vipHashes:
                PermissionEffect(owner=self.node, prefix='[VIP+]',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
            if cl_str in gph.adminHashes:
                PermissionEffect(owner=self.node, prefix='ADMIN',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
            if cl_str in gph.owner:
                PermissionEffect(owner=self.node, prefix='~<{OWNER}>~',
                                 prefixAnim={0: (1, 0, 0), 250: (0, 1, 0), 250 * 2: (0, 0, 1), 250 * 3: (1, 0, 0)})
                break
        except:
            pass

    # grab the node for this player and wire it to follow our spaz (so players' controllers know where to draw their guides, etc)
    if player.exists():
        playerNode = bs.getActivity()._getPlayerNode(player)
        self.node.connectAttr('torsoPosition', playerNode, 'position')


bsSpaz.PlayerSpaz.__init__ = __init__
