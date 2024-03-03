# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import financial_calculations

# app = Flask(__name__)
# CORS(app)

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.get_json()

#     try:
#         analysisPeriod = int(data.get('analysisPeriod', 0))
#         production = float(data.get('production', 0.0))
#         capex = float(data.get('capex', 0.0))
#         opex = float(data.get('opex', 0.0))
#         ppa_price = float(data.get('ppa_price', 0.0))
#         upfront = float(data.get('upfront', 0.0))

#         npv = financial_calculations.calculate_npv(analysisPeriod, production, capex, opex, ppa_price, upfront)
#         cash_flows = [-capex] + [production * ppa_price - opex for _ in range(analysisPeriod)]
#         irr = financial_calculations.calculate_irr(cash_flows)

#         print(f"Calculated NPV: {npv}")
#         print(f"Calculated IRR: {irr}")
#         return jsonify({'npv': npv, 'irr': irr})
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': 'Calculation failed'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


# const handleSubmit = async (e) => {
#     e.preventDefault();
#     try {
#       const response = await fetch('http://127.0.0.1:5000/calculate', {
#         method: 'POST',
#         headers: { 'Content-Type': 'application/json' },
#         body: JSON.stringify(formData)
#       });
#       if (!response.ok) throw new Error('Network response was not ok.');
#       const result = await response.json();
  
#       setResults({
#         npv: typeof result.npv === 'number' ? result.npv.toFixed(2) : 'Calculation error',
#         irr: typeof result.irr === 'number' ? result.irr.toFixed(2) : 'Calculation error'
#       });
#     } catch (error) {
#       console.error('Error:', error);
#       setResults({ npv: 'Calculation error', irr: 'Calculation error' });
#     }
#   };


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import financial_calculations

# import matplotlib  # 新增导入
# matplotlib.use('Agg')  # 在导入 pyplot 之前设置使用 Agg 后端
# import matplotlib.pyplot as plt

# import os

# app = Flask(__name__)
# CORS(app)

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.get_json()
#     print(data)  # 打印接收到的数据

#     # 从请求数据中提取所有必要的参数，并转换为浮点数
#     analysisPeriod = data['analysisPeriod']
#     production = float(data['production'])
#     capex = float(data['capex'])
#     opex = float(data['opex'])
#     ppa_price = float(data['ppa_price'])
#     upfront = float(data['upfront'])

#     # 使用提取的参数调用calculate_npv函数
#     npv = financial_calculations.calculate_npv(analysisPeriod, production, capex, opex, ppa_price, upfront)

#     # 为了调用calculate_irr，需要构建一个适当的现金流数组
#     cash_flows = [upfront, production]  # 这需要根据实际情况调整
#     irr = financial_calculations.calculate_irr(cash_flows)

#     # 打印计算结果
#     print(f"Calculated NPV: {npv}")
#     print(f"Calculated IRR: {irr}")

#     # 生成并保存图片
#     fig, ax = plt.subplots()
#     ax.plot([0, analysisPeriod], [npv, irr], marker='o')  # 以分析期限为x轴，NPV和IRR为y轴的简单折线图
#     image_path = 'financial_analysis_plot.png'  # 直接保存到与app.py相同的目录下
#     plt.savefig(image_path)
#     plt.close(fig)
    
#     # 返回计算结果及图片路径
#     return jsonify({'npv': npv, 'irr': irr, 'image_path': image_path})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import financial_calculations
 
# # 导入matplotlib并设置Agg后端
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
 
# app = Flask(__name__)
# CORS(app)
 
# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.get_json()
 
#     try:
#         analysisPeriod = int(data.get('analysisPeriod', 0))
#         production = float(data.get('production', 0.0))
#         capex = float(data.get('capex', 0.0))
#         opex = float(data.get('opex', 0.0))
#         ppa_price = float(data.get('ppa_price', 0.0))
#         upfront = float(data.get('upfront', 0.0))
 
#         npv = financial_calculations.calculate_npv(analysisPeriod, production, capex, opex, ppa_price, upfront)
#         cash_flows = [-capex] + [production * ppa_price - opex for _ in range(analysisPeriod)]
#         irr = financial_calculations.calculate_irr(cash_flows)
 
#         # 在这里调用绘图函数
#         generate_plot()
 
#         print(f"Calculated NPV: {npv}")
#         print(f"Calculated IRR: {irr}")
#         return jsonify({'npv': npv, 'irr': irr})
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': 'Calculation failed'}), 400
 
# def generate_plot():
#     """生成并保存一个示例图表"""
#     fig, ax = plt.subplots()
#     ax.plot([1, 2, 3], [1, 2, 3])  # 举例绘制一条线
#     plt.savefig('plot.png')  # 保存到文件
#     plt.close(fig)  # 关闭图形，释放资源

# @app.route('/plot.png')
# def serve_plot():
#     """Serve the plot image."""
#     return send_file('plot.png', mimetype='image/png')
 
# if __name__ == '__main__':
#     app.run(debug=True)

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
#         total_revenue = round(operating_info['revenues_per_year'], 2)
#         total_opex = round(operating_info['opex_per_year'], 2)

#         tax = fc.tax_paid_g(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#         tax_paid_g = round(tax['tax_paid_per_year'], 2)

#         principal_p = fc.calculate_debt(analysis_period, repayment_years, capex, debt_percent)
#         principal = round(principal_p['principal_payment'], 2)

#         intr = fc.cashflow(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years)
#         interest = round(intr['interest_expense_total'], 2)
#         cf_aoe = round(intr['cf_aoe'], 2)

#         cc_e = fc.equity_return(analysis_period, capex, debt_percent, production, ppa_price, opex, depreciation_y, interest_rate, tax_rate, repayment_years, equity_return)
#         cce = round(cc_e['cce'], 2)
#         npve = round(cc_e['npve'], 2)
#         irre = round(cc_e['irre'], 2)

#         cc_p = fc.project_return(analysis_period, capex, production, ppa_price, opex, depreciation_y, tax_rate, project_return)
#         ccp = round(cc_p['ccp'], 2)
#         npvp = round(cc_p['npvp'], 2)
#         irrp = round(cc_p['irrp'], 2)
       
        

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
