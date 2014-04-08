# Fantasy Moneyball

## What?

An ongoing project consisting of scripts and web-app for viewing and analyzing our fantasy baseball league hosted on ESPN Fantasy Baseball

## Why? 

ESPN Fantasy & Games provides effective tools for draft prep, live drafts and league and roster management. However, we saw a distance between the detail of the provided team stats relative to the volume of available baseball Sabermetrics.

## ESPN API

Below is some documentation on  of the JSON API endpoints used by ESPN Fantasy Sports to populate their own client views through the fantasy baseball portal. Your experience may vary, so please share any comments!

### Daily Stats

BASE URL:

 - http://games.espn.go.com/flb/playertable/prebuilt/activestats?"

REQUIRED PARAMETERS:

 - INVARIANT:
   + view='stats'
   + mode='bydate'

 - INVARIANT FOR LEAGUE:
   + leagueId=[INTEGER]

 - VARIABLE:
   + filter=[1=batting, 2=pitching]
   + teamId=[INTEGER]
   + start=[YYYYMMDD] (20140322 for 2014)
   + end=[YYYYMMDD] (20141231 for 2014)

### Daily Roster

BASE URL:

 - http://games.espn.go.com/flb/playertable/prebuilt/manageroster?

REQUIRED PARAMS:

 - INVARIANT:
   + view=stats
   + managingIr=false
   + droppingPlayers=false
   + asLM=false
 - INVARIANT FOR LEAGUE:
   + leagueId=[INTEGER]
 - VARIABLE:
   + teamId=[INTEGER]
   + scoringPeriodId=[INTEGER 1-# games in season] (191 for 2014)
   + seasonId=[YYYY]

### Condensed roster

BASE = "http://games.espn.go.com/flb/boxscorequick?"

- INVARIANT:
   + view=scoringperiod
   + version=quick
 - INVARIANT FOR LEAGUE:
   + leagueId=[INTEGER]
 - VARIABLE:
   + teamId=[INTEGER]
   + scoringPeriodId=[INTEGER 1-# games in season] (191 for 2014)
   + seasonId=[YYYY]


