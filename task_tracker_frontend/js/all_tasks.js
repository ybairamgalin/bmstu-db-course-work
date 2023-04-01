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

function clear_children(node) {
    let first = node.firstElementChild
    while (first) {
        first.remove()
        first = node.firstElementChild
    }
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

function create_head_cell(name) {
    let cell = document.createElement('th')
    cell.appendChild(document.createTextNode(name))
    cell.setAttribute('scope', 'col')
    return cell
}

function create_empty_table() {
    let thead = document.createElement('thead')
    thead.appendChild(create_head_cell('#'))
    thead.appendChild(create_head_cell('Топик'))
    thead.appendChild(create_head_cell('Название'))
    thead.appendChild(create_head_cell('Создатель'))
    thead.appendChild(create_head_cell('Исполнитель'))
    thead.appendChild(create_head_cell('Создано'))
    thead.appendChild(create_head_cell('Обновлено'))

    let table_body = document.createElement('tbody')
    table_body.setAttribute('id', 'task_table_rows')

    let table = document.createElement('table')
    table.setAttribute('class', 'table')
    table.setAttribute('id', 'class_table')
    table.appendChild(thead)
    table.appendChild(table_body)

    let table_div = document.getElementById('table_zone')
    clear_children(table_div)
    table_div.appendChild(table)
}

function show_message(msg) {
    let text = document.createElement('h3')
    text.setAttribute('class', 'my-3')
    text.appendChild(document.createTextNode(msg))

    let table_div = document.getElementById('table_zone')
    clear_children(table_div)
    table_div.appendChild(text)
}

function display_tasks(tasks) {
    if (tasks['tasks'].length === 0) {
        show_message('К сожалению ничего не нашлось')
        return
    }

    create_empty_table()
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
