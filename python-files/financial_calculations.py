# import numpy as np
# import numpy_financial as npf

# def round_floats(obj, precision=2):
#     if isinstance(obj, float):
#         return round(obj, precision)
#     elif isinstance(obj, dict):
#         return {k: round_floats(v, precision) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [round_floats(item, precision) for item in obj]
#     else:
#         return obj

# def calculate_total_production(analysis_period, production):
#     yearly_production = [0]  # Production is 0 for the first year
#     for year in range(1, analysis_period):
#         yearly_production.append(production)
#     total_production = sum(yearly_production)
#     result = {"yearly_production":yearly_production, "total_production":total_production}
#     return round_floats(result)

# def calculate_capex(analysis_period, capex, debt_percent):
#     senior_debt = capex * (debt_percent/100)
#     equity = capex - senior_debt
#     funding = equity + senior_debt
#     yearly_capex = [capex] + [0] * (analysis_period - 1)
#     yearly_funding = [capex] + [0] * (analysis_period - 1)
#     total_capex = sum(yearly_capex)
#     result = {"yearly_capex":yearly_capex, "total_capex":total_capex, "funding":funding, "yearly_funding":yearly_funding, "senior_debt": senior_debt, "equity":equity}

#     return round_floats(result)

# def operating_activities(analysis_period, production, ppa_price, opex):
    
#     revenues_per_year = [0]  # Initialize with 0 for the initial year
#     opex_per_year = [0]      # Initialize with 0 for the initial year
#     ebitda_per_year = [0]    # Initialize with 0 for the initial year
#     total_revenue = 0
#     total_opex = 0
#     total_ebitda = 0

#     for year in range(1, analysis_period + 1):
#         yearly_revenue = production * ppa_price
#         revenues_per_year.append(yearly_revenue)
#         total_revenue += yearly_revenue

#         yearly_opex = production * opex
#         opex_per_year.append(-yearly_opex)
#         total_opex += yearly_opex

#         yearly_ebitda = yearly_revenue - yearly_opex  # Since opex is negative, adding it
#         ebitda_per_year.append(yearly_ebitda)
#         total_ebitda += yearly_ebitda

#     result = {"revenues_per_year": revenues_per_year, "total_revenue": total_revenue,"opex_per_year": opex_per_year,"total_opex": total_opex,"ebitda_per_year": ebitda_per_year,"total_ebitda": total_ebitda}
#     return round_floats(result)

# def tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years):
#     capex_info = calculate_capex(analysis_period, capex, debt_percent)
#     senior_debt = capex_info["senior_debt"]/repayment_years
#     operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    
    
#     interest_expense_per_year = [0]
#     geared_tax_income_per_year = [0]
#     tax_paid_per_year = [0]
#     depreciation_per_year = [0] 

#     for year in range(1, analysis_period + 1):

#         if year <= repayment_years:
#             # Calculate yearly interest expense till repayment years
#             yearly_interest_expense = senior_debt * interest_rate * (repayment_years + 1 - year) / 100
#             yearly_depreciation = capex / depreciation_y

#             yearly_geared_tax_income = operating_info["ebitda_per_year"][year] - yearly_interest_expense - yearly_depreciation
#         else:
#             # After repayment years, interest expense becomes 0
#             yearly_interest_expense = 0
#             yearly_depreciation = 0
#             yearly_geared_tax_income = 0

#         interest_expense_per_year.append(-yearly_interest_expense)

        
#         depreciation_per_year.append(-yearly_depreciation)
        
#         geared_tax_income_per_year.append(yearly_geared_tax_income)
        
        
#         yearly_tax_paid = yearly_geared_tax_income * (tax_rate/100)
#         tax_paid_per_year.append(-yearly_tax_paid)
    
#     result = {
#         "interest_expense_per_year": interest_expense_per_year,
#         "depreciation_per_year": depreciation_per_year,
#         "geared_tax_income_per_year": geared_tax_income_per_year,
#         "tax_paid_per_year": tax_paid_per_year
#     }

