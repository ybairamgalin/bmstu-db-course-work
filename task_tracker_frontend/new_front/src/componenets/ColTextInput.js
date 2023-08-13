import React from "react";

export default function ColTextInput({placeholder, onChange}) {
    return (
        <div className="col">
            <div className="form-group">
                <input type="text"
                       className="form-control"
                       placeholder={placeholder}
                       onChange={onChange}
                />
            </div>
        </div>
    );
}
