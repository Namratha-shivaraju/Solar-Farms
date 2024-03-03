// import React, { useState } from 'react'
// import './FInput.css'

// function FInput() {
  
//   return (
//     <div className='main-container'>
//     <div className="container">        
//       <h1 className="heading">
//         Financial Input
//         </h1>
//       <div className="content">
//         <div className="space-y-4">

//           <div>
//             <label className="variables">Analysis Period</label>
//             <select className="dropdown">
//               <option>Year</option>
//               <option>Month</option>
//             </select>
//           </div>
          

//           <div>
//             <label className="variables">Production</label>
//             <input type="number" placeholder="MWh/yr" className="ipvalue"/>
//           </div>

          
          
//           <div>
//             <label className="variables">Turn key costs</label>
//             <input type="number" placeholder="USD" className="ipvalue"/>
//           </div>


//           <div>
//             <label className="variables">Turn key costs</label>
//             <input type="number" placeholder="USD" className="ipvalue"/>
//           </div>
//         </div>

//         <div className="space-y-4">
            

//           <div>
//             <label className="variables">All the variable costs of the solar microgrid</label>
//             <input type="number" placeholder="USD/MWh" className="ipvalue"/>
//           </div>


//           <div>
//             <label className="variables">Debt Percent</label>
//             <input type="number" placeholder="%" className="ipvalue"/>
//           </div>
          

//           <div>
//             <label className="variables">Total number of years to repay debt</label>
//             <input type="number" placeholder="Years" className="ipvalue"/>
//           </div>
          

//           <div>
//             <label className="variables">Total interest rate for the debt</label>
//             <input type="number" placeholder="%" className="ipvalue" />
//           </div>
//         </div>

//         <div className="space-y-4">


//           <div>
//             <label className="variables">Corporate Tax</label>
//             <input type="number" placeholder="%" className="ipvalue"/>
//           </div>


//           <div>
//             <label className="variables">Straight Line Depreciation Schedule</label>
//             <input type="number" placeholder="Years" className="ipvalue"/>
//           </div>
          

//           <div>
//             <label className="variables">The expected rate of return for the project</label>
//             <input type="number" placeholder="%" className="ipvalue"/>
//           </div>
          

//           <div>
//             <label className="variables">The expected rate of return for the equity investors</label>
//             <input type="number" placeholder="%" className="ipvalue"/>
//           </div>
//         </div>
//       </div>
//       <button className="action-button">
//         Calculate
//       </button>
//     </div>
//     </div>
//   )
// }

// export default FInput



//Logical code   

import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Line, LineChart, ReferenceLine, AreaChart, Area, Rectangle } from 'recharts';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import './FInput.css';

