import bs
import bsUtils
import bsVector
import random


class snoMessage(object):
    pass


class areaMessage(object):
    pass


class footingHitMessage(object):
    pass


class ObjectFactory(object):

    def __init__(self):
        self.texSno = bs.getTexture("bunnyColor")
        self.texHail = bs.getTexture("bombColorIce")
        self.snoModel = bs.getModel("frostyPelvis")
        self.hailModel = bs.getModel("powerup")
        self.snowMaterial = bs.Material()
        self.impactSound = bs.getSound('impactMedium')
        self.areaMaterial = bs.Material()
        self.snowMaterial.addActions(conditions=('theyHaveMaterial', bs.getSharedObject('playerMaterial')),
                                     actions=(('modifyPartCollision', 'physical', False),
                                              ('message', 'ourNode', 'atConnect', snoMessage())))
        self.snowMaterial.addActions(conditions=(('theyHaveMaterial', self.areaMaterial)),
                                     actions=('message', 'ourNode', 'atConnect', areaMessage()))
        self.snowMaterial.addActions(conditions=(('theyDontHaveMaterial', bs.getSharedObject('playerMaterial')), 'and',
                                                 ('theyHaveMaterial', bs.getSharedObject('footingMaterial'))),
                                     actions=('message', 'ourNode', 'atConnect', footingHitMessage()))
        self.defaultBallTimeout = 300
        self._ballsBust = True
        self._powerExpire = True
        self._powerLife = 20000


class SnowBall(bs.Actor):
    def __init__(self, position=(0, 1, 0), velocity=(5, 0, 5)):
        bs.Actor.__init__(self)

        factory = self.getFactory()
        self.node = bs.newNode("prop",
                               delegate=self,
                               attrs={'model': factory.snoModel,
                                      'body': 'sphere',
                                      'colorTexture': factory.texSno,
                                      'reflection': 'soft',
                                      'modelScale': 0.4,
                                      'bodyScale': 0.4,
                                      'density': 1,
                                      'reflectionScale': [0.15],
                                      'shadowSize': 0.6,
                                      'position': position,
                                      'velocity': velocity,
                                      'materials': [bs.getSharedObject('objectMaterial'), factory.snowMaterial]
                                      })
        self._exploded = False
        if factory._ballsBust:
            self.shouldBust = True
        else:
            self.shouldBust = False

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage(how="outOfBounds"))
        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1], m.velocity[2],
                                    1.0 * m.magnitude, 1.0 * m.velocityMagnitude, m.radius, 0,
                                    m.forceDirection[0], m.forceDirection[1], m.forceDirection[2])
        elif isinstance(m, bs.ImpactDamageMessage):
            print [dir(m), m.intensity]
        elif isinstance(m, snoMessage):
            if self._exploded:
                return
            v = self.node.velocity
            if bs.Vector(*v).length() > 5.0:
                node = bs.getCollisionInfo("opposingNode")

                if node is not None and node.exists():
                    t = self.node.position
                    hitDir = self.node.velocity

                    node.handleMessage(bs.HitMessage(pos=t,
                                                     velocity=v,
                                                     magnitude=bsVector.Vector(*v).length(),
                                                     velocityMagnitude=bsVector.Vector(*v).length() * 0.5,
                                                     radius=0,
                                                     srcNode=self.node,
                                                     sourcePlayer=None,
                                                     forceDirection=hitDir,
                                                     hitType='snoBall',
                                                     hitSubType='default'))
            self._exploded = True

            bs.gameTimer(1, bs.WeakCall(self.handleMessage, bs.DieMessage(how="snoMessage")))
        elif isinstance(m, areaMessage):
            self.handleMessage(bs.DieMessage(how="areaMessage"))
        elif isinstance(m, footingHitMessage):
            if self._exploded:
                return
            bs.gameTimer(1000, bs.WeakCall(self.handleMessage, bs.DieMessage()))
        else:
            bs.Actor.handleMessage(self, m)

    def _disappear(self):
        self._exploded = True
        if self.exists():
            scl = self.node.modelScale
            bsUtils.animate(self.node, "modelScale", {0: scl * 1.0, 300: scl * 0.5, 500: 0.0})
            bs.gameTimer(550, bs.WeakCall(self.handleMessage, bs.DieMessage(how="disappeared")))

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        if activity is None:
            raise Exception("no current activity")
        try:
            return activity._sharedSnowStormFactory
        except Exception:
            f = activity._sharedSnowStormFactory = ObjectFactory()
            return f


