
function show_all_tasks() {
    fetch("http://localhost:6432/task?task_id=13", {
        method: "GET",
        headers: {
            'Access-Control-Allow-Origin': '*'
        }
        })
        .then(response => response.json())
        .then(data => console.log(data));
}