function FInput() {
  const initialFormData = {
    analysis_period: '',
    currency: '',
    production: '',
    capex: '',
    opex: '',
    ppa_price: '',
    debt_percent: '',
    repayment_years: '',
    interest_rate: '',
    tax_rate: '',
    depreciation_y: '',
    project_return: '',
    equity_return: ''
  };

  const [formData, setFormData] = useState(initialFormData);

  //to show result in non image -- const [results, setResults] = useState({ npv: null, irr: null });
  // years: null, totalRevenue: null, totalOpex: null, taxPaidG: null, principal: null, interest: null, cf_aoe: null, cce: null, ccp: null, npve: null, npvp: null, irre: null, irrp: null
  const [results, setResults] = useState([]); // Store multiple results
  const [isCalculated, setIsCalculated] = useState(false); 
  //image change
  //const [plotUrl, setPlotUrl] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  //uncomment if image does not work

  // const handleSubmit = async (e) => {
  //   e.preventDefault(); // Prevent the default form submit action

  //   try {
  //     const response = await fetch('http://127.0.0.1:5000/calculate', { // Adjust the URL/port as needed
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify(formData)
  //     });
  //   // comment this if image does not work
  //     if (!response.ok) throw new Error('Network response was not ok.');

  //     const data = await response.json();
  //     setResults({ npv: data.npv, irr: data.irr });
  //     setPlotUrl('http://127.0.0.1:5000/plot.png');
  //     setIsCalculated(true);
  //   } catch (error) {
  //     console.error('There was a problem with your fetch operation:', error);
  //     alert('Failed to calculate. Please check the console for more details.');
  //   }
  // };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Network response was not ok.');

      const data = await response.json();
      // const newResult = {years: data.years, totalRevenue: data.total_revenue, totalOpex: data.total_opex, taxPaidG: data.tax_paid_g, principal: data.principal, 
      // interest: data.interest, cf_aoe: data.cf_aoe, cce: data.cce, ccp: data.ccp, npve: data.npve, npvp: data.npvp, irre: data.irre, irrp: data.irrp};
      
      // const newResult = Object.fromEntries(
      //   Object.entries(data).map(([key, value]) => [key, value === null ? 0 : isNaN(value) ? null : value])
      // );
      const chartData = [];
      for (let index = 0; index < data.years; index++) {
        chartData.push({
          years: index + 1,
          totalRevenue: data.totalRevenue[index] || 0,
          totalOpex: data.totalOpex[index] || 0,
          taxPaidG: data.taxPaidG[index] || 0,
          principal: data.principal[index] || 0,
          interest: data.interest[index] || 0,
          cf_aoe: data.cf_aoe[index] || 0,
          cce: data.cce[index] || 0,
          ccp: data.ccp[index] || 0,
          npve: data.npve[index] || 0,
          npvp: data.npvp[index] || 0,
          irre: data.irre[index] || 0,
          irrp: data.irrp[index] || 0,
        })
      }
      // const years = Array.from({ length: newResult.years }, (_, i) => i + 1);
      // const chartData = years.map((year, index) => ({
      //   year: year,
      //   totalRevenue: newResult.totalRevenue[index],
      //   // totalOpex: newResult.totalOpex[index],
      //   // taxPaidG: newResult.taxPaidG[index],
      //   principal: newResult.principal[index],
      //   interest: newResult.interest[index],
      //   cf_aoe: newResult.cf_aoe[index],
      //   cce: newResult.cce[index],
      //   ccp: newResult.ccp[index],
      //   npve: newResult.npve[index],
      //   npvp: newResult.npvp[index],
      //   irre: newResult.irre[index],
      //   irrp: newResult.irrp[index],
      // }));

      setResults(chartData);
      setIsCalculated(true);
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
      alert('Failed to calculate. Please check the console for more details.');
    }
  };





  const exportPDF = () => {
    // Adjust the selector if needed to target the specific content you want to capture
    html2canvas(document.querySelector(".report-container")).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const imgWidth = 210; // A4 width in mm
      const pageHeight = 295;  // A4 height in mm
      const imgHeight = canvas.height * imgWidth / canvas.width;
      let heightLeft = imgHeight;

      const doc = new jsPDF('p', 'mm');
      let position = 0;

      doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        doc.addPage();
        doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }
      doc.save('report.pdf');
    });
  };

  // const exportPDF = () => {
  //   html2canvas(document.querySelector(".report-container")).then(canvas => {
  //     const imgData = canvas.toDataURL('image/png');
  //     const canvasWidth = canvas.width;
  //     const canvasHeight = canvas.height;
  //     const canvasAspectRatio = canvasWidth / canvasHeight;
  
  //     // Set PDF size based on the aspect ratio of the canvas
  //     const pdfWidth = 210; // A4 width in mm
  //     const pdfHeight = pdfWidth / canvasAspectRatio;
  
  //     // Create a new jsPDF instance with calculated width and height
  //     const pdf = new jsPDF({
  //       orientation: canvasWidth > canvasHeight ? "landscape" : "portrait",
  //       unit: 'mm',
  //       format: [pdfWidth, pdfHeight]
  //     });
  
  //     // Add the captured image to the PDF
  //     pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
  //     pdf.save("session-report.pdf");
  //   });
  // };

  const handleReset = () => {
    setFormData(initialFormData); // Reset form data to initial state
    //uncomment this if image does not work -- setResults({ npv: null, irr: null }); // Reset results
    setResults([]);
    setIsCalculated(false); // Reset calculated state
  };

  return (
    <div className='main-container'>
      <div className="container">
        <h1 className="heading">Financial Input</h1>
        <form className="content" onSubmit={handleSubmit}>
          
          <div className='form-content'>
              <label htmlFor="analysis_period" className="variables">Analysis Period</label>
              <input type="number" placeholder="Years" className="ipvalue" name="analysis_period" id="analysis_period" onChange={handleChange} value={formData.analysis_period}/>
            </div>

            <div className='form-content'>
              <label htmlFor="currency" className="variables">Currency</label>
              <select name="currency" className="dropdown" id="currency" onChange={handleChange} value={formData.currency}>
                <option value="">Choice</option>
                <option value="USD">USD</option>
              </select>
            </div>

            <div className='form-content'> 
              <label htmlFor="production" className="variables">Production</label>
              <input type="number" placeholder="MWh/yr" className="ipvalue" name="production" id='production' onChange={handleChange} value={formData.production}/>
            </div>

            <div className='form-content'>
              <label htmlFor="capex" className="variables">Turn key costs</label>
              <input type="number" placeholder="USD" className="ipvalue" name="capex" id="capex" onChange={handleChange} value={formData.capex}/>
            </div>

            <div className='form-content'>
              <label htmlFor="opex" className="variables">Variable costs by generation (OPEX)</label>
              <input type="number" placeholder="USD/MWh" className="ipvalue" name="opex" id="opex" onChange={handleChange} value={formData.opex}/>
            </div>

            <div className='form-content'>
              <label htmlFor="ppa_price" className="variables">PPA Prices</label>
              <input type="number" placeholder="USD/MWh" className="ipvalue" name="ppa_price" id="ppa_price" onChange={handleChange} value={formData.ppa_price}/>
            </div>

            <div className='form-content'>
              <label htmlFor="debt_percent" className="variables">Debt Percent</label>
              <input type="number" placeholder="%" className="ipvalue" name="debt_percent" id="debt_percent" onChange={handleChange} value={formData.debt_percent}/>
            </div>

            <div className='form-content'>
              <label htmlFor="repayment_years" className="variables">Total number of years to repay debt</label>
              <input type="number" placeholder="Years" className="ipvalue" name="repayment_years" id="repayment_years" onChange={handleChange} value={formData.repayment_years}/>
            </div>

            <div className='form-content'>
              <label htmlFor="interest_rate" className="variables">Total interest rate for the debt</label>
              <input type="number" placeholder="%" className="ipvalue" name="interest_rate" id="interest_rate" onChange={handleChange} value={formData.interest_rate}/>
            </div>

            {/* <div className='form-content'>
              <label htmlFor="dcc" className="variables">Debt closing costs</label>
              <input type="number" placeholder="USD" className="ipvalue" name="dcc" id="dcc" onChange={handleChange} value={formData.dcc}/>
            </div> */}

            {/* <div className='form-content'>
              <label htmlFor="upfront" className="variables">Up-front fee</label>
              <input type="number" placeholder="%" className="ipvalue" name="upfront" id="upfront" onChange={handleChange} value={formData.upfront}/>
            </div> */}

            <div className='form-content'>
              <label htmlFor="tax_rate" className="variables">Corporate Tax</label>
              <input type="number" placeholder="%" className="ipvalue" name="tax_rate" id="tax_rate" onChange={handleChange} value={formData.tax_rate}/>
            </div>

            <div className='form-content'>
              <label htmlFor="depreciation_y" className="variables">Straight Line Depreciation Schedule</label>
              <input type="number" placeholder="Years" className="ipvalue" name="depreciation_y" id="depreciation_y" onChange={handleChange} value={formData.depreciation_y}/>
            </div>

            <div className='form-content'>
              <label htmlFor="project_return" className="variables">Expected rate of return for the project</label>
              <input type="number" placeholder="%" className="ipvalue" name="project_return" id="project_return" onChange={handleChange} value={formData.project_return}/>
            </div>

            <div className='form-content'>
              <label htmlFor="equity_return" className="variables">Expected rate of return for the equity investors</label>
              <input type="number" placeholder="%" className="ipvalue" name="equity_return" id="equity_return" onChange={handleChange} value={formData.equity_return}/>
            </div>

            <div className="form-actions">
            <button type="submit" className="action-button">
              Calculate
            </button>

            <button type="button" className="reset-button" onClick={handleReset}>
              Reset
            </button>
          </div>
        
        </form>
      </div>
       <div className="report-container">
        <h1 className="heading">Financial Report</h1>
        {/* <h1 className='load'>{isCalculated ? 'Results' : 'Please enter all the fields'}</h1> */}
        {/* {isCalculated && (
          <div className="info">
            <div className="info-inside">
              <p>NPV: {results.npv !== null ? `$${results.npv}` : 'Not Calculated'}</p>
              <p>IRR: {results.irr !== null ? `${results.irr}%` : 'Not Calculated'}</p>
            </div>
          </div>
        )} */}
        {/* {isCalculated && plotUrl && (
          <div className="info">
            <div className="info-inside">
              <p className='pstyle'>NPV: {results.npv !== null ? `$${results.npv}` : 'Not Calculated'}</p>
              <p className='pstyle'>IRR: {results.irr !== null ? `${results.irr}%` : 'Not Calculated'}</p>
              <img src={plotUrl} alt="Plot" />
            </div>
          </div>
        )} */}
        {/* <button type="button" onClick={exportPDF}>Save Session as PDF</button> */}
        {/* {isCalculated ? results.map((result, index) => (
          <div className="info" key={index}>
            <div className="info-inside">
              <p className='pstyle'>NPV: {result.npv !== null ? `$${result.npv}` : 'Not Calculated'}</p>
              <p className='pstyle'>IRR: {result.irr !== null ? `${result.irr}%` : 'Not Calculated'}</p>
              {result.plotUrl && <img src={result.plotUrl} alt="Plot" />}
            </div>
            <button type="button">Save Session as PDF</button>
          </div>
        )) : <h1 className='load'>Please enter all the fields and calculate</h1>} */}
        {isCalculated ? (
        <div className="info">
        <div className="info-inside">
          {/* <p className='pstyle'>NPV: {result.npv !== null ? `$${result.npv}` : 'Not Calculated'}</p>
          <p className='pstyle'>IRR: {result.irr !== null ? `${result.irr}%` : 'Not Calculated'}</p> */}
          {/* {result.plotUrl && <img src={result.plotUrl} alt="Plot" />} */}
        <div className='project_cashflow'>
          <h4>Project Cashflow</h4>
          <div className='charts'> 
          <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={results} // This should be your transformed data array
            margin={{
              top: 20, right: 30, left: 20, bottom: 5,
            }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="years" name='years'/>
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="totalRevenue" stackId="a" fill="#AFA1C4" name="Total Revenue" />
          <Bar dataKey="totalOpex" stackId="a" fill="#D4B4CD" name="Total OPEX" />
          <Bar dataKey="taxPaidG" stackId="a" fill="#F7D4D2" name="Tax Paid (Geared)" />
          <Bar dataKey="principal" stackId="a" fill="#D2D6C3" name="Principal" />
          <Bar dataKey="interest" stackId="a" fill="#A4A8BF" name="Interest" />
          </BarChart>
        </ResponsiveContainer>
        </div>
        </div>
        <div className='cashflow_for_debt'>
          <h4>Cash Flow Available for Debt Service (USD)</h4>
          <div className='charts'>
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart
            data={results} // This should be your transformed data array
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="years" name='years'/>
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="principal" stackId="1" stroke="#D2D6C3" fill="#D2D6C3" name='Principal'/>
            <Area type="monotone" dataKey="interest" stackId="1" stroke="#A4A8BF" fill="#A4A8BF" name='Interest'/>
            <Area type="monotone" dataKey="cf_aoe" stackId="1" stroke="#AFA1C4" fill="#AFA1C4" name='Cash flow Available to Equity'/>
            </AreaChart>
          </ResponsiveContainer> 
          </div>
        </div>
        <div className='ccf'>
          <h4>Cumulative Cash Flow</h4>
          <div className='left-graph'>
            <h3>Equity (USD)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
            <AreaChart
            data={results} // This should be your transformed data array
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="years" name='years'/>
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="cce" stackId="1" stroke="#AFA1C4" fill="#AFA1C4" name='Cumulative Cash flow to Equity'/>
            </AreaChart>
            </ResponsiveContainer>
            </div>
          </div>
          <div className='right-graph'>
            <h3>Project (USD)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
            <AreaChart
            data={results} // This should be your transformed data array
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
            >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="years" name='years'/>
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="ccp" stackId="1" stroke="#AFA1C4" fill="#AFA1C4" name='Cumulative Cash flow to Project'/>
            </AreaChart>
            </ResponsiveContainer>
            </div>
          </div>
        </div>
        <div className='ccf'>
          <h4>Equity Returns</h4>
          <div className='left-graph'>
            <h3>IRR (%)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart
              width={500}
              height={300}
              data={results}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
              >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="years" name='years'/>
              <YAxis />
              <Tooltip />
              <Legend />
              <ReferenceLine y={0} stroke="#000" />
              <Line type="monotone" dataKey="irre" stroke="#AFA1C4" name='IRR to Equity(%)'/>
              </LineChart>
            </ResponsiveContainer>
            </div>
          </div>
          <div className='right-graph'>
            <h3>NPV (USD)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
            <BarChart
              width={500}
              height={300}
              data={results}
              margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="years" name='years'/>
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="npve" fill="#AFA1C4" activeBar={<Rectangle fill="pink" stroke="blue" name='NPV to Equity'/>} />
            </BarChart>
          </ResponsiveContainer>
          </div>
          </div>
        </div>
        <div className='ccf'>
          <h4>Project Returns</h4>
          <div className='left-graph'>
            <h3>IRR (%)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart
              width={500}
              height={300}
              data={results}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
              >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="years" name='years'/>
              <YAxis />
              <Tooltip />
              <Legend />
              <ReferenceLine y={0} stroke="#000" />
              <Line type="monotone" dataKey="irrp" stroke="#AFA1C4" name='IRR to Project(%)'/>
              </LineChart>
            </ResponsiveContainer>
            </div>
          </div>
          <div className='right-graph'>
            <h3>NPV (USD)</h3>
            <div className='charts'>
            <ResponsiveContainer width="100%" height={400}>
            <BarChart
              width={500}
              height={300}
              data={results}
              margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="years" name='years'/>
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="npvp" fill="#AFA1C4" activeBar={<Rectangle fill="pink" stroke="blue" name='NPV to Project'/>} />
            </BarChart>
          </ResponsiveContainer>
          </div>
          </div>
        </div>
        </div>
        </div>
        ) : <h1 className='load'>Please enter all the fields and calculate</h1>}
        {!isCalculated ? ' ' : <button type="button" onClick={exportPDF}>Save Session as PDF</button>}
      </div>
    </div>
    
  );
}

export default FInput;
