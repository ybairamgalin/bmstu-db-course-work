async function fetchImpl(url, method, expected_response, body, headers, setError) {
    let request_init = {
        method: method
    }
    if (body) {
        request_init['body'] = JSON.stringify(body)
    }
    if (headers) {
        request_init['headers'] = headers
    }
    let response = await fetch(url, request_init)
    if (response.status === 401) {
        window.location = '/auth'
    }
    if (response.status === expected_response) {
        return await response.json()
    }
    if (setError) {
        let json = await response.json()
        setError(json['detail'])
    }
    throw new Error(url + ' responded with ' + response.status)
}

export async function fetchPost(
    url, body = null, headers = null, setError = null, expected_response=200
){
    return await fetchImpl(url, 'POST', expected_response, body, headers, setError)
}
