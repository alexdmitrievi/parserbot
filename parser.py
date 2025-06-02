from bankrotbaza_parser import fetch_bankrotbaza
from lot_online_parser import fetch_lot_online
from fabrikant_parser import fetch_fabrikant
from torgilist_parser import fetch_torgilist

def fetch_lots():
    return (
        fetch_bankrotbaza()
        + fetch_lot_online()
        + fetch_fabrikant()
        + fetch_torgilist()
    )



