function try_get_token() {
    if (localStorage.getItem('x-user-token')) {
        return localStorage.getItem('x-user-token');
    }

    window.location.replace('http://localhost/auth');
}

function show_user_data() {
    let paragraph = document.getElementById('username_paragraph');
    let username = localStorage.getItem('task_tracker_name');
    paragraph.appendChild(document.createTextNode(username));
}

window.onload = function load_topics() {
    const token = try_get_token();
    show_user_data();

    fetch('http://localhost:6432/api/topic/info', {
        method: 'GET',
        headers: {'X-User-Token': token},
    })
    .then(response => response.json())
    .then(data => show_topics(data))
}

function show_topics(data) {
    let topics_dropdown = document.getElementById('topic_select')
    clear_children(topics_dropdown)
    data['topics'].splice(0, 0, {'id': 0, 'name': 'ANY'})

    for (let i = 0; i < data['topics'].length; i++) {
        let new_option = document.createElement('option')
        let option_text = document.createTextNode(
            data['topics'][i]['name'].toUpperCase())
        new_option.setAttribute('value', data['topics'][i]['id'])
        new_option.appendChild(option_text)
        topics_dropdown.appendChild(new_option)
    }
}

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
    let title = task['title']
    if (title.length > 30) {
        title = title.substring(0, 29) + '. . .'
    }
    let executor = task['executor']
    if (executor == null) {
        executor = 'не назначен'
    }

    let row = document.createElement("tr")
    row.appendChild(create_sell(row_number.toString()))
    row.appendChild(create_sell('FRONT'))
    row.appendChild(create_sell(title, `/task/${task['public_id']}`))
    row.appendChild(create_sell(task['creator']))
    row.appendChild(create_sell(executor))
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

    let selected_topic = Number(
        document.getElementById('topic_select').value)
    if (selected_topic !== 0) {
        request_body['topic_id'] = selected_topic
    }
    const token = try_get_token()

    fetch('http://localhost:6432/api/task/info', {
            method: 'POST',
            body: JSON.stringify(request_body),
            headers: {
                'Content-Type': 'application/json',
                'X-User-Token': token,
            }
        })
        .then(response => response.json())
        .then(data => display_tasks(data))
}

