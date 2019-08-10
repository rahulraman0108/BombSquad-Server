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
stats_file = bs.getEnvironment()['systemScriptsDirectory']+"/stats.json"  # Don't change
mainHTMLFile = webServerRootDirectory + "index.html"  # Try not to use another name instead of index
html2_file = webServerRootDirectory + str(port) + "I.html"  # Don't change
botEnabled = settings.botFile  # Don't change
bot_file = webServerRootDirectory + "bot.json"  # The name with extension of the .json file to be read by my discord bot
html1_s = ("""<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial scale=1"/>
  <link rel="stylesheet" href="2.css"/><link rel="stylesheet" href="thegr8.css"/>
  <title>Players Stats</title>
  <script>
    function show(){
  var value = document.getElementById("playerstoshow").value;
  var table = document.getElementById("table");
  var rows = table.getElementsByTagName("tr");
  var boolv = Number.isInteger(parseInt(value));
  if(boolv==true){
    for (var i = 1; i < (rows.length); i++){
      var row = document.getElementById(String(i));
      row.style.display = "";
      if(i>parseInt(value)){
        row.style.display = "none";
      }
    }
  }
  alert("Upto "+String(value)+" number of row(s) of player stats table is/are shown.");
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
        if(i>parseInt(value)){
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
function gaccount(account) {
  var inv, mhr;
  inv = document.getElementById('inv');
  mhr = new XMLHttpRequest();
  mhr.onreadystatechange = function (e) {
    if (mhr.readyState == 4 && mhr.status == 200) {
      inv.innerHTML = mhr.responseText;
      var account = document.getElementById(String(account));
      if (account!=null) {
        account.style.display = "";
      }
    }
  }
  mhr.open("GET", '"""+str(port)+"""I.html", true);
  mhr.setRequestHeader('Content-type', 'text/html');
  mhr.send();
}
function load(){
  var url_string = window.location.href;
  var url = new URL(url_string);
  var account = url.searchParams.get("account");
  if(String(account)!=="null"){
    gaccount(String(account));
  }
}
  </script>
</head>

<body onload="load()">
<section width=100%><div width=100%>
<center><img src="teaser.png" WIDTH=50% HEIGHT=24% align="middle"></center>

<span style="font-size: 22px;background-color:lightblue;">
<b>Join me: </b>
<!-- Your links and buttons to be here -->
</span>

<b><p id="counter" class="counter"></p></b>

<section id="inv" class="background">
</section>
<section id="full">
<br>
  <center>
  <div style="background-color:lightblue"><b>`""" + str(partyName) + """` party's player stats.<br>
    Number of rows of player of the following stats table to show:
    </b><input type="number" id="playerstoshow" onchange="show()" value="100" />
  <input type="text" id="searchInput" onkeyup="search()" placeholder="Search for names.." title="Type in a name"></div>
  </center>
<br>
<table class="background" id="table" width=100%>
<tr><th><u>Rank</u></th><th><u>Player</u></th><th><u>Scores</u></th><th><u>Avg<br>Score</u></th>""" +
           """<th><u>Kills</u></th><th><u>K/D</u></th><th><u>Deaths</u></th></tr>\n""")


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
        h1.write(html1_s)
        h2 = open(html2_file, "w")
        json_data = {}
        rank = 0
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/toppers.json", "w")
        toppers = {}
        f2 = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "w")
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
            if rank == 1:
                toppers[str(aid)] = "1st Ranker\n"
            elif rank == 2:
                toppers[str(aid)] = "2nd Ranker\n"
            elif rank == 3:
                toppers[str(aid)] = "3rd Ranker\n"
            elif rank < 6:
                toppers[str(aid)] = (str(rank) + "th Ranker\n")
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
            h1.write(
                "<tr id=\"" + str(rank) + "\"><td> #" + str(rank) + "</td><td><a href=\"?account=" + aid +
                "\">" + str(name) + "</a></td><td>" + scores + "</td><td>" + str(
                    int(scores) / int(games)) + "</td><td>" + kills + "</td><td>" + kd + "</td><td>" + deaths +
                "</td></tr>\n")
            h2.write(
                "<div id=\"" + aid + "\" style=\"display: none;background-color:lightblue;\"><center>" +
                "<span><b>`"+ str(partyName) + "` party's player's individual stats.</b></span><br><strong>Rank: " +
                "</strong>" + str(rank) + " <strong>Common name: </strong><a href=\"http://bombsquadgame.com/scores" +
                "#profile?id=" + aid + "\">" + str(name) + "</a> <strong>Last used name: </strong>" + str(ln) + "<br>" +
                "<strong>Games played: </strong>" + games + " <strong>Total score: </strong>" + scores + " <strong>" +
                "Average Score: </strong>" + str(int(scores) / int(games)) + "<br><strong>Kills: </strong>" + kills +
                " <strong>Multi Kills Count: </strong>" + mkc + " <strong>Deaths: </strong>" + deaths + " <strong>" +
                "Kills per deaths: </strong>" + kd + "<br><strong>Last character used: " + "</strong>" + lc +
                "</center></div>")
        h1.write("""</table></section>
</div></section>
<script>var countDownDate = new Date("Jun 30, 2019 24:00:00").getTime(); var x = setInterval(function() { var now = new Date().getTime(); var distance = countDownDate - now; var days = Math.floor(distance / (1000 * 60 * 60 * 24));  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));  document.getElementById("counter").innerHTML = "Season Ends In " + days + "Days " + hours + "Hrs ";  if (distance < 0) {  clearInterval(x); document.getElementById("counter").innerHTML = "Season Results"; } }, 1000); 
</script></body>
</html>""")
        h1.close()
        h2.close()
        f.write(json.dumps(toppers))
        f.close()
        f2.write(json.dumps(pStats))
        f2.close()
        if botEnabled:
            b = open(bot_file, "w")
            b.write(json.dumps(json_data))
            b.close()

        # aaand that's it!
        print('Added ' + str(len(self._account_kills)) + ' account\'s stats entries.')
