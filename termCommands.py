# coding=utf-8


class TermCommands:
    def __init__(self, stdin):
        """To make an instance of this class."""
        self.stdin = stdin

    def start(self, string):
        """To start analyzing and then processing commands.."""
        if string.startswith("/"):
            command_with_arguments = string.split(" ")
            command = command_with_arguments[0]
            arguments = command_with_arguments[1:]
            self.run(command, arguments)

    def kickByNick(self, nick):
        self.stdin.write("""c = '''roster = bsInternal._getGameRoster()""" +
                         """\\n    for i in roster:""" +
                         """\\n        try:""" +
                         """\\n            if i['players'][0]['nameFull'].lower().find(""" + str(nick) +
                         """.encode('utf-8').lower()) != -1:""" +
                         """\\n                bsInternal._disconnectClient(int(i['clientID']))""" +
                         """\\n        except:""" +
                         """\\n            pass'''
exec(c)\n""")
        self.stdin.flush()

    def run(self, command, args):
        """To run an analyzed command with arguments."""
        self.stdin.write("# coding=utf-8\nimport weakref\na = bs.getActivity()\nactivity = weakref.ref(a)\n" +
                         "del(a)\nimport getPermissionsHashes as gph\n")
        if command == '/kick':
            if not args:
                return
            else:
                if len(args[0]) > 3:
                    self.kickByNick(args[0])
                else:
                    try:
                        self.stdin.write("bsInternal._disconnectClient(int(" + str(args[0]) + "))\n")
                        self.stdin.flush()
                    except:
                        self.kickByNick(args[0])
        elif command == '/admin':
            clID = int(args[0])
            self.stdin.write("""c = '''for client in bsInternal._getGameRoster():""" +
                             """\\n    if client['clientID'] == int(""" + str(clID) + """):""" +
                             """\\n        if """ + str(args[1]) + """ == 'add':""" +
                             """\\n            newadmin = client['displayString']""" +
                             """\\n            gph.co.append(newadmin)""" +
                             """\\n        elif """ + str(args[1]) + """ == 'remove':""" +
                             """\\n            newadmin = client['displayString']""" +
                             """\\n            if newadmin in gph.co:""" +
                             """\\n                gph.co.remove(newadmin)'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/chu':
            clID = int(args[0])
            self.stdin.write("""c = '''for client in bsInternal._getGameRoster():""" +
                             """\\n    if client['clientID'] == int(""" + str(clID) + """):""" +
                             """\\n        if """ + str(args[1]) + """ == 'add':""" +
                             """\\n            chutiya = client['displayString']""" +
                             """\\n            gph.chutiya.append(chutiya)""" +
                             """\\n        elif """ + str(args[1]) + """ == 'remove':""" +
                             """\\n            chutiya = client['displayString']""" +
                             """\\n            if chutiya in gph.chutiya:""" +
                             """\\n                gph.chutiya.remove(chutiya)'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/ass':
            clID = int(args[0])
            self.stdin.write("""c = '''for client in bsInternal._getGameRoster():""" +
                             """\\n    if client['clientID'] == int(""" + str(clID) + """):""" +
                             """\\n        if """ + str(args[1]) + """ == 'add':""" +
                             """\\n            asshole = client['displayString']""" +
                             """\\n            gph.assholes.append(asshole)""" +
                             """\\n        elif """ + str(args[1]) + """ == 'remove':""" +
                             """\\n            asshole = client['displayString']""" +
                             """\\n            if asshole in gph.assholes:""" +
                             """\\n                gph.assholes.remove(asshole)'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/vip':
            clID = int(args[0])
            self.stdin.write("""c = '''for client in bsInternal._getGameRoster():""" +
                             """\\n    if client['clientID'] == int(""" + str(clID) + """):""" +
                             """\\n        if """ + str(args[1]) + """ == 'add':""" +
                             """\\n            cl_str = client['displayString']""" +
                             """\\n            gph.vipHashes.append(cl_str)""" +
                             """\\n        elif """ + str(args[1]) + """ == 'remove':""" +
                             """\\n            cl_str = client['displayString']""" +
                             """\\n            if cl_str in gph.vipHashes:""" +
                             """\\n                gph.vipHashes.remove(cl_str)'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/list':
            self.stdin.write("""print("======== FOR /kick(and /admin like) ONLY: ========")\n
c = '''for i in bsInternal._getGameRoster():""" +
                             """\\n    try:""" +
                             """\\n        print(str(i['players'][0]['nameFull']) +  "     """ +
                             """(/kick " + str(i['clientID']) + ")")""" +
                             """\\n    except:""" +
                             """\\n        pass'''\n
exec(c)\n
print("==================================")\n
print("======= For other commands: =======")\n
for s in bsInternal._getForegroundHostSession().players:print(str(s.getName()) + "     " +""" +
                             """ str(bsInternal._getForegroundHostSession().players.index(s)))\n""")
            self.stdin.flush()
        elif command == '/ooh':
            if args is not None and len(args) > 0:
                s = int(args[0])

                self.stdin.write("""c = '''def oohRecurce(c):""" +
                                 """\\n    bs.playSound(bs.getSound('ooh'), volume=2)""" +
                                 """\\n    c -= 1""" +
                                 """\\n    if c > 0:""" +
                                 """\\n        bs.gameTimer(int(""" + str(args[1]) + """) if len(args) > 1 and """ +
                                 str(args[1]) + """ is not None else 1000, bs.Call(oohRecurce, c=c))'''
exec(c)
oohRecurce(int(""" + str(s) + """))\n""")
                self.stdin.flush()
            else:
                self.stdin.write("""bs.playSound(bs.getSound('ooh'), volume=2)\n""")
                self.stdin.flush()
        elif command == "/quit":
            self.stdin.write("bsInternal.quit()\n")
            self.stdin.flush()
        elif command == "/say":
            say = ""
            for i in range(args):
                say += str(args[i])
            self.stdin.write("bsInternal._chatMessage('" + str(say) + "')\n")
            self.stdin.flush()
        elif command == '/freeze':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.actor.node.handleMessage(bs.FreezeMessage())
\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("bs.getSession().players[int(" + str(
                        args[0]) + ")].actor.node.handleMessage(bs.FreezeMessage())\n")
                    self.stdin.flush()
        elif command == '/thaw':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.actor.node.handleMessage(bs.ThawMessage())
\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("bs.getSession().players[int(" + str(
                        args[0]) + ")].actor.node.handleMessage(bs.ThawMessage())\n")
                    self.stdin.flush()
        elif command == '/sleep':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.actor.node.handleMessage("knockout", 5000)
\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bs.getSession().players[int(""" + str(
                        args[0]) + """)].actor.node.handleMessage("knockout", 5000)\n""")
                    self.stdin.flush()
        elif command == '/kill':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.actor.node.handleMessage(bs.DieMessage())
\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bs.getSession().players[int(""" + str(
                        args[0]) + """)].actor.node.handleMessage(bs.DieMessage())\n""")
                    self.stdin.flush()
        elif command == '/curse':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.actor.curse()
\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bs.getSession().players[int(""" + str(
                        args[0]) + """)].actor.curse()\n""")
                    self.stdin.flush()
        elif command == "/box":
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""c = '''for i in bs.getSession().players:""" +
                                     """\\n    try:""" +
                                     """\\n        i.actor.node.torsoModel = bs.getModel("tnt")""" +
                                     """\\n        i.actor.node.colorMaskTexture = bs.getTexture("tnt")""" +
                                     """\\n        i.actor.node.colorTexture = bs.getTexture("tnt")""" +
                                     """\\n        i.actor.node.highlight = (1, 1, 1)""" +
                                     """\\n        i.actor.node.color = (1, 1, 1)""" +
                                     """\\n        i.actor.node.headModel = None""" +
                                     """\\n        i.actor.node.style = "cyborg" """ +
                                     """\\n    except:""" +
                                     """\\n        print""" +
                                     """\\n        'error' '''
