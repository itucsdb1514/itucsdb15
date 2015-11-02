from tables import sponsors
from pages import HomePage

def InitPageFunc(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    sponsorTable.create_table()
    sponsorTable.close_con()

    return HomePage.HomePageFunc()