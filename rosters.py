import bs4
import json
import datetime
from pprint import pprint
import urllib
import urllib2

from league_info import *

#TEAMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]

class Lineup:

    def __init__(self, team, scoring_period, year=2013):
        self.error = False
        self.team = team
        self.scoring_period = scoring_period
        self.year = year
        self.get_lineup()

    def get_lineup(self):
        BASE = "http://games.espn.go.com/flb/boxscorequick?"
        params = dict(leagueId=LEAGUE_ID, view='scoringperiod', 
            version='quick')
        params['seasonId'] = self.year
        params['teamId'] = self.team
        params['scoringPeriodId'] = self.scoring_period
        url = BASE + urllib.urlencode(params)
        source = urllib2.urlopen(url).read()
        if source.find('games-error-red-alert') <> -1:
            self.error = True
            return
        resp = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(resp)

        header = soup.find("div", "games-pageheader").find("h1")
        date = header.find("em").get_text()
        if date == "Offseason":
            self.error = True
            return
        fmt = '%A, %B %d'
        dt = datetime.datetime.strptime(date, fmt)
        fmt = '%m-%d'
        self.date = "{}-{}".format(self.year, dt.strftime(fmt))

        trs = soup.findAll("tr", "pncPlayerRow")
        tds = map(lambda x: x.find('td'), trs)
        self.lineup = map(self.get_player, trs)

    def get_player(self, tr):
        player_name = None
        slot_node = tr.find("td", "playerSlot")
        slot = slot_node.get_text()
        player_id = slot_node.get('id') # No id if slot empty
        if player_id:
            player_id = player_id.split('_')[1]
            name_node = tr.find("td", "playertablePlayerName")
            player_name = name_node.find("a").get_text()

        return slot, player_id, player_name

    def csv(self):
        output = ""
        for row in self.lineup:
            output += "{},{},{},{},{},{}\n".format(
                self.team, self.date, self.scoring_period, *row)

        return output

def main():
    year = 2014
    output = "teamId,date,scoringPeriodId,slot,playerId,playerName\n"
    with open("{}_lineups.csv".format(year), 'w') as f:
        f.write(output)
    for team in TEAMS:
        scoring_period = 1
        while scoring_period <= 12:
            lineup = Lineup(team, scoring_period, year=year)
            if lineup.error:
                break
            output = lineup.csv()
            with open("{}_lineups.csv".format(year), 'a') as f:
                f.write(output)
            scoring_period += 1

for team in TEAMS:
    print team

#if __name__ == "__main__":
#    main()
