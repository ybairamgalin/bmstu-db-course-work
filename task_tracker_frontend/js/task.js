function try_get_token() {
    if (localStorage.getItem('x-user-token')) {
        return localStorage.getItem('x-user-token');
    }

    window.location.replace('http://localhost/auth');
}

function clear_children(node) {
    let first = node.firstElementChild
    while (first) {
        first.remove()
        first = node.firstElementChild
    }
}

function display_tags(tags) {
    let tags_div = document.getElementById('tags_div');
    clear_children(tags_div);
    if (tags.length === 0) {
        tags_div.innerText = '-';
        return;
    }

    for (let i = 0; i < tags.length; i++) {
        let tag_span = document.createElement('span');
        tag_span.setAttribute('class', 'badge bg-secondary mx-1');
        tag_span.appendChild(document.createTextNode(tags[i]));
        tags_div.appendChild(tag_span);
    }
}

function parse_date(date_string) {
    let date = new Date(date_string + 'Z');
    // return date.getDay() + '.' + date.getMonth() + '.' + date.getFullYear() +
    //     ' ' + date.getHours() + ':' + date.getMinutes();

    return date.toLocaleDateString('ru') + ' ' +
        date.toLocaleString('ru', {hour: '2-digit', minute:'2-digit'});
}


function show_task(body) {
    let task_name_element = document.getElementById('task_name');
    clear_children(task_name_element);
    task_name_element.appendChild(document.createTextNode(body['title']));

    let task_status_element = document.getElementById('status_button')
    clear_children(task_status_element)
    task_status_element.innerText = body['status']

    let task_content = body['content'];
    if (task_content === undefined) {
        task_content = 'Отсутствует';
    } else {
        task_content.replace('\\n', '<br>')
    }
    let task_content_element = document.getElementById('task_content');
    clear_children(task_content_element);
    task_content_element.innerText = task_content;

    let task_creator_element = document.getElementById('task_creator');
    clear_children(task_creator_element);
    task_creator_element.appendChild(document.createTextNode(
        body['creator']['name'] + ' @' + body['creator']['login']
    ))

    let executor = 'Не назначен'
    if (body['executor'] !== undefined) {
        executor = body['executor']['name'] + ' @' + body['executor']['login']
    }
    let task_executor_element = document.getElementById('task_executor');
    clear_children(task_executor_element);
    task_executor_element.appendChild(document.createTextNode(executor));

    display_tags(body['tags'])

    let created_at_element = document.getElementById('created_at');
    created_at_element.innerText = parse_date(body['created_at']);
    let updated_at_element = document.getElementById('updated_at');
    updated_at_element.innerText = parse_date(body['updated_at']);
}

function handle_task_response(response) {
    let status_code = response.status;
    response.json().then(body => {
        if (status_code === 200) {
            show_task(body);
            return;
        }

        alert(status_code)
    })
}

window.onload = function handle_task_screen_load() {
    const token = try_get_token();
    let url = window.location.href;

    let task_id_start_idx = url.lastIndexOf('/');
    if (task_id_start_idx === -1) {
        return; // TODO
    }
    let task_id = url.substring(task_id_start_idx + 1);

    fetch('http://localhost:6432/api/task?' + new URLSearchParams({
        public_id: task_id.trim(),
    }),
        {
            method: 'GET',
            headers: {'X-User-Token': token},
        })
        .then(response => handle_task_response(response))
}
