from flask import Flask, request, jsonify
from flask_cors import CORS
import financial_calculations as fc
import base64
from io import BytesIO
import math

# Import matplotlib and set the Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

def safe_jsonify(data):
    if isinstance(data, dict):
        return {k: safe_jsonify(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [safe_jsonify(v) for v in data]
    elif isinstance(data, float) and math.isnan(data):
        return None
    else:
        return data

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    try:
        analysis_period = int(data.get('analysis_period', 0))
        production = int(data.get('production', 0))
        capex = int(data.get('capex', 0))
        opex = int(data.get('opex', 0))
        ppa_price = int(data.get('ppa_price', 0))
        debt_percent = int(data.get('debt_percent', 0))
        repayment_years = int(data.get('repayment_years', 0))
        interest_rate = int(data.get('interest_rate', 0))
        tax_rate = int(data.get('tax_rate', 0))
        depreciation_y = int(data.get('depreciation_y', 0))
        project_return = int(data.get('project_return', 0))
        equity_return = int(data.get('equity_return', 0))

        years = analysis_period

        operating_info = fc.operating_activities(analysis_period, production, ppa_price, opex)
        total_revenue =  operating_info['revenues_per_year']
        total_opex =  operating_info['opex_per_year']

        tax = fc.tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
        tax_paid_g =  tax['tax_paid_per_year']

        principal_p = fc.calculate_debt(analysis_period, repayment_years, capex, debt_percent)
        principal =  principal_p['principal_payment']

        intr = fc.cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
        interest =  intr['interest_expense_total']
        cf_aoe =  intr['cf_aoe']

        cc_e = fc.equity_return(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years, equity_return)
        cce =  cc_e['cce']
        npve =  cc_e['npve']
        irre =  cc_e['irre']

        cc_p = fc.project_return(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate, project_return)
        ccp =  cc_p['ccp']
        npvp =  cc_p['npvp']
        irrp =  cc_p['irrp']
       
        

        response_data = {
            "years": years,
            "totalRevenue": total_revenue,
            "totalOpex": total_opex,
            "taxPaidG": tax_paid_g,
            "principal": principal,
            "interest": interest,
            "cf_aoe": cf_aoe,
            "cce": cce,
            "ccp": ccp,
            "npve": npve,
            "npvp": npvp,
            "irre": irre,
            "irrp": irrp  
        }

        safe_response_data = safe_jsonify(response_data)

        return jsonify(safe_response_data)
        

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Calculation failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import financial_calculations as fc
# import base64
# from io import BytesIO
# import math

# # Import matplotlib and set the Agg backend
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

# app = Flask(__name__)
# CORS(app)

# def safe_jsonify(data):
#     if isinstance(data, dict):
#         return {k: safe_jsonify(v) for k, v in data.items()}
#     elif isinstance(data, list):
#         return [safe_jsonify(v) for v in data]
#     elif isinstance(data, float) and math.isnan(data):
#         return None
#     else:
#         return data

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.get_json()

#     try:
#         analysis_period = int(data.get('analysis_period', 0))
#         production = int(data.get('production', 0))
#         capex = int(data.get('capex', 0))
#         opex = int(data.get('opex', 0))
#         ppa_price = int(data.get('ppa_price', 0))
#         debt_percent = int(data.get('debt_percent', 0))
#         repayment_years = int(data.get('repayment_years', 0))
#         interest_rate = int(data.get('interest_rate', 0))
#         tax_rate = int(data.get('tax_rate', 0))
#         depreciation_y = int(data.get('depreciation_y', 0))
#         project_return = int(data.get('project_return', 0))
#         equity_return = int(data.get('equity_return', 0))

#         years = analysis_period

#         operating_info = fc.operating_activities(analysis_period, production, ppa_price, opex)
#         total_revenue =  operating_info['revenues_per_year']
#         total_opex =  operating_info['opex_per_year']

#         tax = fc.tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#         tax_paid_g =  tax['tax_paid_per_year']

#         principal_p = fc.calculate_debt(analysis_period, repayment_years, capex, debt_percent)
#         principal =  principal_p['principal_payment']

#         intr = fc.cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#         interest =  intr['interest_expense_total']
#         cf_aoe =  intr['cf_aoe']

#         cc_e = fc.equity_return(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years, equity_return)
#         cce =  cc_e['cce']
#         npve =  cc_e['npve']
#         irre =  cc_e['irre']

#         cc_p = fc.project_return(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate, project_return)
#         ccp =  cc_p['ccp']
#         npvp =  cc_p['npvp']
#         irrp =  cc_p['irrp']
       
        

#         response_data = {
#             "years": years,
#             "totalRevenue": total_revenue,
#             "totalOpex": total_opex,
#             "taxPaidG": tax_paid_g,
#             "principal": principal,
#             "interest": interest,
#             "cf_aoe": cf_aoe,
#             "cce": cce,
#             "ccp": ccp,
#             "npve": npve,
#             "npvp": npvp,
#             "irre": irre,
#             "irrp": irrp  
#         }

#         safe_response_data = safe_jsonify(response_data)

#         return jsonify(safe_response_data)
        

#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': 'Calculation failed'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)
