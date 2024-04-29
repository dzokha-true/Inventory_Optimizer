# This function takes in a SKU and checks if it needs a reorder. A notification is returned if it does.

import numpy as np
import pandas as pd
import datetime
from scipy.stats import norm
from math import sqrt, ceil

def getEOQ(D, S, H):
    EOQ = ceil(sqrt(2*D*S/H))
    return EOQ

def calcSS(service_level, T1, sigma_LT, sigma_D, D_avg, PC):
    alpha = 1 - service_level
    Z = abs(norm.ppf(alpha))
    
    SS = (Z * sqrt(PC/T1) * sigma_D) + (Z * sigma_LT * D_avg)
    return SS

def calcROP(muD, muLT, SS):
    ROP = muD * muLT + SS
    return ROP

def reorderNeeded(Stock, ROP):
    if Stock < ROP:
        return True
    else:
        return False
    
def predictDemand(SKU):
    
    # Step 0: extract historical sales data from database
    """
    NEED DATA HELPER FUNCTION
    """
    data = getData(SKU)
    
    # Step 1: generate regressors
    
    regressors = pd.DataFrame()
    regressors['sin_day'] = np.sin(2 * pi * np.arange(len(data)))
    regressors['cos_day'] = np.cos(2 * pi * np.arange(len(data)))
    regressors['sin_week'] = np.sin(2 * pi * np.arange(len(data)) / 7)
    regressors['cos_week'] = np.cos(2 * pi * np.arange(len(data)) / 7)
    regressors['sin_biweekly'] = np.sin(2 * pi * np.arange(len(data)) / 14)
    regressors['cos_biweekly'] = np.cos(2 * pi * np.arange(len(data)) / 14)
    regressors['sin_month'] = np.sin(2 * pi * np.arange(len(data)) / 30)
    regressors['cos_month'] = np.cos(2 * pi * np.arange(len(data)) / 30)
    regressors['sin_bimonthly'] = np.sin(2 * pi * np.arange(len(data)) / 60)
    regressors['cos_bimonthly'] = np.cos(2 * pi * np.arange(len(data)) / 60)
    regressors['sin_quarter'] = np.sin(2 * pi * np.arange(len(data)) / 90)
    regressors['cos_quarter'] = np.cos(2 * pi * np.arange(len(data)) / 90)
    regressors['sin_third'] = np.sin(2 * pi * np.arange(len(data)) / 120)
    regressors['cos_third'] = np.cos(2 * pi * np.arange(len(data)) / 120)
    regressors['sin_half'] = np.sin(2 * pi * np.arange(len(data)) / 180)
    regressors['cos_half'] = np.cos(2 * pi * np.arange(len(data)) / 180)
    regressors['sin_year'] = np.sin(2 * pi * np.arange(len(data)) / 365)
    regressors['cos_year'] = np.cos(2 * pi * np.arange(len(data)) / 365)
    regressors['sin_biannual'] = np.sin(2 * pi * np.arange(len(data)) / 730)
    regressors['cos_biannual'] = np.cos(2 * pi * np.arange(len(data)) / 730)
    regressors['day'] = data['Date'].dt.day
    regressors['month'] = data['Date'].dt.month
    regressors['year'] = data['Date'].dt.year
    regressors = sm.add_constant(regressors)
    
    # Step 2: fit predictive model
    
    wls_model = sm.WLS(data['Quantity'], regressors)
    wls_fit = wls_model.fit()
    
    # Step 3: initialize array of dates covering the next year and fit the model to predict demand for them
    
    prediction_date_range = 365 # default is to predict one year ahead
    
    today = date.today()

    prediction_dates = np.empty(prediction_date_range, dtype = 'object')
    
    for i in range(0,prediction_date_range):
        prediction_dates[i] = today + timedelta(days = i)
    
    prediction_data = pd.DataFrame()
    prediction_data['sin_day'] = np.sin(2 * pi * np.arange(prediction_date_range))
    prediction_data['cos_day'] = np.cos(2 * pi * np.arange(prediction_date_range))
    prediction_data['sin_week'] = np.sin(2 * pi * np.arange(prediction_date_range) / 7)
    prediction_data['cos_week'] = np.cos(2 * pi * np.arange(prediction_date_range) / 7)
    prediction_data['sin_biweekly'] = np.sin(2 * pi * np.arange(prediction_date_range) / 14)
    prediction_data['cos_biweekly'] = np.cos(2 * pi * np.arange(prediction_date_range) / 14)
    prediction_data['sin_month'] = np.sin(2 * pi * np.arange(prediction_date_range) / 30)
    prediction_data['cos_month'] = np.cos(2 * pi * np.arange(prediction_date_range) / 30)
    prediction_data['sin_bimonthly'] = np.sin(2 * pi * np.arange(prediction_date_range) / 60)
    prediction_data['cos_bimonthly'] = np.cos(2 * pi * np.arange(prediction_date_range) / 60)
    prediction_data['sin_quarter'] = np.sin(2 * pi * np.arange(prediction_date_range) / 90)
    prediction_data['cos_quarter'] = np.cos(2 * pi * np.arange(prediction_date_range) / 90)
    prediction_data['sin_third'] = np.sin(2 * pi * np.arange(prediction_date_range) / 120)
    prediction_data['cos_third'] = np.cos(2 * pi * np.arange(prediction_date_range) / 120)
    prediction_data['sin_half'] = np.sin(2 * pi * np.arange(prediction_date_range) / 180)
    prediction_data['cos_half'] = np.cos(2 * pi * np.arange(prediction_date_range) / 180)
    prediction_data['sin_year'] = np.sin(2 * pi * np.arange(prediction_date_range) / 365)
    prediction_data['cos_year'] = np.cos(2 * pi * np.arange(prediction_date_range) / 365)
    prediction_data['sin_biannual'] = np.sin(2 * pi * np.arange(prediction_date_range) / 730)
    prediction_data['cos_biannual'] = np.cos(2 * pi * np.arange(prediction_date_range) / 730)
    prediction_data['Day'] = np.int32(prediction_dates.dt.day)
    prediction_data['Month'] = np.int32(prediction_dates.dt.month)
    prediction_data['Year'] = np.int32(prediction_dates.dt.year)

    wls_predictions = wls_fit.predict(prediction_data)
    
    # Step 4: generate predicted demand dataframe
    
    predicted_demand = pd.DataFrame()
    predicted_demand['Date'] = prediction_dates
    predicted_demand['Quantity'] = np.array(np.ceil(wls_predictions))
    
    # Step 5: plot predictions
    
    generate_confidence_interval = True    # set to True to generate a confidence interval alongside the plot
    plt.plot(predicted_demand['Date'], predicted_demand['Quantity'], color = 'b')
    plt.xticks(rotation=12, ha="right")
    plt.xlabel("Date")
    plt.ylabel("Expected Sales")
    plt.title(f"Predicted Demand for SKU {SKU}")
    
    if generate_confidence_interval:
        Qinv = t.ppf(0.005, prediction_date_range-1)
        epsilon = -sqrt(np.var(data['Quantity']))*Qinv*(1/sqrt(prediction_date_range))
        plt.fill_between(predicted_demand['Date'],(wls_predictions - epsilon), (wls_predictions + epsilon), color = 'b', alpha = 0.2)
        plt.legend(["Predicted Demand", "99% Confidence Interval"])

    # Path - currently saves to local directory
    plt.savefig(f"{SKU}_demand_graph.png")
    
    # Step 6: return data
    
    return predicted_demand

