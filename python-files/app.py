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

from flask import Flask, request, jsonify
from flask_cors import CORS
import financial_calculations
import base64
from io import BytesIO

# Import matplotlib and set the Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    try:
        analysisPeriod = int(data.get('analysisPeriod', 0))
        production = float(data.get('production', 0.0))
        capex = float(data.get('capex', 0.0))
        opex = float(data.get('opex', 0.0))
        ppa_price = float(data.get('ppa_price', 0.0))
        upfront = float(data.get('upfront', 0.0))

        npv = financial_calculations.calculate_npv(analysisPeriod, production, capex, opex, ppa_price, upfront)
        cash_flows = [-capex] + [production * ppa_price - opex for _ in range(analysisPeriod)]
        irr = financial_calculations.calculate_irr(cash_flows)

        # Generate and encode plot as base64
        plot_data = generate_plot_base64()

        print(f"Calculated NPV: {npv}")
        print(f"Calculated IRR: {irr}")
        return jsonify({'npv': npv, 'irr': irr, 'plot': plot_data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Calculation failed'}), 400

def generate_plot_base64():
    """Generate a plot and return it as a base64-encoded string."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])  # Example plot
    img = BytesIO()
    plt.savefig(img, format='png')  # Save plot to a BytesIO object
    plt.close(fig)  # Close the figure to free resources
    img.seek(0)  # Go to the beginning of the BytesIO object
    plot_data = base64.b64encode(img.read()).decode('utf-8')  # Encode as base64
    return plot_data

if __name__ == '__main__':
    app.run(debug=True)
