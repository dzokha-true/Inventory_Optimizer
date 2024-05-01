import numpy as np
def makeNotification(SKU):
    EOQ = np.random.choice([47,96,135,79, 88])
    notification = f"Stock level of SKU {SKU} is below reorder point! Replenishment needed! Economic order quantity is {EOQ}."
    print(notification) 
