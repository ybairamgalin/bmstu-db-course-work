let tags = []

function try_get_token() {
    if (localStorage.getItem('x-user-token')) {
        return localStorage.getItem('x-user-token');
    }

    window.location.replace('http://localhost/auth');
}

function parse_executor_name(string) {
    if (string === 'Не назначен') {
        return -1;
    }
    if (Array.from(string).indexOf('@') === -1) {
        return null;
    }
    return string.slice(
        Array.from(string).indexOf('@')
    ).trim()
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function clear_children(node) {
    let first = node.firstElementChild
    while (first) {
        first.remove()
        first = node.firstElementChild
    }
}

function display_tags() {
    let tags_div = document.getElementById('tags_div');
    clear_children(tags_div)
    for (let i = 0; i < tags.length; i++) {
        let tag_span = document.createElement('span');
        tag_span.setAttribute('class','badge bg-secondary my-2 mx-1');
        tag_span.appendChild(document.createTextNode(tags[i]));
        tags_div.appendChild(tag_span);
    }
}

function handle_tag_input_change() {
    let tag_input = document.getElementById('input_task_tag');
    let tag_value = tag_input.value;
    if (tag_value.length === 0) {
        return;
    }
    if (Array.from(tag_value)[tag_value.length - 1] === ' ') {
        tag_value.trim()
        if (tag_value.length > 0 && tags.indexOf(tag_value.trim()) === -1) {
            tags.push(tag_value.trim());
            display_tags();
        }
        tag_input.value = '';
    }
}

function show_suggests(response) {
    if (response.status !== 200) {
        return;
    }

    response.json().then(body =>{
        let datalist = document.getElementById('list_task_executor_suggests')
        clear_children(datalist)
        if (body['users'].length === 0) {
            return
        }
        for (let i = 0; i < body['users'].length; i++) {
            let option = document.createElement('option')
            option.appendChild(document.createTextNode(
                body['users'][i]['name'] + ' @' + body['users'][i]['login']))
            datalist.appendChild(option)
        }
    })
}

async function handle_executor_input_change() {
    let executor_input = document.getElementById('input_task_executor');
    let executor_input_value = executor_input.value;
    if (executor_input_value.length < 2) {
        return;
    }
    let string_copy = (' ' + executor_input_value).slice(1);
    await sleep(750);
    if (string_copy !== executor_input.value) {
        return;
    }

    let token = try_get_token();
    fetch('http://localhost:6432/api/users/find?' + new URLSearchParams({
        query: executor_input_value.trim()
    }),
    {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Token': token,
            }
        })
        .then(response => show_suggests(response))
}

function handle_creation(data) {
    let status = data.status;

    data.json().then(body=>{
       if (status === 201) {
           window.location.replace('http://localhost/task/' + body['id']);
           return;
       }
       alert(status);
    });
}

function create_task() {
    let token = try_get_token();
    let task_name = document.getElementById('input_task_title').value;
    if (task_name.length === 0) {
        return; // TODO
    }
    let task_content = document.getElementById('input_task_description').value;
    let executor = parse_executor_name(
        document.getElementById('input_task_executor').value);
    if (executor == null) {
        return; // TODO
    }

    let request = {
        title: task_name,
        content: task_content,
        tags: tags
    }
    if (executor !== -1) {
        request['executor_username'] = executor;
    }

    fetch('http://localhost:6432/api/task', {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json',
            'X-User-Token': token
        }
    })
    .then(data => handle_creation(data))
}