#     return round_floats(result)

# def tax_paid_ug(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate):
#     operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    
#     depreciation_per_year = [0] 
#     geared_taxable_income_per_year = [0]
#     tax_paid_ug_per_year = [0]


#     for year in range(1, analysis_period + 1):

#         yearly_depreciation = capex / depreciation_y
#         depreciation_per_year.append(-yearly_depreciation)

#         geared_taxable_income = operating_info["ebitda_per_year"][year] - yearly_depreciation
#         geared_taxable_income_per_year.append(geared_taxable_income)
        
        
#         tax_paid_ug = geared_taxable_income * (tax_rate/100)
#         tax_paid_ug_per_year.append(-tax_paid_ug)
    
#     result =  {
#         "depreciation_per_year": depreciation_per_year,
#         "geared_taxable_income_per_year": geared_taxable_income_per_year,
#         "tax_paid_ug_per_year": tax_paid_ug_per_year
#     }

#     return round_floats(result)

# def calculate_debt(analysis_period, repayment_years, capex, debt_percent):
#     capex_info = calculate_capex(analysis_period, capex, debt_percent)
#     senior_debt = capex_info["senior_debt"]
#     opening_balance = [0] * analysis_period
#     principal_payment = [0] * analysis_period
#     closing_balance = [0] * analysis_period
#     opening_balance[0] = senior_debt

#     if repayment_years > 0:
#         repayment_amount = senior_debt
#         yearly_principal_payment = repayment_amount / repayment_years
#     else:
#         yearly_principal_payment = 0

#     for year in range(analysis_period):
#         if year > 0:
#             opening_balance[year] = closing_balance[year - 1]
        
#         if year < repayment_years:
#             principal_payment[year] = yearly_principal_payment
#         else:
#             principal_payment[year] = 0
        
#         closing_balance[year] = opening_balance[year] - principal_payment[year]

#     result = {
#         "opening_balance": opening_balance,
#         "principal_payment": principal_payment,
#         "closing_balance": closing_balance
#     }

#     return round_floats(result)



# def cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years):
#     # Calculate Total CAPEX and Funding
#     capex_info = calculate_capex(analysis_period, capex, debt_percent)
#     tcapex = capex_info["yearly_capex"]
#     tfunding = capex_info["yearly_funding"]
#     operating_info = operating_activities(analysis_period, production, ppa_price, opex)
#     total_ebitda = operating_info["ebitda_per_year"]
#     debt_service_per_year = [0]
    
#     cash_flow_after_funding_before_tax = [0] + [ebitda - capex - funding for ebitda, capex, funding in zip(total_ebitda[1:], tcapex[1:], tfunding[1:])]


#     tax_info = tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#     total_tax_paid = tax_info["tax_paid_per_year"]

#     cash_flow_available_for_debt_service = [cf + tax for cf, tax in zip(cash_flow_after_funding_before_tax, total_tax_paid)]
   
#     senior_debt = capex_info["senior_debt"]  
#     principal_per_year = senior_debt / repayment_years
    
#     interest_per_year = [0]  # Interest for the initial year is 0
#     for year in range(1, repayment_years + 1):
#         interest = principal_per_year * interest_rate * (repayment_years + 1 - year) / 100
#         interest_per_year.append(interest)
#         ds = interest + (principal_per_year if year <= repayment_years else 0)
#         debt_service_per_year.append(ds)
#     interest_per_year.extend([0] * (analysis_period - len(interest_per_year)))  # Fill the rest with 0 if analysis_period > repayment_years
            
#     # Cash Flow Available to Equity
#     cash_flow_available_to_equity = [cf - ds for cf, ds in zip(cash_flow_available_for_debt_service, debt_service_per_year)]

