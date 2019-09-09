# coding=utf-8
import threading
import json
import os
import urllib2
import bs
import settings

port = 43210  # The port of your party in `bombsquad_server`
partyName = settings.partyName  # The name of your party in `bombsquad_server`
webServerRootDirectory = "/var/www/html/"  # The directory which is served by the web server on your system
stats_file = bs.getEnvironment()['systemScriptsDirectory'] + "/stats.json"  # Don't change
mainHTMLFile = webServerRootDirectory + str(port) + ".html"  # Don't change
botEnabled = settings.botFile  # Don't change
bot_file = webServerRootDirectory + str(port) + ".json"  # Don't change

html1_start = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial scale=1"/>
    <link rel="stylesheet" href="2.css"/>
    <link rel="stylesheet" href="thegr8.css"/>
    <title>""" + str(partyName) + """ Players Stats</title>
    <script type="text/javascript">
        function show() {
            var value = document.getElementById("playerstoshow").value;
            var table = document.getElementById("table");
            var rows = table.getElementsByTagName("tr");
            var boolv = Number.isInteger(parseInt(value));
            if (boolv === true) {
                for (var i = 1; i < (rows.length); i++) {
                    var row = document.getElementById(String(i));
                    row.style.display = "";
                    if (i > parseInt(value)) {
                        row.style.display = "none";
                    }
                }
            }
            alert("Upto " + String(value) + " number of row(s) of player stats table is/are shown.");
        }

        function search() {
            var input, filter, table, tr, td, i, txtValue, value;
            input = document.getElementById("searchInput");
            filter = input.value.toUpperCase();
            table = document.getElementById("table");
            tr = table.getElementsByTagName("tr");
            value = document.getElementById("playerstoshow").value;
            for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[1];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        if (i > parseInt(value)) {
                            tr[i].style.display = "none";
                        } else {
                            tr[i].style.display = "";
                        }
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }
    </script>
</head>

<body onload="show()">
<section>
    <div>
        <div class="no-limits"><b>""" + str(partyName) + """ party's player stats.</b><br>
            <img alt="Intro image" src="teaser.png"
                 style="alignment: center; align-content: center; height: 24%; width: 50%">

            <div style="font-size: 22px;background-color:lightblue;" class="dropdown">
                <button class="dropbtn">Some important links:</button>
                <div class="dropdown-content">
                  <a href="https://patreon.com/rahulraman">Patreon</a>
                  <a href="https://discordapp.com/invite/BCZvf3W">Discord</a>
                  <a href="https://www.youtube.com/channel/UCme4Yo-CHGvdBcgFv8rXomQ">YouTube</a>
                  <a href="https://thegreat.ml/subscribe/">My Email Newsletter</a>
                  <a href="https://thegreat.ml/">My Website</a>
                </div>
            </div>

            <p id="counter" class="counter"></p></div>

        <section id="full">
            <div style="background-color:lightblue" class="limit-min-max">
                <label for="playerstoshow">Number of rows of player of the following stats table to show:</label>
                <input type="number" id="playerstoshow" onchange="show()" value="100"/>
                <input type="text" id="searchInput" onkeyup="search()" placeholder="Search for names.."
                       title="Type in a name">
            </div>
            <table class="background" id="table" style="width: 100%;">
                <tr>
                    <th><u>Rank</u></th>
                    <th><u>Player</u></th>
                    <th><u>Scores</u></th>
                    <th><u>Kills</u></th>
                    <th><u>Deaths</u></th>
                </tr>"""
html1_end = """
            </table>
        </section>
    </div>
</section>
<script type="text/javascript">
    var countDownDate = new Date("Sep 31, 2019 24:00:00").getTime();
    var x = setInterval(function () {
        var now = new Date().getTime();
        var distance = countDownDate - now;
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        document.getElementById("counter").innerHTML = "Season Ends In " + days + "Days " + hours + "Hrs ";
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("counter").innerHTML = "Season Results";
        }
    }, 1000);
