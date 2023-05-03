function clear_children(node) {
    let first = node.firstElementChild
    while (first) {
        first.remove()
        first = node.firstElementChild
    }
}

function show_error_message(msg) {
    let error_div = document.getElementById('message_area')
    clear_children(error_div)
    let text = document.createElement('p')
    text.appendChild(document.createTextNode(msg))
    text.setAttribute('class', 'text-danger')
    error_div.appendChild(text)
}

function handle_registry(data) {
    if (data.status === 409) {
        show_error_message('Пользователь с таким именем уже существует')
        return;
    }
    if (data.status !== 201) {
        show_error_message(data.status);
        return;
    }

    window.location.replace('http://localhost/auth');
}

function signup() {
    let username = document.getElementById('login_input').value;
    let password = document.getElementById('password_input').value;
    let repeated_password = document.getElementById('repeat_password_input').value
    let name = document.getElementById('name_input').value;

    if (username.length < 5) {
        show_error_message('Логин должен быть не менее 5 символов');
        return;
    }
    if (name.length < 3) {
        show_error_message('Имя должно быть не менее 3 символов');
        return;
    }
    if (password.length < 5) {
        show_error_message('Пароль должен быть не менее 5 символов');
        return;
    }
    if (password !== repeated_password) {
        show_error_message('Введенные пароли не совпадают');
        return;
    }

    let request = {
        'username': username,
        'hashed_password': password,
        'name': name
    }

    fetch('http://localhost:6432/api/user/create', {
        method: 'POST',
        body: JSON.stringify(request),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(data => handle_registry(data))
}