#     result = {
#         "cash_flow_after_funding_before_tax": cash_flow_after_funding_before_tax,
#         "total_tax_paid": total_tax_paid,
#         "cash_flow_available_for_debt_service": cash_flow_available_for_debt_service,
#         "total_debt_service": debt_service_per_year,
#         "cf_aoe": cash_flow_available_to_equity,
#         "interest_expense_total": interest_per_year,
#     }

#     return round_floats(result)


# def equity_return(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years, equity_return):
#     # First, calculate the cash flow information and the capex information
#     cash_flow_info = cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#     capex_info = calculate_capex(analysis_period, capex, debt_percent)
    
#     # Cash flow to equity for each year
#     cash_flows_to_equity = [-capex_info['equity']]  # Initial investment is negative
#     cash_flows_to_equity += cash_flow_info['cf_aoe'][1:] 
    

#     cumulative_cash_flow_equity = []
#     cumulative_cash = 0
#     for cf in cash_flows_to_equity:
#         cumulative_cash += cf
#         cumulative_cash_flow_equity.append(cumulative_cash)
    
#     # Calculate NPV to equity for each year
#     npvs_to_equity = []
#     for year in range(analysis_period):
#         npv = npf.npv(equity_return, cash_flows_to_equity[:year])
#         npvs_to_equity.append(npv)
    
#     # Calculate IRR to equity for each year, handling potential errors with calculation
#     irrs_to_equity = []
#     for year in range(1, analysis_period + 1):
#         try:
#             irr = npf.irr(cash_flows_to_equity[:year])
#             irrs_to_equity.append(irr)
#         except:
#             irrs_to_equity.append("Calculation Error")
    
#     result = {
#         "cash_flows_to_equity": cash_flows_to_equity,
#         "cce":cumulative_cash_flow_equity,
#         "npve": npvs_to_equity,
#         "irre": irrs_to_equity
#     }

#     return round_floats(result)



# def project_return(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate, project_return):
#     operating_info = operating_activities(analysis_period, production, ppa_price, opex)
#     tax_info_ug = tax_paid_ug(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate)
    
#     # Cash flow available to project before tax per year
   
#     cash_flow_available = [-capex]
#     cash_flow_available += operating_info['ebitda_per_year'][1:] 
#     # Tax paid (ungeared) per year
#     tax_paid = [0] 
#     tax_paid = tax_paid + tax_info_ug['tax_paid_ug_per_year'][1:]
    
#     # Cash flow to project per year
#     cash_flow_to_project = [cash_flow_available[i] + tax_paid[i] for i in range(analysis_period)]
    
#     # Cumulative cash flow to project per year
#     cumulative_cash_flow_to_project = []
#     cumulative_cash = 0
#     for cf in cash_flow_to_project:
#         cumulative_cash += cf
#         cumulative_cash_flow_to_project.append(cumulative_cash)
    
#     # NPV per year
#     npvs_to_project = []
#     for year in range(1, analysis_period + 1):
#         npv = npf.npv(project_return, cash_flow_to_project[:year])
#         npvs_to_project.append(npv)
    
#     # IRR per year, handling potential errors with calculation
#     irrs_to_project = []
#     for year in range(1, analysis_period + 1):
#         try:
#             irr = npf.irr(cash_flow_to_project[:year])
#             irrs_to_project.append(irr)
#         except:
#             irrs_to_project.append("Calculation Error")

#     result = {
#         "Cash Flow Available to Project": cash_flow_available,
#         "Tax Paid (Ungeared)": tax_paid,
#         "Cash Flow to Project": cash_flow_to_project,
#         "ccp": cumulative_cash_flow_to_project,  # Now a list
#         "npvp": npvs_to_project,
#         "irrp": irrs_to_project
#     }

#     return round_floats(result)


import numpy as np
import numpy_financial as npf

def round_floats(obj, precision=2):
    if isinstance(obj, float):
        return round(obj, precision)
    elif isinstance(obj, dict):
        return {k: round_floats(v, precision) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(item, precision) for item in obj]
    else:
        return obj