def checkForReorder(SKU):
    
    # 1. Call predictor module to generate predicted demand
    
    predicted_demand = predictDemand(SKU)
    start_date = predicted_demand['Date'][0]
    end_date = predicted_demand['Date'][len(predicted_demand)-1]
    
    num_days = (end_date - start_date).days
    num_years = num_days / 365.25
    num_weeks = num_days / 7
    
    # 3. Extract necessary information from database and store necessary parameters in variables
    # As with 1 and 2, ultimate implementation depends on where data is stored

    service_level = 0.95
    T1 = 7 
    fixed_order_cost = 40
    fixed_holding_cost = 100
    
    # call helper functions to find quantity on hand and quantity on order
    quantity_on_order = sku_on_order(SKU)
    quantity_on_hand = stock(SKU)
    quantity_available = quantity_on_hand + quantity_on_order
    
    mean_daily_demand_past = mean_daily(SKU)
    mean_daily_demand_predicted = np.sum(predicted_demand['Quantity'])/num_days
    mean_daily_demand = np.mean(mean_daily_demand_past, mean_daily_demand_predicted)
    
    mean_weekly_demand_past = mean_weekly(SKU)
    mean_weekly_demand_predicted = np.sum(predicted_demand['Quantity'])/num_weeks
    mean_weekly_demand = np.mean(mean_weekly_demand_past, mean_weekly_demand_predicted)
    
    # call total_demand helper function
    annual_demand = total_demand(SKU)
    
    sd_weekly_demand_past = sd_weekly(SKU)
    sd_demand_predicted = np.std(predicted_demand)
    sd_weekly_demand = np.mean(sd_weekly_demand_past, sd_weekly_demand_predicted)
    
    mean_lead_time = 14 #days
    sd_lead_time = 3 # days
    
    performance_cycle_additional_days = 0   # customizable parameter that accounts for additional frictions beyond lead time
    performance_cycle = mean_lead_time + performance_cycle_additional_days
    
    # 4. Compute safety stock
    
    safety_stock = calcSS(service_level, T1, sd_lead_time, sd_weekly_demand, mean_weekly_demand, performance_cycle)
    
    # 5. Compute reorder point
    
    ROP = calcROP(mean_daily_demand, mean_lead_time, safety_stock)
    
    # 6. Check if reorder is needed
    
    reorder_needed = reorderNeeded(quantity_available, ROP)
    
    if reorder_needed:
        EOQ = getEOQ(mean_annual_demand, fixed_order_cost, fixed_holding_cost)
        notification = notification = f"Stock level of SKU {SKU} is below reorder point! Replenishment needed! Economic order quantity is {EOQ}."
        print notification
    else:
        print ""