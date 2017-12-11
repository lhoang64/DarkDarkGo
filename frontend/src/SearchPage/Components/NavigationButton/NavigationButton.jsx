import React from 'react'

import NextButton from 'react-icons/lib/md/arrow-forward'
import PrevButton from 'react-icons/lib/md/arrow-back'

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
        <PrevButton className="previousButton" onClick={()=>props.changeOffsetBy(-1)} />
        <NextButton className="nextButton" onClick={()=>props.changeOffsetBy(1)} />
    </div>
    )
    
}