def calculate_total_production(analysis_period, production):
    yearly_production = [0]  # Production is 0 for the first year
    for year in range(1, analysis_period):
        yearly_production.append(production)
    total_production = sum(yearly_production)
    result = {"yearly_production":yearly_production, "total_production":total_production}
    return round_floats(result)

def calculate_capex(analysis_period, capex, debt_percent):
    senior_debt = capex * (debt_percent/100)
    equity = capex - senior_debt
    funding = equity + senior_debt
    yearly_capex = [capex] + [0] * (analysis_period - 1)
    yearly_funding = [capex] + [0] * (analysis_period - 1)
    total_capex = sum(yearly_capex)
    result = {"yearly_capex":yearly_capex, "total_capex":total_capex, "funding":funding, "yearly_funding":yearly_funding, "senior_debt": senior_debt, "equity":equity}

    return round_floats(result)


def operating_activities(analysis_period, production, ppa_price, opex):
    revenues_per_year = [0]  # Initialize with 0 for the initial year
    opex_per_year = [0]      # Initialize with 0 for the initial year
    ebitda_per_year = [0]    # Initialize with 0 for the initial year
    total_revenue = 0
    total_opex = 0
    total_ebitda = 0

    for year in range(1, analysis_period + 1):
        yearly_revenue = production * ppa_price
        revenues_per_year.append(yearly_revenue)
        total_revenue += yearly_revenue

        yearly_opex = production * opex
        opex_per_year.append(-yearly_opex)
        total_opex += yearly_opex

        yearly_ebitda = yearly_revenue - yearly_opex  # Since opex is negative, adding it
        ebitda_per_year.append(yearly_ebitda)
        total_ebitda += yearly_ebitda

    result = {"revenues_per_year": revenues_per_year, "total_revenue": total_revenue,"opex_per_year": opex_per_year,"total_opex": total_opex,"ebitda_per_year": ebitda_per_year,"total_ebitda": total_ebitda}
    return round_floats(result)

def tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years):
    capex_info = calculate_capex(analysis_period, capex, debt_percent)
    senior_debt = capex_info["senior_debt"]/repayment_years
    operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    
    
    interest_expense_per_year = [0]
    geared_tax_income_per_year = [0]
    tax_paid_per_year = [0]
    depreciation_per_year = [0] 

    for year in range(1, analysis_period + 1):

        if year <= repayment_years:
            # Calculate yearly interest expense till repayment years
            yearly_interest_expense = senior_debt * interest_rate * (repayment_years + 1 - year) / 100
            yearly_depreciation = capex / depreciation_y

            yearly_geared_tax_income = operating_info["ebitda_per_year"][year] - yearly_interest_expense - yearly_depreciation
        else:
            # After repayment years, interest expense becomes 0
            yearly_interest_expense = 0
            yearly_depreciation = 0
            yearly_geared_tax_income = 0

        interest_expense_per_year.append(-yearly_interest_expense)

        
        depreciation_per_year.append(-yearly_depreciation)
        
        geared_tax_income_per_year.append(yearly_geared_tax_income)
        
        
        yearly_tax_paid = yearly_geared_tax_income * (tax_rate/100)
        tax_paid_per_year.append(-yearly_tax_paid)
    
    result = {
        "interest_expense_per_year": interest_expense_per_year,
        "depreciation_per_year": depreciation_per_year,
        "geared_tax_income_per_year": geared_tax_income_per_year,
        "tax_paid_per_year": tax_paid_per_year
    }

    return round_floats(result)

