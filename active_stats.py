import bs4
import json
import datetime
import urllib
import urllib2


BASE = "http://games.espn.go.com/flb/playertable/prebuilt/activestats?"
params = dict(leagueId=183180, view='stats', mode='bydate', filter=2,
    start=20140322, end=20141231)


class Stats:
    
    def __init__(self):
        self.stats = {}
        TEAMS = [1, 2, 3, 4, 5,
                 6, 7, 8, 9, 11] 
        self.FILENAME = 'active_stats.txt'
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
        self.labels = filter(None, labels)[1:]
        trs = soup.findAll("tr", "tableBody")
        # Map list of tr objects to a list of (key, value) tuples
        days = map(self.get_day, trs)
        # Filter out invalid rows
        days = filter(lambda x: x[0] <> None, days)
        # Assign team's stats to the stats dictionary
        self.stats[str(team)] = dict(days)

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

    def write_stats(self):
        with open(self.FILENAME, 'w') as f:
            data = json.dumps(self.stats)
            f.write(data)

    def __str__(self):
        stats = self.stats
        output = ""

        for ix, (team, days) in enumerate(stats.items()):
            sorted_stats = sorted(days.items(), reverse=True)
            date, latest = sorted_stats[1]
            size = len(latest)
            fmt = "\t{:>5}"*size 
            if ix == 0:

                output += "{}\n".format(date)
                output += "       "
                output += fmt.format(*latest.keys()) + "\n"
            output += "Team {:2}:".format(team)
            output += fmt.format(*latest.values()) + "\n"            

        return output

def main():
    stats = Stats()
    stats.write_stats()
    print(stats)

if __name__ == "__main__":
    main()
