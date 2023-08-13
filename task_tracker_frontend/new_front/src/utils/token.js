export function getTokenFromLocalStorage() {
    let token = localStorage.getItem('X-User-Token')
    if (!token) {
        return ''
    }
    return token
}

export function getNameFromLocalStorage() {
    let name = localStorage.getItem('X-User-Name')
    if (!name) {
        return ''
    }
    return name
}

export function setTokenToLocalStorage(token, name) {
    localStorage.setItem('X-User-Token', token)
    localStorage.setItem('X-User-Name', name)
}
