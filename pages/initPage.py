from tables import sponsors
from tables import players
from tables import teams
from tables import stadiums
from tables import comments
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
    stadiumTable = stadiums.Stadiums(dsn)
    stadiumTable.create_table()
    stadiumTable.close_con()
    commentTable = comments.Comments(dsn)
    commentTable.create_table()
    commentTable.close_con()

    return HomePage.HomePageFunc()