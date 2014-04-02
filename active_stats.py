import bs4
import json
from datetime import datetime
import urllib
import urllib2


BASE = "http://games.espn.go.com/flb/playertable/prebuilt/activestats?"
params = dict(leagueId=183180, view='stats', mode='bydate', filter=2,
    start=20140322, end=20141231)
FILENAME = 'active_stats1.txt'

class Stats:
    
    def __init__(self):
        self.stats = {}
        TEAMS = [1, 2, 3, 4, 5,
                 6, 7, 8, 9, 11] 
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
        self.labels = filter(None, labels)
        trs = soup.findAll("tr", "tableBody")
        days = map(self.get_day, trs)
        days = filter(None, days)
        self.stats[str(team)] = days
    
    def get_day(self, tr):
        day = {}
        tds = tr.findAll('td')
        if self.td_cont(tds[0]) <> 'TOTALS' and self.td_cont(tds[1]) <> '--' and self.td_cont(tds[10]) <> '--':
            tds = map(self.td_cont, tds)
            tds = filter(None, tds)
            fmt = '%A, %B %d'
            dt = datetime.strptime(
            tds[0], fmt)
            fmt = '%m-%d'
            day['date'] = "2014-{}".format(
            dt.strftime(fmt))
            for ix, key in enumerate(
            self.labels[1:]):
                day[key] = tds[ix + 1]
        return day

def save_stats(stats):
    with open(FILENAME, 'w') as f:
        data = json.dumps(stats.stats)
        f.write(data)

#with open(FILENAME, 'r') as f:
#    f.read()

def main():
    stats = Stats()
    print(stats.stats.keys(), stats.stats.values()[0])

if __name__ == "__main__":
    main()
