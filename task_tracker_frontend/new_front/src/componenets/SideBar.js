import React from "react";
import {getNameFromLocalStorage} from "../utils/token";


export default function SideBar() {
    return (
        <div className="d-flex flex-column flex-shrink-0 p-3 text-white bg-dark side-bar">
            <h2>Task tracker</h2>
            <hr />
            <ul className="nav nav-pills flex-column mb-auto">
                <li className="nav-item p-2 link-light">
                    <a href="/new-task" className='link-light'>Создать задачу</a>
                </li>
                <li className="nav-item p-2">
                    <a href="/tasks" className='link-light'>Все задачи</a>
                </li>
            </ul>
            <hr />
            <div className="dropdown"><p>
                {getNameFromLocalStorage()}
            </p></div>
        </div>
    );
}
