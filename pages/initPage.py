from tables import sponsors
from tables import players
from pages import HomePage

def InitPageFunc(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    sponsorTable.create_table()
    sponsorTable.close_con()
    playerTable = players.Players(dsn)
    playerTable.create_table()
    playerTable.close_con()

    return HomePage.HomePageFunc()