</script>
</body>
</html>"""


def update(score_set):
    """
   Given a Session's ScoreSet, tallies per-account kills, scores, deaths, multiKills, and names
   and passes them to a background thread to process and
   store.
   """
    # look at score-set entries to tally per-account kills, deaths and scores for this round

    account_kills = {}
    account_deaths = {}
    account_scores = {}
    account_mkc = {}
    account_ln = {}
    account_c = {}
    for p_entry in score_set.getValidPlayers().values():
        account_id = p_entry.getPlayer().get_account_id()
        if account_id is not None:
            account_kills.setdefault(account_id, 0)  # make sure exists
            account_kills[account_id] += p_entry.accumKillCount
            account_deaths.setdefault(account_id, 0)  # make sure exists
            account_deaths[account_id] += p_entry.accumKilledCount
            account_scores.setdefault(account_id, 0)  # make sure exists
            account_scores[account_id] += p_entry.accumScore
            account_mkc.setdefault(account_id, 0)  # make sure exists
            account_mkc[account_id] += p_entry.mkc
            account_ln.setdefault(account_id, "")  # make sure exists
            account_ln[account_id] = p_entry.nameFull
            account_c.setdefault(account_id, "")  # make sure exists
            account_c[account_id] = str(p_entry.character)
        # Ok; now we've got a dict of account-ids and kills, scores, deaths, multiKills, and names.
        # Now lets kick off a background thread to load existing scores
        # from disk, do display-string lookups for accounts that need them,
        # and write everything back to disk (along with a pretty html version)
        # We use a background thread so our server doesn't hitch while doing this.
    UpdateThread(account_kills, account_deaths, account_scores, account_mkc, account_ln, account_c).start()


class UpdateThread(threading.Thread):
    def __init__(self, account_kills, account_deaths, account_scores, account_mkc, account_ln, account_c):
        threading.Thread.__init__(self)
        self._account_kills = account_kills
        self.account_deaths = account_deaths
        self.account_scores = account_scores
        self.account_mkc = account_mkc
        self.account_ln = account_ln
        self.account_c = account_c

    def run(self):
        # pull our existing stats from disk
        if os.path.exists(stats_file):
            with open(stats_file) as f:
                stats = json.loads(f.read())
        else:
            stats = {}

        # now add this batch of kills, deaths and scores to our persistant stats
        for account_id, kill_count in self._account_kills.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now increment their kills whether they were already there or not
            stats[account_id]['kills'] += kill_count
            # also incrementing the games played and adding the id
            stats[account_id]['games'] += 1
            stats[account_id]['aid'] = str(account_id)
        for account_id, killed_count in self.account_deaths.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now increment their deaths whether they were already there or not
            stats[account_id]['deaths'] += killed_count
        for account_id, score in self.account_scores.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now increment their scores whether they were already there or not
            stats[account_id]['scores'] += score
        for account_id, mkc in self.account_mkc.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now increment their mkc whether they were already there or not
            if stats[account_id]['mkc'] < mkc:
                stats[account_id]['mkc'] = mkc
        for account_id, ln in self.account_ln.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now add their last name whether they were already there or not
            stats[account_id]['lastName'] = ln
        for account_id, c in self.account_c.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'mkc': 0, 'name_html': name_html,
                                     'lastName': "", 'games': 0, 'aid': "", 'lastCharacter': ""}
            # now add their last character whether they were already there or not
            stats[account_id]['lastCharacter'] = c

        # dump our stats back to disk
        with open(stats_file, 'w') as f:
            f.write(json.dumps(stats))

        # lastly, write a pretty html version.
        # our stats url could point at something like this...
        entries = [(a['scores'], a['mkc'], a['kills'], a['deaths'], a['name_html'], a['lastName'], a['games'], a['aid'],
                    a["lastCharacter"]) for a in stats.values()]
        # this gives us a list of scores/names sorted high-to-low
        entries.sort(reverse=True)
        h1 = open(mainHTMLFile, "w")
        h1.write(html1_start)
        json_data = {}
        rank = 0
        toppers = {}
        pStats = {}
        for entry in entries:
            rank += 1
            scores = str(entry[0])
            mkc = str(entry[1])
            kills = str(entry[2])
            deaths = str(entry[3])
            name = entry[4].encode('utf-8')
            ln = entry[5].encode('utf-8')
            games = str(entry[6])
            aid = str(entry[7])
            lc = str(entry[8])
            if rank < 11:
                toppers[str(aid)] = ("#" + str(rank))
            pStats[str(aid)] = {"rank": str(rank),
                                "scores": str(scores),
                                "games": str(games),
                                "deaths": str(deaths),
                                "kills": str(kills)}
            json_data[str(rank)] = {
                "icon_url": str(str(name).split("\'>")[0]).split("src='")[1],
                "name": str(name).split("\'>")[1],
                "last_used_name": str(ln),
                "games_played": str(games),
                "account_id": str(aid),
                "rank": str(rank),
                "scores": str(scores),
                "multi_kill_count": str(mkc),
                "kills": str(kills),
                "deaths": str(deaths)
            }
            try:
                kd = str(float(kills) / float(deaths))[:3]
            except Exception:
                kd = "0"
            try:
                average_score = str(float(scores) / float(games))[:3]
            except Exception:
                average_score = "0"
            h1.write(
                "<tr id=\"" + str(rank) + "\"><td> #" + str(rank) + "</td><td>" +
                """<div class="player" id=\"""" + aid + """\" aria-hidden="true">
                            <div class="wrap"><a href=\"#""" + aid + """\">""" + name + """</a></div>
                            <div class="player-data limit-min-max">
                                <div class="player-header"><a href="http://bombsquadgame.com/scores#profile?id=""" +
                aid + """\">""" + name +
                """</a><a href="#" class="btn-close" aria-hidden="true">×</a></div>
                                <div class="player-body">
                                    <div class="column">
                                        <p class="profile">
                                            <i><u>Rank:</u></i> """ + str(rank) +
                """<br><i><u>Last used name:</u></i> """ + ln + """<br>
                                            <i><u>Games played:</u></i> """ + games +
                """<br><i><u>Total score:</u></i> """ + scores + """<br>
                                            <i><u>Average Score:</u></i> """ + average_score +
                """<br><i><u>Kills:</u></i> """ + kills + """<br>
                                        </p>
                                    </div>
                                    <div class="column">
                                        <p class="profile">
                                            <i><u>Multi Kills Count:</u></i> """ + mkc +
                """<br><i><u>Deaths:</u></i> """ + deaths + """<br><i><u>Kills per deaths:</u></i>""" +
                kd + """<br><i><u>Last character used:</u></i> """ + lc + """
                                        </p>
                                    </div>
                                </div>
                                <div class="player-footer">
                                    <a href="#"
                                       style="background: #ffb84d; border: #ffb84d; border-radius: 8px;""" +
                """ color: black; display: inline-block; font-size: 14px; padding: 8px 15px; text-decoration: none;"""
                + """text-align: center; min-width: 60px; position: relative; transition: color .1s ease;">Close</a>
                                </div>
                            </div>
                        </div>"""
                + "</td><td>" + scores + "</td><td>" + kills + "</td><td>" + deaths + "</td></tr>\n")

        h1.write(html1_end)
        h1.close()
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/toppers.json", "w")
        f.write(json.dumps(toppers))
        f.close()
        f2 = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "w")
        f2.write(json.dumps(pStats))
        f2.close()
        if botEnabled:
            b = open(bot_file, "w")
            b.write(json.dumps(json_data))
            b.close()

        # and that's it!
        print('Added ' + str(len(self._account_kills)) + ' account\'s stats entries.')
