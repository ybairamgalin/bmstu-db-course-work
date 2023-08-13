import React, {useState} from "react";
import { useNavigate } from "react-router-dom";

import {API_PATH} from "../constants";
import {setTokenToLocalStorage} from "../utils/token";

export default function Login({setToken}) {
    const [login, setLogin] = useState()
    const [pass, setPass] = useState()
    const [error, setError] = useState()

    let navigate = useNavigate()

    const handleLogin = (event) => {
        setLogin(event.target.value)
    }
    const handlePass = (event) => {
        setPass(event.target.value)
    }

    async function handleSubmit() {
        if (!login || !pass) {
            setError('Логин и пароль должны быть заполнены')
            // TODO
            return
        }
        let response = await fetch(
            API_PATH + '/user/auth',
            {
                method: 'POST',
                body: JSON.stringify(
                    {
                        'username': login,
                        'hashed_password': pass
                    }
                ),
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        )
        if (response.status === 401) {
            setError('Неверный логин или пароль')
            return
        }
        if (response.status === 200) {
            let json = await response.json()
            setTokenToLocalStorage(json['X-User-Token'], json['name'])
            setToken(json['X-User-Token'])
            navigate('/tasks')
            return
        }

        setError('Необработанная ошибка')
    }

    return (
        <div className="d-flex justify-content-center py-5 my-5">
            <form>
                <h1>Мой трекер задач</h1>
                <p className="text-danger">{error}</p>
                <div className="mb-3">
                    <label htmlFor="login_input" className="form-label">Логин</label>
                    <input
                        type="text"
                        className="form-control"
                        id="login_input"
                        aria-describedby="emailHelp"
                        onChange={handleLogin}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password_input" className="form-label">Пароль</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password_input"
                        onChange={handlePass}
                    />
                </div>
                <div className="mb-3">
                    <label id="emailHelp" className="form-text text-muted">
                        Нет аккаунта? <a href="/signup">Создать аккаунт</a>
                    </label>
                </div>
                <button
                    type="button"
                    className="btn btn-dark"
                    onClick={handleSubmit}
                >
                    Submit
                </button>
            </form>
        </div>
    );
}
