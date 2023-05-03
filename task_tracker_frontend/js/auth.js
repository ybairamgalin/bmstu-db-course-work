
function clear_children(node) {
    let first = node.firstElementChild
    while (first) {
        first.remove()
        first = node.firstElementChild
    }
}

function clear_password() {
    document.getElementById('password_input').value = ''
}

function show_error_message(msg) {
    let error_div = document.getElementById('message_area')
    clear_children(error_div)
    let text = document.createElement('p')
    text.appendChild(document.createTextNode(msg))
    text.setAttribute('class', 'text-danger')
    error_div.appendChild(text)
}

function validate_auth(response) {
    let token_string = 'x-user-token'

    if (response.status !== 200) {
        show_error_message('Неправильный логин или пароль')
        clear_password()
        localStorage.removeItem(token_string)
        return
    }
    response.json().then(body => {
        localStorage.setItem(token_string, body['X-User-Token']);
        localStorage.setItem('task_tracker_name', body['name']);
        window.location.replace('http://localhost/');
    })
}

function auth() {
    let username = document.getElementById('login_input').value;
    let password = document.getElementById('password_input').value;

    if (username === '') {
        show_error_message('Имя пользователя пусто');
        return;
    }
    if (username.length < 5) {
        show_error_message('Имя пользователя не может содержать менее 5 символов')
        return;
    }
    if (password === '') {
        show_error_message('Пароль пуст')
        return;
    }

    let hashed_password = password /* TODO add hashing */;

    let request = {
        'username': username,
        'hashed_password': hashed_password
    }

    fetch('http://localhost:6432/api/user/auth', {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(data => validate_auth(data))
}