def tax_paid_ug(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate):
    operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    
    depreciation_per_year = [0] 
    geared_taxable_income_per_year = [0]
    tax_paid_ug_per_year = [0]


    for year in range(1, analysis_period + 1):

        yearly_depreciation = capex / depreciation_y
        depreciation_per_year.append(-yearly_depreciation)

        geared_taxable_income = operating_info["ebitda_per_year"][year] - yearly_depreciation
        geared_taxable_income_per_year.append(geared_taxable_income)
        
        # net_taxable_income = geared_taxable_income  # Assuming no adjustments for ungeared
        # net_taxable_income_per_year.append(net_taxable_income)
        
        tax_paid_ug = geared_taxable_income * (tax_rate/100)
        tax_paid_ug_per_year.append(-tax_paid_ug)
    
    result =  {
        "depreciation_per_year": depreciation_per_year,
        "geared_taxable_income_per_year": geared_taxable_income_per_year,
        # "net_taxable_income_per_year": net_taxable_income_per_year,
        "tax_paid_ug_per_year": tax_paid_ug_per_year
    }

    return round_floats(result)

def calculate_debt(analysis_period, repayment_years, capex, debt_percent):
    capex_info = calculate_capex(analysis_period, capex, debt_percent)
    senior_debt = capex_info["senior_debt"]
    opening_balance = [0] * (analysis_period + 1)
    principal_payment = [0] * (analysis_period + 1)
    closing_balance = [0] * (analysis_period + 1)
    opening_balance[0] = senior_debt

    # Calculate principal payment if repayment_years is not 0 to avoid division by zero
    if repayment_years > 0:
        repayment_amount = senior_debt
        yearly_principal_payment = repayment_amount / repayment_years
    else:
        yearly_principal_payment = 0

    # Loop through each year to calculate the debt structure
    for year in range(1, analysis_period + 1):
        if year > 0:
            # Opening balance of next year is the closing balance of the previous year
            opening_balance[year] = closing_balance[year - 1]
        
        # Principal payment calculation, skip for year 0
        if year <= repayment_years:
            principal_payment[year] = yearly_principal_payment
        else:
            principal_payment[year] = 0
        
        # Closing balance calculation
        closing_balance[year] = opening_balance[year] - principal_payment[year]

    result = {
        "opening_balance": opening_balance,
        "principal_payment": principal_payment,
        "closing_balance": closing_balance
    }

    return round_floats(result)



def cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years):
    # Calculate Total CAPEX and Funding
    capex_info = calculate_capex(analysis_period, capex, debt_percent)
    tcapex = capex_info["yearly_capex"]
    tfunding = capex_info["yearly_funding"]
    operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    total_ebitda = operating_info["ebitda_per_year"]
    debt_service_per_year = [0]
    
    cash_flow_after_funding_before_tax = [0] + [ebitda - capex - funding for ebitda, capex, funding in zip(total_ebitda[1:], tcapex[1:], tfunding[1:])]


    tax_info = tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
    total_tax_paid = tax_info["tax_paid_per_year"]

    cash_flow_available_for_debt_service = [cf + tax for cf, tax in zip(cash_flow_after_funding_before_tax, total_tax_paid)]
   
    
    senior_debt = capex_info["senior_debt"]  
    principal_per_year = senior_debt / repayment_years
    
    interest_per_year = [0]  # Interest for the initial year is 0
    for year in range(1, repayment_years + 1):
        interest = principal_per_year * interest_rate * (repayment_years + 1 - year) / 100
        interest_per_year.append(interest)
        ds = interest + (principal_per_year if year <= repayment_years else 0)
        debt_service_per_year.append(ds)
    interest_per_year.extend([0] * (analysis_period - len(interest_per_year) + 1))  # Fill the rest with 0 if analysis_period > repayment_years
            
    # Cash Flow Available to Equity
    cash_flow_available_to_equity = [0] * (analysis_period + 1)  # Initialize with zeros
    for year in range(1, analysis_period + 1):
        if year <= repayment_years:
            cash_flow_available_to_equity[year] = cash_flow_available_for_debt_service[year] - debt_service_per_year[year]
        else:
            # Set cf_aoe to 0 beyond repayment years as per requirement
            cash_flow_available_to_equity[year] = 0
    # cash_flow_available_to_equity = [cf - ds for cf, ds in zip(cash_flow_available_for_debt_service, debt_service_per_year)]
    
    result = {
        "cash_flow_after_funding_before_tax": cash_flow_after_funding_before_tax,
        "total_tax_paid": total_tax_paid,
        "cash_flow_available_for_debt_service": cash_flow_available_for_debt_service,
        "total_debt_service": debt_service_per_year,
        "cf_aoe": cash_flow_available_to_equity,
        "interest_expense_total": interest_per_year,
    }

    return round_floats(result)




