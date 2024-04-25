# This function takes in a SKU and checks if it needs a reorder. A notification is returned if it does.

import numpy as np
import pandas as pd

def checkForReorder(SKU):
    # 1. Check for predictions
    predictions_unavailable = False  # placeholder - change to add logic after integration

    if (predictions_unavailable):
        raise noPredictionsException
        
    # 2. Fetch predictions for the next 4 weeks' demand
    # As with 1, implementation depends on where the data will be stored
    
    # 3. Extract necessary information from database and store necessary parameters in variables
    # As with 1 and 2, ultimate implementation depends on where data is stored

    service_level = 0.95
    T1 = 7 
    fixed_order_cost = 40
    fixed_holding_cost = 100
    
    quantity_on_order = # from ORDERS database
    quantity_on_hand = # from STOCK database
    quantity_available = quantity_on_hand + quantity_on_order
    
    mean_daily_demand_past = # from SALES database
    mean_daily_demand_predicted = # from PREDICTIONS
    mean_daily_demand = np.mean(mean_daily_demand_past, mean_daily_demand_predicted)
    
    mean_weekly_demand_past = # from SALES database
    mean_weekly_demand_predicted = # from PREDICTIONS
    mean_weekly_demand = np.mean(mean_weekly_demand_past, mean_weekly_demand_predicted)
    
    annual_demand = # from SALES database
    
    sd_weekly_demand_past = # from SALES database
    sd_weekly_demand_predicted = # from PREDICTIONS
    sd_weekly_demand = np.mean(sd_weekly_demand_past, sd_weekly_demand_predicted)
    
    mean_lead_time = # from ORDERS database
    sd_lead_time = # from ORDERS database
    
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
        return notification
    else:
        return False
    