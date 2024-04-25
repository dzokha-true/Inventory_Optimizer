from math import sqrt, ceil

def getEOQ(D, S, H):
    EOQ = ceil(sqrt(2*D*S/H))
    return EOQ