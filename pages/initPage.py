from tables import sponsors
from tables import players
from tables import teams
from tables import stadiums
from tables import nats
from tables import comments
from tables import coaches
from pages import HomePage

def InitPageFunc(dsn):
    for x in range(0, 2):
        playerTable = players.Players(dsn)
        playerTable.create_table()
        playerTable.close_con()
        sponsorTable = sponsors.Sponsors(dsn)
        sponsorTable.create_table()
        sponsorTable.close_con()
        natTable = nats.Nats(dsn)
        natTable.create_table()
        natTable.close_con()
        teamTable = teams.Teams(dsn)
        teamTable.create_table()
        teamTable.close_con()
        coachTable = coaches.Coaches(dsn)
        coachTable.create_table()
        coachTable.close_con()
        stadiumTable = stadiums.Stadiums(dsn)
        stadiumTable.create_table()
        stadiumTable.close_con()
        commentTable = comments.Comments(dsn)
        commentTable.create_table()
        commentTable.close_con()

    return HomePage.HomePageFunc()