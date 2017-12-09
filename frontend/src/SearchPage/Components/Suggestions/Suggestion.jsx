import React from 'react'

export default (props) => {
    if (props.suggestions && props.suggestions.length > 0){
        return (
        <ul className="suggestions whitetext">
            {props.suggestions}
        </ul>
        )
    }
    return null
}