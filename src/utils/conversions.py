# utils/conversions.py

def satoshi_to_btc(satoshi):
    """
    Convert satoshi to bitcoin
    :param satoshi: amount in satoshi
    :return: amount in bitcoin
    """
    return satoshi / 100000000

def btc_to_satoshi(btc):
    """
    Convert bitcoin to satoshi
    :param btc: amount in bitcoin
    :return: amount in satoshi
    """
    return int(btc * 100000000)