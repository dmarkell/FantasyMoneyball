import bs4
import csv
import json
import datetime
import os
import urllib
import urllib2

from league_info import *


BASE = "http://games.espn.go.com/flb/playertable/prebuilt/activestats?"
params = dict(leagueId=LEAGUE_ID, view='stats', mode='bydate', filter=2,
    start=20140322, end=20141231)

class Stats:
    
    def __init__(self):
        self.stats = {}
        
        if os.name == 'posix':
            self.FILEPATH = '/Users/devinmarkell/Dropbox/Public/baseball'
        else:
            self.FILEPATH = 'C:\\Users\\dmarkell.BOC\\Dropbox\\Public\\baseball'

        self.FILENAME = 'active_stats'
        for team in TEAMS:
            self.get_team(team)
    
    def td_cont(self, td):
        return td.get_text()

    def get_team(self, team):
        params['teamId'] = team
        enc_params = urllib.urlencode(params)
        url = BASE + enc_params
        resp = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(resp)
        head_row = soup.find("tr", "tableSubHead")
        labels = head_row.findAll("td")
        labels = map(self.td_cont, labels)
        section_break = labels[2:].index(u'')
        for ix, name in enumerate(labels[2:]):
            if ix < section_break:
                labels[ix + 2] = "b_{}".format(name)
            elif ix > section_break:
                labels[ix + 2] = "p_{}".format(name)
        self.labels = filter(None, labels)[1:]
        trs = soup.findAll("tr", "tableBody")
        # Map list of tr objects to a list of (key, value) tuples
        days = map(self.get_day, trs)
        # Filter out invalid rows
        days = filter(lambda x: x[0] <> None, days)
        # Assign team's stats to the stats dictionary
        for date, stats in days:
            entries = self.stats.get(date, {})
            entries[str(team)] = stats
            self.stats[date] = entries

    def valid_row(self, tds):
        """Checks tds array and returns True if row is valid, False if not"""

        valid_row = True
        if self.td_cont(tds[0]) == 'TOTALS':
            valid_row = False
        elif self.td_cont(tds[1]) == '--':
            valid_row = False
        elif self.td_cont(tds[10]) == '--':
            valid_row = False

        return valid_row

    def get_day(self, tr):
        """Returns dict of day's stats using labels"""

        day_key = None
        day_stats = {}
        tds = tr.findAll('td')
        if self.valid_row(tds):
            tds = map(self.td_cont, tds)
            tds = filter(None, tds)
            fmt = '%A, %B %d'
            dt = datetime.datetime.strptime(tds[0], fmt)
            fmt = '%m-%d'
            day_key = "2014-{}".format(dt.strftime(fmt))
            tds = tds[1:]
            for ix, label in enumerate(self.labels):
                day_stats[label] = tds[ix]

        return day_key, day_stats

    def write_stats_json(self):
        json_path = "{}/{}.txt".format(self.FILEPATH, self.FILENAME)
        csv_path = "{}/{}.csv".format(self.FILEPATH, self.FILENAME)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = dict(last_updated=timestamp, stats=self.stats)
        output = json.dumps(data)
        with open(json_path, 'w') as f:
            f.write(output)

    def write_stats_csv(self):
        labels = self.stats.values()[0].values()[0].keys()
        header = "date,teamId,{}".format(','.join(labels))
        self.csv = []
        for date, teams in self.stats.items():
            for team, stats in teams.items():
                values = stats.values()
                values.insert(0, team)
                values.insert(0, date)
                self.csv.append(tuple(values))

        self.csv = sorted(self.csv, reverse=True)
        with open(csv_path, 'w') as f:
            f.write(header + '\n') 
            for entry in self.csv:
                f.write(','.join(entry) + '\n')

def main():
    stats = Stats()
    stats.write_stats_json()
    

if __name__ == "__main__":
    main()
