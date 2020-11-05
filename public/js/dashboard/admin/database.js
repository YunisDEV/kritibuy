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
                    id: clickedID
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
qs('#add-row-btn').addEventListener('click', () => {
    qs('#add-row').classList.toggle('d-none')
})
qs('#add-row').addEventListener('submit', (e) => {
    e.preventDefault()
    fetch(location.pathname, {
        method: 'POST',
        body: new FormData(e.target)
    }).then((res) => res.json())
        .then((data) => {
            console.log(data)
            if (data.success) location.reload()
            else {
                alert(data.data.error)
            }
        })
})