exec(c)\n""")
                    self.stdin.flush()
                else:
                    n = int(args[0])
                    self.stdin.write("""c = '''n = int(""" + str(n) + """)"""
                                     + """\\nbs.getSession().players[n].actor.node.torsoModel = bs.getModel("tnt")"""
                                     + """\\nbs.getSession().players[n].actor.node.colorMaskTexture ="""
                                     + """ bs.getTexture("tnt")""" +

                                     """\\nbs.getSession().players[n].actor.node.colorTexture = bs.getTexture("tnt")"""
                                     + """\\nbs.getSession().players[n].actor.node.highlight = (1, 1, 1)""" +
                                     """\\nbs.getSession().players[n].actor.node.color = (1, 1, 1)""" +
                                     """\\nbs.getSession().players[n].actor.node.headModel = None""" +
                                     """\\nbs.getSession().players[n].actor.node.style = "cyborg"'''
exec(c)\n""")
                    self.stdin.flush()
        elif command == '/remove':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bs.getSession().players:i.removeFromGame()\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bs.getSession().players[int(""" + str(args[0]) + """)].removeFromGame()\n""")
                    self.stdin.flush()
        elif command == '/end':
            self.stdin.write("""bsInternal._getForegroundHostActivity().endGame()\n""")
            self.stdin.flush()
        elif command == '/snake':
            self.stdin.write("""c = '''try:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[0].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[1].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[1].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[2].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[2].actor.node.holdNode = \\""" +
                             """\\n""" +
                             """        bsInternal._getForegroundHostActivity().players[3].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[3].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[4].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[4].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[5].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[5].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[6].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[6].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[7].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    bsInternal._getForegroundHostActivity().players[7].actor.node.holdNode = \\""" +
                             """\\n        bsInternal._getForegroundHostActivity().players[0].actor.node""" +
                             """\\nexcept:""" +
                             """\\n    pass'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/spaz':
            if not args:
                return
            else:
                if args[0] == 'all':
                    c = str(args[1])
                    self.stdin.write("""c = '''c = \"""" + str(c) + """\"""" +
                                     """\\nfor i in bs.getSession().players:""" +
                                     """\\n    try:""" +
                                     """\\n        i.actor.node.torsoModel = bs.getModel(c+"Torso")""" +
                                     """\\n        i.actor.node.colorMaskTexture = bs.getTexture(c+"ColorMask")""" +
                                     """\\n        i.actor.node.colorTexture = bs.getTexture(c+"Color")""" +
                                     """\\n        i.actor.node.headModel = bs.getModel(c+"Head")""" +
                                     """\\n        i.actor.node.toesModel = bs.getModel(c+"Toes")""" +
                                     """\\n        i.actor.node.pelvisModel = bs.getModel(c+"Pelvis")""" +
                                     """\\n        i.actor.node.upperArmModel = bs.getModel(c+"UpperArm")""" +
                                     """\\n        i.actor.node.foreArmModel = bs.getModel(c+"ForeArm")""" +
                                     """\\n        i.actor.node.handModel = bs.getModel(c+"Hand")""" +
                                     """\\n        i.actor.node.upperLegModel = bs.getModel(c+"UpperLeg")""" +
                                     """\\n        i.actor.node.lowerLegModel = bs.getModel(c+"LowerLeg")""" +
                                     """\\n        i.actor.node.style = c""" +
                                     """\\n        bunnySounds = [c + '1', c + '2']""" +
                                     """\\n        bunnyHitSounds = [c + 'Hit1', c + 'Hit2']""" +
                                     """\\n        i.actor.node.attackSounds = bunnySounds""" +
                                     """\\n        i.actor.node.jumpSounds = [c + 'Jump']""" +
                                     """\\n        i.actor.node.impactSounds = bunnyHitSounds""" +
                                     """\\n        i.actor.node.deathSounds = [c + "Death"]""" +
                                     """\\n        i.actor.node.pickupSounds = bunnySounds""" +
                                     """\\n        i.actor.node.fallSounds = [c + "Fall"]""" +
                                     """\\n    except:""" +
                                     """\\n        print('error')'''
exec(c)\n""")
                    self.stdin.flush()
                else:
                    n = int(args[0])
                    c = str(args[1])
                    self.stdin.write("""c = '''n = int(""" + str(n) + """)""" +
                                     """\\nc = \"""" + str(c) + """\"""" +
                                     """\\nbs.getSession().players[n].actor.node.torsoModel = bs.getModel(c+"Torso")"""
                                     + """\\nbs.getSession().players[n].actor.node.colorMaskTexture =""" +
                                     """ bs.getTexture(c+"ColorMask")""" +

                                     """\\nbs.getSession().players[n].actor.node.colorTexture =""" +
                                     """ bs.getTexture(c+"Color")""" +

                                     """\\nbs.getSession().players[n].actor.node.headModel = bs.getModel(c+"Head")""" +
                                     """\\nbs.getSession().players[n].actor.node.toesModel = bs.getModel(c+"Toes")""" +
                                     """\\nbs.getSession().players[n].actor.node.pelvisModel =""" +
                                     """ bs.getModel(c+"Pelvis")""" +

                                     """\\nbs.getSession().players[n].actor.node.upperArmModel =""" +
                                     """ bs.getModel(c+"UpperArm")""" +

                                     """\\nbs.getSession().players[n].actor.node.foreArmModel =""" +
                                     """ bs.getModel(c+"ForeArm")""" +

                                     """\\nbs.getSession().players[n].actor.node.handModel = bs.getModel(c+"Hand")""" +
                                     """\\nbs.getSession().players[n].actor.node.upperLegModel =""" +
                                     """ bs.getModel(c+"UpperLeg")""" +

                                     """\\nbs.getSession().players[n].actor.node.lowerLegModel =""" +
                                     """ bs.getModel(c+"LowerLeg")""" +

                                     """\\nbs.getSession().players[n].actor.node.style = c""" +
                                     """\\nbunnySounds = [c + '1', c + '2']"""
                                     + """\\nbunnyHitSounds = [c + 'Hit1', c + 'Hit2']""" +
                                     """\\nbs.getSession().players[n].actor.node.attackSounds = bunnySounds""" +
                                     """\\nbs.getSession().players[n].actor.node.jumpSounds = [c + 'Jump']""" +
                                     """\\nbs.getSession().players[n].actor.node.impactSounds = bunnyHitSounds""" +
                                     """\\nbs.getSession().players[n].actor.node.deathSounds = [c + "Death"]""" +
                                     """\\nbs.getSession().players[n].actor.node.pickupSounds = bunnySounds""" +
                                     """\\nbs.getSession().players[n].actor.node.fallSounds = [c + "Fall"]'''
exec(c)\n""")
                    self.stdin.flush()
        elif command == '/tex':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""c = '''for i in bs.getSession().players:""" +
                                     """\\n    try:""" +
                                     """\\n        i.actor.node.colorMaskTexture = bs.getTexture("egg1")""" +
                                     """\\n        i.actor.node.colorTexture = bs.getTexture("egg1")""" +
                                     """\\n    except:""" +
                                     """\\n        print('error')'''
exec(c)\n""")
                    self.stdin.flush()
                else:
                    n = int(args[0])
                    self.stdin.write("""bs.getSession().players[""" + str(
                        n) + """].actor.node.colorMaskTexture = bs.getTexture("egg1")
bs.getSession().players[""" + str(n) + """].actor.node.colorTexture = bs.getTexture("egg1")\n""")
                    self.stdin.flush()
        elif command == '/hug':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""c = '''try:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[0].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[1].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass""" +
                                     """\\ntry:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[1].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[0].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass""" +
                                     """\\ntry:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[3].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[2].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass""" +
                                     """\\ntry:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[4].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[3].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass""" +
                                     """\\ntry:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[5].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[6].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass""" +
                                     """\\ntry:""" +
                                     """\\n    bsInternal._getForegroundHostActivity().players[6].actor.""" +
                                     """node.holdNode = \\""" +
                                     """\\n        bsInternal._getForegroundHostActivity().players[7].actor.node""" +
                                     """\\nexcept:""" +
                                     """\\n    pass'''
