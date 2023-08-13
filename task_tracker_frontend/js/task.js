const status_to_next_statuses = {
    'Отркыт': [
        'В работу',
        'Требуется информация',
        'Закрыть',
    ],
    'В работе': [
        'На паузу',
        'На ревью',
        'Требуется информация',
        'Закрыть',
    ],
    'В работе (на паузе)': [
        'В работу',
        'На ревью',
        'Требуется информация',
        'Закрыть',
    ],
    'Требуется информация': [
        'Открыть',
        'В работу',
        'Закрыть',
    ],
    'На ревью': [
        'В работу',
        'Требуется информация',
        'Закрыть',
    ],
    'Закрыт': [
        'Переоткрыть',
    ],
}

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
    return date.toLocaleDateString('ru') + ' ' +
        date.toLocaleString('ru', {hour: '2-digit', minute:'2-digit'});
}

function create_comment_card(comment) {
    let card = document.createElement('div');
    card.setAttribute('class', 'card my-3');

    let card_body = document.createElement('div');
    card_body.setAttribute('class', 'card-body');

    let card_subtitle = document.createElement('h6');
    card_subtitle.setAttribute('class', 'card-subtitle mb-2 text-muted');
    card_subtitle.innerText =
        parse_date(comment['created_at']) + ' ' +
        comment['author']['name'] + ' @' + comment['author']['login'] +
        ' добавил комментарий'
    card_body.appendChild(card_subtitle)

    let card_text = document.createElement('p');
    card_text.setAttribute('class', 'card-text');
    card_text.innerText = comment['text'];
    card_body.appendChild(card_text);

    card.appendChild(card_body);
    return card;
}

function show_comments(comments) {
    let comments_div_element = document.getElementById('task_comments');
    clear_children(comments_div_element);
    if (comments.length === 0) {
        comments_div_element.setAttribute('class', 'my-3')
        comments_div_element.innerText = 'Комментариев нет';
        return;
    }
    for (let i = 0; i < comments.length; ++i) {
        let card = create_comment_card(comments[i]);
        comments_div_element.appendChild(card);
    }
}

function handle_comment_add(response) {
    if (response.status === 201) {
        window.location.reload();
        return;
    }

    alert('Что-то пошло не так, сервер вернул ' + response.status);
}

function add_comment() {
    const token = try_get_token();
    let url = window.location.href;

    let task_id_start_idx = url.lastIndexOf('/');
    if (task_id_start_idx === -1) {
        return; // TODO
    }
    let task_id = url.substring(task_id_start_idx + 1);
    let comment_value = document.getElementById('comment_input').value;
    if (comment_value.trim() === '') {
        alert('Комментарий не может быть пустым');
        return;
    }

    let request = {
        'text': comment_value.trim(),
    }
    fetch('http://localhost:6432/api/task/comment/add?' + new URLSearchParams({
        public_id: task_id.trim(),
    }),
        {
            method: 'POST',
            body: JSON.stringify(request),
            headers: {
                'X-User-Token': token,
                'Content-Type': 'application/json',
            },
        })
        .then(response => handle_comment_add(response));
}

function format_spent_time(seconds) {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = Math.floor(((seconds % 3600) % 60));

    return hours + ' ч. ' + minutes + ' мин. ' + secs + ' сек.'
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

    let spent_time_element = document.getElementById('spent_time')
    if (body['spent_time'] !== undefined) {
        spent_time_element.innerText = format_spent_time(body['spent_time']);
    } else {
        spent_time_element.innerText = '-';
    }

    show_comments(body['comments'])
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