def equity_return(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years, equity_return):
    # First, calculate the cash flow information and the capex information
    cash_flow_info = cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
    capex_info = calculate_capex(analysis_period, capex, debt_percent)
    
    # Cash flow to equity for each year
    cash_flows_to_equity = [-capex_info['equity']]  # Initial investment is negative
    cash_flows_to_equity += cash_flow_info['cf_aoe'][1:] 
    
    cumulative_cash_flow_equity = []
    cumulative_cash = 0
    for cf in cash_flows_to_equity:
        cumulative_cash += cf
        cumulative_cash_flow_equity.append(cumulative_cash)
    
    # Calculate NPV to equity for each year
    npvs_to_equity = []
    for year in range(analysis_period + 1):
        npv = npf.npv(equity_return, cash_flows_to_equity[:year+1])
        npvs_to_equity.append(npv)
    
    # npvs_to_equity = []
    # for year in range(analysis_period + 1):
    #     npvs_to_equity.append(cash_flows_to_equity[year]/ (1 + equity_return) ** year)
    
    print(sum(npvs_to_equity))
    # Calculate IRR to equity for each year, handling potential errors with calculation
    irrs_to_equity = [0]
    for year in range(1, analysis_period + 1):
        try:
            irr = npf.irr(cash_flows_to_equity[:year+1])
            irrs_to_equity.append(irr)
        except:
            irrs_to_equity.append("Calculation Error")
    
    result = {
        "cash_flows_to_equity": cash_flows_to_equity,
        "cce": cumulative_cash_flow_equity,  # Keeping the original key name as 'cce'
        "npve": npvs_to_equity,  # Keeping the original key name as 'npve'
        "irre": irrs_to_equity  # Keeping the original key name as 'irre'
    }

    return round_floats(result)

def project_return(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate, project_return_rate):
    operating_info = operating_activities(analysis_period, production, ppa_price, opex)
    tax_info_ug = tax_paid_ug(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate)
    
    # Cash flow available to project before tax per year
    cash_flow_available = [-capex] + operating_info['ebitda_per_year'][1:] 
    
    # Tax paid (ungeared) per year
    tax_paid = [0] + tax_info_ug['tax_paid_ug_per_year'][1:]
    
    # Cash flow to project per year
    cash_flow_to_project = [cash_flow_available[i] + tax_paid[i] for i in range(analysis_period + 1)]
    
    # Cumulative cash flow to project per year
    cumulative_cash_flow_to_project = []
    cumulative_cash = 0
    for cf in cash_flow_to_project:
        cumulative_cash += cf
        cumulative_cash_flow_to_project.append(cumulative_cash)
    
    # NPV per year
    npvs_to_project = []
    for year in range(analysis_period + 1):
        npv = npf.npv(project_return_rate, cash_flow_to_project[:year+1])
        npvs_to_project.append(npv)
    
    # IRR per year, handling potential errors with calculation
    irrs_to_project = [0]
    for year in range(1, analysis_period + 1):
        try:
            irr = npf.irr(cash_flow_to_project[:year+1])
            irrs_to_project.append(irr)
        except:
            irrs_to_project.append("Calculation Error")

    result = {
        "Cash Flow Available to Project": cash_flow_available,
        "Tax Paid (Ungeared)": tax_paid,
        "Cash Flow to Project": cash_flow_to_project,
        "ccp": cumulative_cash_flow_to_project,  # Keeping the original key name as 'ccp'
        "npvp": npvs_to_project,  # Keeping the original key name as 'npvp'
        "irrp": irrs_to_project  # Keeping the original key name as 'irrp'
    }

    return round_floats(result)