exec(c)\n""")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bsInternal._getForegroundHostActivity().players[int(""" + str(
                        args[0]) + """)].actor.node.holdNode = bsInternal._getForegroundHostActivity().""" +
                                     """players[int(""" + str(
                        args[1]) + """)].actor.node\n""")
                    self.stdin.flush()
        elif command == '/speed':
            if not args:
                return
            else:
                self.stdin.write("""activity.players[int(""" + str(
                    args[0]) + """)].actor.node.hockey = activity.players[int(""" + str(
                    args[0]) + """)].actor.node.hockey == False\n""")
                self.stdin.flush()
        elif command == '/gm':
            if not args:
                return
            else:
                self.stdin.write("""activity.players[int(""" + str(args[0]) +
                                 """)].actor.node.hockey = activity.players[int(""" + str(args[0]) +
                                 """)].actor.node.hockey == False""" +
                                 """\\nactivity.players[int(""" + str(
                    args[0]) + """)].actor.node.invincible = activity.players[int(""" + str(
                    args[0]) + """)].actor.node.invincible == False""" +
                                 """\\nactivity.players[int(""" + str(
                    args[0]) + """)].actor._punchPowerScale = 5 if activity.players[int("""
                                 + str(args[0]) + """)].actor._punchPowerScale == 1.2 else 1.2\n""")
                self.stdin.flush()
        elif command == '/tint':
            if not args:
                return
            else:
                if args[0] == 'r':
                    command = 1.3 if args[1] is None else float(args[1])
                    s = 1000 if args[2] is None else float(args[2])
                    self.stdin.write("""bsUtils.animateArray(bs.getSharedObject('globals'), 'tint', 3, {0: (1 * """ +
                                     str(command) + """, 0, 0), """ + str(s) + """: (0, 1 * """ + str(command) +
                                     """, 0), """ + str(s) + """ * 2: (0, 0, 1 * """ + str(command) + """),"""
                                     + str(s) + """ * 3: (1 * """ + str(command) + """, 0, 0)}, True)\n""")
                    self.stdin.flush()
                else:
                    if args[2] is not None:
                        self.stdin.write("bs.getSharedObject('globals').tint = (" + str(float(args[0])) + ", " + str(
                            float(args[1])) + ", " + str(float(args[2])) + ")\n")
                        self.stdin.flush()
        elif command == '/sm':
            self.stdin.write(
                "bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False\n")
            self.stdin.flush()
        elif command == '/bunny':
            if not args:
                return
            self.stdin.write("""c = '''import BuddyBunny""" +
                             """\\nfor i in range(int(""" + str(args[0]) + """)):""" +
                             """\\n    p = bs.getSession().players[int(""" + str(args[1]) + """)]""" +
                             """\\n    if not 'bunnies' in p.gameData:""" +
                             """\\n        p.gameData['bunnies'] = BuddyBunny.BunnyBotSet(p)""" +
                             """\\n    p.gameData['bunnies'].doBunny()'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/cameraMode':
            self.stdin.write("""c = '''if bs.getSharedObject('globals').cameraMode == 'follow':""" +
                             """\\n    bs.getSharedObject('globals').cameraMode = 'rotate'""" +
                             """\\nelse:""" +
                             """\\n    bs.getSharedObject('globals').cameraMode = 'follow'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/lm':
            self.stdin.write("""c = '''arr = []""" +
                             """\\nfor i in range(100):""" +
                             """\\n    try:""" +
                             """\\n        arr.append(bsInternal._getChatMessages()[-1 - i])""" +
                             """\\n    except:""" +
                             """\\n        pass""" +
                             """\\narr.reverse()""" +
                             """\\nfor i in arr:""" +
                             """\\n    print(i)'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/gp':
            if not args:
                return
            else:
                self.stdin.write("""c = '''s = bsInternal._getForegroundHostSession()""" +
                                 """\\nfor i in s.players[int(""" + str(
                    args[0]) + """)].getInputDevice()._getPlayerProfiles():""" +
                                 """\\n    try:""" +
                                 """\\n        print(i)""" +
                                 """\\n    except:""" +
                                 """\\n        pass'''
exec(c)\n""")
                self.stdin.flush()
        elif command == '/icy':
            self.stdin.write("""bsInternal._getForegroundHostActivity().players[int(""" + str(
                args[0]) + """)].actor.node = bsInternal._getForegroundHostActivity().players[int(""" + str(
                args[1]) + """)].actor.node\n""")
            self.stdin.flush()
        elif command == '/fly':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("for i in bsInternal._getForegroundHostActivity().players: i.actor.node.fly = " +
                                     "True\n")
                    self.stdin.flush()
                else:
                    self.stdin.write("""bsInternal._getForegroundHostActivity().players[int(""" + str(
                        args[0]) + """)].actor.node.fly = bsInternal._getForegroundHostActivity().players[int(""" + str(
                        args[0]) + """)].actor.node.fly == False\n""")
                    self.stdin.flush()
        elif command == '/iceOff':
            self.stdin.write("""c = '''try:""" +
                             """\\n    activity.getMap().node.materials = [bs.getSharedObject('footingMaterial')]""" +
                             """\\n    activity.getMap().isHockey = False""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\ntry:""" +
                             """\\n    activity.getMap().floor.materials = [bs.getSharedObject('footingMaterial')]""" +
                             """\\n    activity.getMap().isHockey = False""" +
                             """\\nexcept:""" +
                             """\\n    pass""" +
                             """\\nfor i in activity.players:""" +
                             """\\n    i.actor.node.hockey = False'''
exec(c)\n""")
            self.stdin.flush()
        elif command == '/maxPlayers':
            if not args:
                return
            else:
                self.stdin.write("""c = '''try:""" +
                                 """\\n    bsInternal._getForegroundHostSession()._maxPlayers = int(""" + str(
                    args[0]) + """)""" +
                                 """\\n    bsInternal._setPublicPartyMaxSize(int(""" + str(args[0]) + """))""" +
                                 """\\n    print('Players limit set to ' + str(int(""" + str(args[0]) + """)))""" +
                                 """\\nexcept:""" +
                                 """\\n    pass'''
exec(c)\n""")
                self.stdin.flush()
        elif command == '/heal':
            if not args:
                return
            else:
                self.stdin.write("bsInternal._getForegroundHostActivity().players[int(" + str(
                    args[0]) + ")].actor.node.handleMessage(bs.PowerupMessage(powerupType='health'))\n")
                self.stdin.flush()
        elif command == '/shatter':
            if not args:
                return
            else:
                if args[0] == 'all':
                    self.stdin.write("""for i in bsInternal._getForegroundHostActivity().players:""" +
                                     """ i.actor.node.shattered = int(""" + str(args[1]) + """)""")
                    self.stdin.flush()
                else:
                    self.stdin.write("bsInternal._getForegroundHostActivity().players[int(" + str(
                        args[0]) + ")].actor.node.shattered = int(" + str(args[1]) + ")")
                    self.stdin.flush()
