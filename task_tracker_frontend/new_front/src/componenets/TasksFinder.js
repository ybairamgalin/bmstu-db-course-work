import React, {useState} from "react";

import {API_PATH} from "../constants";
import {getTokenFromLocalStorage} from "../utils/token";

import ColTextInput from "./ColTextInput";
import ColOption from "./ColOption";
import TasksTable from "./TasksTable";
import Pagination from "./Pagination";

import {fetchPost} from "../utils/fetch";

const LIMIT = 10

export default function TasksFinder() {
    const [taskName, setTaskName] = useState()
    const [executor, setExecutor] = useState()

    const [tasks, setTasks] = useState([])
    const [error, setError] = useState()
    let cursor = null

    async function fetchTasks() {
        let request_body = {
            limit: LIMIT
        }
        if (taskName) {
            request_body['name_part'] = taskName
        }
        if (executor) {
            request_body['executor_username'] = executor
        }
        if (tasks && tasks['cursor']) {
            request_body['cursor'] = tasks['cursor']
        }
        let response_tasks = await fetchPost(
            API_PATH + '/tasks/info',
            request_body,
            {
                'Content-Type': 'application/json',
                'X-User-Token': getTokenFromLocalStorage(),
            },
            setError
        )
        setTasks(response_tasks)
    }

    return (
        <div className="d-flex flex-fill flex-column p-3">
            <div className="my-2">
                <form>
                    <div className="row"><h2>Все задачи</h2></div>
                    <p className="text-danger">{error}</p>
                    <div className="row my-3">
                        <ColTextInput
                            placeholder='Название'
                            onChange={e => (setTaskName(e.target.value))}
                        />
                        <ColTextInput
                            placeholder='Исполнитель'
                            onChange={e => (setExecutor(e.target.value))}
                        />
                        <ColTextInput placeholder='Теги' id='tags'/>
                        <ColOption
                            options={['Время создания', 'Время обновления']}
                            text={'Сортировать по'}
                        />
                    </div>
                    <button
                        id="find_tasks"
                        type="button"
                        className="btn btn-dark"
                        onClick={async (e) => {
                            if (tasks && tasks.cursor) {
                                tasks.cursor = null
                            }
                            await fetchTasks()
                        }}
                    >
                        Найти!
                    </button>
                </form>
            </div>
            <div className="my-2">
                <TasksTable tasks={tasks['tasks']}/>
            </div>
            {(tasks && tasks.tasks && tasks.tasks.length >= LIMIT) ? (
                <div className="my-2">
                    <Pagination fetchNext={fetchTasks}/>
                </div>
            ) : ('')}
        </div>
    );
}


