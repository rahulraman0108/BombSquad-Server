# NOTE TO SELF - this script supports python 3; should test that occasionally
# and eventually switch to it completely (perhaps when the game itself does)
from __future__ import print_function

import sys
import os
import time
import json
import subprocess
import threading
import traceback
import tempfile
import copy
import pytest


def test_func1():
    # we expect to be running from the dir where this script lives
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    if script_dir != '':
        os.chdir(script_dir)

    config_path = './config.py'
    binary_path = "./bs_headless"
    if binary_path is None:
        raise Exception('unable to locate bs_headless binary')

    # Server settings:
    # Config values are initialized with defaults here.
    # You an add your own overrides in config.py
    config = {}

    # Name of our server in the public parties list
    config['partyName'] = 'FFA'

    # If True, your party will show up in the global public party list
    # Otherwise it will still be joinable via LAN or connecting by IP address
    config['partyIsPublic'] = True

    # UDP port to host on. Change this to work around firewalls or run multiple
    # servers on one machine.
    # 43210 is the default and the only port that will show up in the LAN
    # browser tab.
    config['port'] = 43210

    # Language the server will run in.
    # This is no longer terribly relevant, as all clients now see the game in their
    # own language. You still may want to override this simply to keep your listing
    # accurate however.
    config['language'] = 'English'

    # Max devices in the party. Note that this does *NOT* mean max players.
    # Any device in the party can have more than one player on it if they have
    # multiple controllers. Also, this number currently includes the server so
    # generally make it 1 bigger than you need. Max-players is not currently
    # exposed but I'll try to add that soon.
    config['maxPartySize'] = 6

    # Options here are 'ffa' (free-for-all) and 'teams'
    # this value is only used if you do not supply a playlistCode (see below);
    # in that case the default teams or free-for-all playlist gets used
    config['sessionType'] = 'ffa'

    # To host your own custom playlists, use the 'share' functionality in the
    # playlist editor in the regular version of the game.
    # This will give you a numeric code you can enter here to host that playlist.
    config['playlistCode'] = None

    # Whether to shuffle the playlist or play its games in designated order
    config['playlistShuffle'] = True

    # If True, keeps team sizes equal by disallowing joining the largest team
    # (teams mode only)
    config['autoBalanceTeams'] = True

    # Whether to enable telnet access on port 43250
    # This allows you to run python commands on the server as it is running.
    # Note: you can now also run live commands via stdin so telnet is generally
    # unnecessary. BombSquad's telnet server is very simple so you may have to turn
    # off any fancy features in your telnet client to get it to work.
    # IMPORTANT: Telnet is not encrypted at all, so you really should not expose
    # it's port to the world. If you need remote access, consider connecting to
    # your machine via ssh and running telnet to localhost from there.
    config['enableTelnet'] = False

    # Port used for telnet
    config['telnetPort'] = 43250

    # This can be None for no password but PLEASE do not expose that to the
    # world or your machine will likely get owned.
    config['telnetPassword'] = 'changeme'

    # Series length in teams mode (7 == 'best-of-7' series; a team must get 4 wins)
    config['teamsSeriesLength'] = 7

    # Points to win in free-for-all mode (Points are awarded per game based on
    # performance)
    config['ffaSeriesScoreToWin'] = 24

    # If you provide a custom stats webpage for your server, you can use
    # this to provide a convenient in-game link to it in the server-browser
    # beside the server name.
    # if ${ACCOUNT} is present in the string, it will be replaced by the
    # currently-signed-in account's id.  To get info about an account,
    # you can use the following url:
    # http://bombsquadgame.com/accountquery?id=ACCOUNT_ID_HERE
    config['statsURL'] = ''

    # If config.py exists, run it to apply any overrides it wants..
    if os.path.isfile(config_path):
        exec (compile(open(config_path).read(), config_path, 'exec'))

    restart_server = True

    # the server-binary will get relaunched after this amount of time
    # (combats memory leaks or other cruft that has built up)
    restart_minutes = 360

    # sleep for just a moment to allow initial stdin data to get through
    time.sleep(0.25)

    # restart indefinitely until we're told not to..
    while restart_server:
        launch_time = time.time()

        # most of our config values we can feed to bombsquad as it is running
        # (see below). however certain things such as network-port need to be
        # present in bs's config file at launch... so let's write out a config first
        if not os.path.exists('bscfg'):
            os.mkdir('bscfg')
        if os.path.exists('bscfg/config.json'):
            f = open('bscfg/config.json')
            bscfg = json.loads(f.read())
            f.close()
        else:
            bscfg = {}
        bscfg['Port'] = config['port']
        bscfg['Enable Telnet'] = config['enableTelnet']
        bscfg['Telnet Port'] = config['telnetPort']
        bscfg['Telnet Password'] = config['telnetPassword']
        f = open('bscfg/config.json', 'w')
        f.write(json.dumps(bscfg))
        f.close()

        # launch our binary and grab its stdin; we'll use this to feed it commands
        result = subprocess.Popen(
            [binary_path, '-cfgdir', 'bscfg'], stdin=subprocess.PIPE)
        import termCommands
        tc = termCommands.TermCommands(result.stdin)

        # set quit to True any time after launching the server to gracefully quit it
        # at the next clean opportunity (end of the current series, etc)
        config['quit'] = False
        config['quitReason'] = None

        # so we pass our initial config..
        config_dirty = True

        # now just sleep and run commands until the server exits
        while True:

            # request a restart after a while
            if (time.time() - launch_time > 60 * restart_minutes
                    and not config['quit']):
                print('restart_minutes (' + str(restart_minutes) +
                      'm) elapsed; requesting server restart '
                      'at next clean opportunity...')
                config['quit'] = True
                config['quitReason'] = 'restarting'
                config_dirty = True

            # whenever the config changes, dump it to a json file and feed it to the
            # running server
            if config_dirty:
                f = tempfile.NamedTemporaryFile(mode='w', delete=False)
                fname = f.name
                f.write(json.dumps(config))
                f.close()
                # (game handles deleting this file for us once its done with it)
                result.stdin.write(('bsUtils.configServer(configFile=' +
                                    repr(fname) + ')\n').encode('utf-8'))
                result.stdin.flush()
                config_dirty = False

            code = result.poll()
            if code is not None:
                print('BombSquad exited with code ' + str(code))
                break

            time.sleep(1)
            assert True, "Test Passed"
