import React from 'react'
import './FOutput.css'

function FOutput() {
  return (
    // <div className='main-container'>
    // <div className="container">        
    //   <h1 className="heading">
    //   Financial Report</h1>
    //   <div className='info'>
    //     <div className='info-inside'>
    //         <div className='info-text'>
    //             <span className='load'>Getting things ready</span>
    //         </div>
    //     </div>
    //   </div>
    // </div>
    // </div>
    <div className='main-container'>
    <div className="report-container">
        <h1 className="heading">Financial Report</h1>
        <div className="info">
            <div className="info-inside">
                <div className="info-text "></div>
                <span className="load">Getting things ready...</span>
              </div>
        </div>
      </div>
    </div>
  )
}

export default FOutput
