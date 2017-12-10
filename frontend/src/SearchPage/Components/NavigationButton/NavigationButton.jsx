import React from 'react'

export default (props) => {
    if (props.offset === 0){
        // Return Next button
        return (
        <div className="offsetButtons">
            <button className="nextButton" onClick={()=>props.changeOffsetBy(1)}>
                Next
            </button>
        </div>
        )
    } 
    // Return both Next and Prev button
    return (
    <div className="offsetButtons">
        <button className="previousButton" onClick={()=>props.changeOffsetBy(-1)}>
            Previous
        </button>
        <button className="nextButton" onClick={()=>props.changeOffsetBy(1)}>
            Next
        </button>
        </div>
    )
    
}