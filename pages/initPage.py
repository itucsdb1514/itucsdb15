from tables import sponsors
from tables import players
from tables import users
from tables import teams
from tables import stadiums
from tables import nats
from tables import stats
from tables import comments
from tables import coaches
from tables import matches
from tables import betrates
from tables import playerHistory
from tables import leagues
from pages import HomePage
from tables import outfitTable
from tables import likes

def InitPageFunc(dsn):
    for x in range(0, 2):
        playerTable = players.Players(dsn)
        playerTable.create_table()
        playerTable.close_con()
        userTable = users.Users(dsn)
        userTable.create_table()
        userTable.close_con()
        sponsorTable = sponsors.Sponsors(dsn)
        sponsorTable.create_table()
        sponsorTable.close_con()
        natTable = nats.Nats(dsn)
        natTable.create_table()
        natTable.close_con()
        statTable = stats.Stats(dsn)
        statTable.create_table()
        statTable.close_con()
        teamTable = teams.Teams(dsn)
        teamTable.create_table()
        teamTable.close_con()
        leagueTable = leagues.Leagues(dsn)
        leagueTable.create_table()
        leagueTable.close_con()
        coachTable = coaches.Coaches(dsn)
        coachTable.create_table()
        coachTable.close_con()
        stadiumTable = stadiums.Stadiums(dsn)
        stadiumTable.create_table()
        stadiumTable.close_con()
        matchTable = matches.Matches(dsn)
        matchTable.create_table()
        matchTable.close_con()
        betrateTable = betrates.Betrates(dsn)
        betrateTable.create_table()
        betrateTable.close_con()
        commentTable = comments.Comments(dsn)
        commentTable.create_table()
        commentTable.close_con()
        playerHis = playerHistory.playerHistory(dsn)
        playerHis.create_table()
        playerHis.close_con()
        outfittable=outfitTable.outfits(dsn)
        outfittable.create_table()
        outfittable.close_con()
        likeTable = likes.Likes(dsn)
        likeTable.create_table()
        likeTable.close_con()

    return HomePage.HomePageFunc()
