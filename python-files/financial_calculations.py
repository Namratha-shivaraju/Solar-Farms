
import numpy as np
import numpy_financial as npf

def calculate_npv(analysisPeriod, production, turnKeyCosts, variableCosts, ppa, upfront):
    # 示例：将所有值转换为浮点数进行计算
    analysisPeriod = float(analysisPeriod)
    production = float(production)
    turnKeyCosts = float(turnKeyCosts)
    variableCosts = float(variableCosts)
    ppa = float(ppa)
    upfront = float(upfront)
    
    # 计算年度现金流
    revenue_per_year = production * ppa
    costs_per_year = production * variableCosts
    cash_flow = revenue_per_year - costs_per_year
    
    cash_flows = [-turnKeyCosts - upfront] + [cash_flow] * int(analysisPeriod)
    rate = 0.1  # 假设折现率为10%
    
    npv = npf.npv(rate, cash_flows)
    return npv

def calculate_irr(cash_flows):
    return npf.irr(cash_flows)
