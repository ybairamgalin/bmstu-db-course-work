import React from "react";

import toDateToShow from "../utils/date";

function Headers({headers}) {
    return (
        <thead>
        <tr>
            {headers.map(header => {
                return <th key={header}>{header}</th>
            })}
        </tr>
        </thead>
    )
}

function TableCell({index, task}) {
    return (
        <tr
            onClick={() => {window.location = ('/task/' + task.public_id)}}
            style={
                {cursor: 'pointer'}
            }
        >
            <td>{index}</td>
            <td>{task.title}</td>
            <td>{task.creator.name}</td>
            <td>{task.executor?.name}</td>
            <td>{toDateToShow(task.created_at)}</td>
            <td>{toDateToShow(task.updated_at)}</td>
        </tr>
    )
}

function TableBody({tasks}) {
    return (
        <tbody>
        {tasks?.map((task, index) => {
            return <TableCell key={index + 1} index={index + 1} task={task}></TableCell>
        })}
        </tbody>
    )
}

export default function TasksTable({tasks}) {
    return (
        <table className='table table-hover'>
            <Headers
                headers={['#', 'Название', 'Создатель', 'Исполнитель', 'Создана', 'Обновлена']}
            />
            <TableBody tasks={tasks}/>
        </table>
    );
}
