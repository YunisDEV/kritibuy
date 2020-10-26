qs = document.querySelector.bind(document)
qsa = document.querySelectorAll.bind(document)
qsa('.delete-row-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault()
        var clickedID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
        var d = confirm('Do you want to delete row id: ' + clickedID + '?')
        if (d) {
            fetch(location.pathname, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id:clickedID
                })
            }).then((res) => res.json())
            .then((data) => {
                if (data.success) location.reload()
                else {
                    alert(data.error)
                }
            })
        }
    })
})
qsa('.update-row-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault();
        var clickedID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
    })
})
qs('#add-row-btn').addEventListener('click', () => {
    qs('#add-row').classList.toggle('d-none')
})
qs('#add-row').addEventListener('submit', (e) => {
    e.preventDefault()
    var request_body = {}
    var t = e.target
    for (var i = 0; i < t.length - 1; i++) {
        request_body[t[i].getAttribute('name')] = t[i].value
    }
    fetch(location.pathname, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request_body)
    }).then((res) => res.json())
        .then((data) => {
            if (data.success) location.reload()
            else {
                alert(data.data.error)
            }
        })
})
