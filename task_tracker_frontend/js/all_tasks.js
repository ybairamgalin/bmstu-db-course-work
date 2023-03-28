function create_sell(value, ref = null) {
    let element = document.createElement("td")
    if (!ref) {
        element.appendChild(document.createTextNode(value))
        return element
    }
    let link_element = document.createElement("a")
    link_element.appendChild(document.createTextNode(value))
    link_element.setAttribute('href', ref)
    link_element.setAttribute('class', 'link-dark')
    element.appendChild(link_element)
    return element
}

function create_table_row(row_number, task) {
    let row = document.createElement("tr")
    row.appendChild(create_sell(row_number.toString()))
    row.appendChild(create_sell('FRONT'))
    row.appendChild(create_sell(task['title'], `/task/${task['public_id']}`))
    row.appendChild(create_sell(task['creator']))
    row.appendChild(create_sell(task['executor']))
    row.appendChild(create_sell(task['created_at']))
    row.appendChild(create_sell(task['updated_at']))

    return row
}
function display_tasks(tasks) {
    let rows = document.getElementById('task_table_rows')

    let first = rows.firstElementChild
    while (first) {
        first.remove()
        first = rows.firstElementChild
    }

    for (let i = 0; i < tasks['tasks'].length; i++) {
        rows.appendChild(create_table_row(i + 1, tasks['tasks'][i]))
    }
    rows.append()
}

function show_all_tasks() {
    let request_body = {
        'cursor': 'ladksfjlkdj',
        'name_part': document.getElementById('task_search_field').value
    }

    fetch('http://localhost:6432/api/task/info', {
            method: 'POST',
            body: JSON.stringify(request_body),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => display_tasks(data))
}
