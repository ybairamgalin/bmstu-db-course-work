import React, {useEffect, useState} from "react";
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom';

import SideBar from "./componenets/SideBar";
import TasksFinder from "./componenets/TasksFinder";
import Login from "./componenets/Login";
import Task from "./componenets/Task";

import {getTokenFromLocalStorage} from "./utils/token";

function TasksScreen() {
    return (
        <main><SideBar/><TasksFinder/></main>
    )
}

function App() {
    const [token, setToken] = useState('')
    useEffect(() => {
        setToken(getTokenFromLocalStorage())
    }, [])

    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path='/'
                    element={
                    token?<Navigate to='/tasks' replace={true}/>
                         :<Navigate to='/auth' replace={true}/>
                }
                />
                <Route
                    path='/auth'
                    element={<Login setToken={setToken}/>}
                />
                <Route
                    path='/tasks'
                    element={<TasksScreen/>}
                />
                <Route
                    path='/task/:publicId'
                    element={<Task/>}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
