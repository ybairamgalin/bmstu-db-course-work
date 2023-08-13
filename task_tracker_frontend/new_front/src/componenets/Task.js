import React, {useEffect} from "react";
import {useParams} from "react-router-dom";

export default function Task() {
    const params = useParams()
    console.log(params)

    useEffect(() => {

    }, [])

    return (
        <div>{params.publicId}</div>
    )
}
