import React from 'react'

export default (props) => {
    if (props.suggestions && props.suggestions.length > 0){
        return (
        <ul className={"whitetext "+props.className}>
            {props.suggestions}
        </ul>
        )
    }
    return null
}