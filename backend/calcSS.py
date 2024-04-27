from scipy.stats import norm

def calcSS(service_level, T1, sigma_LT, sigma_D, D_avg, PC):
    alpha = 1 - service_level
    Z = abs(norm.ppf(alpha))
    
    SS = (Z * sqrt(PC/T1) * sigma_D) + (Z * sigma_LT * D_avg)
    
    return SS