class HailStone(bs.Actor):
    def __init__(self, position=(0, 1, 0), velocity=(5, 0, 5)):
        bs.Actor.__init__(self)

        factory = self.getFactory()
        self.node = bs.newNode("prop",
                               delegate=self,
                               attrs={'model': factory.hailModel,
                                      'body': 'sphere',
                                      'colorTexture': factory.texHail,
                                      'reflection': 'soft',
                                      'modelScale': 0.2,
                                      'bodyScale': 0.2,
                                      'density': 1,
                                      'reflectionScale': [0.15],
                                      'shadowSize': 0.6,
                                      'position': position,
                                      'velocity': velocity,
                                      'materials': [bs.getSharedObject('objectMaterial'), factory.snowMaterial]
                                      })
        self._exploded = False
        if factory._ballsBust:
            self.shouldBust = True
        else:
            self.shouldBust = False

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage(how="outOfBounds"))
        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1], m.velocity[2],
                                    1.0 * m.magnitude, 1.0 * m.velocityMagnitude, m.radius, 0,
                                    m.forceDirection[0], m.forceDirection[1], m.forceDirection[2])
        elif isinstance(m, bs.ImpactDamageMessage):
            print [dir(m), m.intensity]
        elif isinstance(m, snoMessage):
            if self._exploded:
                return
            v = self.node.velocity
            node = bs.getCollisionInfo("opposingNode")

            if node is not None and node.exists():
                if not node.getDelegate().frozen:
                    node.getDelegate().handleMessage(bs.FreezeMessage())
                else:
                    node.getDelegate().handleMessage(bs.ShouldShatterMessage())
                    node.getDelegate().handleMessage(bs.DieMessage())

            bs.gameTimer(1, bs.WeakCall(self.handleMessage, bs.DieMessage(how="snoMessage")))
        elif isinstance(m, areaMessage):
            self.handleMessage(bs.DieMessage(how="areaMessage"))
        elif isinstance(m, footingHitMessage):
            if self._exploded:
                return
            bs.gameTimer(1000, bs.WeakCall(self.handleMessage, bs.DieMessage()))
        else:
            bs.Actor.handleMessage(self, m)

    def _disappear(self):
        self._exploded = True
        if self.exists():
            scl = self.node.modelScale
            bsUtils.animate(self.node, "modelScale", {0: scl * 1.0, 300: scl * 0.5, 500: 0.0})
            bs.gameTimer(550, bs.WeakCall(self.handleMessage, bs.DieMessage(how="disappeared")))

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        if activity is None:
            raise Exception("no current activity")
        try:
            return activity._sharedSnowStormFactory
        except Exception:
            f = activity._sharedSnowStormFactory = ObjectFactory()
            return f


class ProtectedSpazArea(bs.Actor):
    """For making the area to give the spaz protection from ice hail stones."""

    def __init__(self, position, radius):
        bs.Actor.__init__(self)
        self.position = (position[0], position[1] - 0.5, position[2])
        self.radius = radius
        color = (random.random(), random.random(), random.random())
        factory = self.getFactory()
        self.node = bs.newNode('region',
                               attrs={'position': (self.position[0], self.position[1], self.position[2]),
                                      'scale': (self.radius, self.radius, self.radius),
                                      'type': 'sphere',
                                      'materials': [factory.areaMaterial, bs.getSharedObject("regionMaterial")]})
        self.visualRadius = bs.newNode('shield', attrs={'position': self.position, 'color': color, 'radius': 0.1})
        bsUtils.animate(self.visualRadius, "radius", {0: 0, 500: self.radius * 2})
        bsUtils.animateArray(self.node, "scale", 3, {0: (0, 0, 0), 500: (self.radius, self.radius, self.radius)})

    def delete(self):
        if self.node.exists():
            self.node.delete()
        if self.visualRadius.exists():
            self.visualRadius.delete()

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        if activity is None:
            raise Exception("no current activity")
        try:
            return activity._sharedSnowStormFactory
        except Exception:
            f = activity._sharedSnowStormFactory = ObjectFactory()
            return f

