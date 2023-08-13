import React from "react";

export default function ColOption({id, options, text}) {
    return (
        <div className="col">
            <select id={id} className="form-select">
                {options.map(option => {
                    return <option key={option}>{option}</option>
                })}
            </select>
            <div id={id+'text'} className="form-text p-1">
                {text}
            </div>
        </div>
    );
}
