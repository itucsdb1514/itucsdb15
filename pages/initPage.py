from tables import sponsors
from tables import players
from tables import teams
from pages import HomePage

def InitPageFunc(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    sponsorTable.create_table()
    sponsorTable.close_con()
    playerTable = players.Players(dsn)
    playerTable.create_table()
    playerTable.close_con()
    teamTable = teams.Teams(dsn)
    teamTable.create_table()
    teamTable.close_con()

    return HomePage.HomePageFunc()