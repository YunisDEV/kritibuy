var qs = document.querySelector.bind(document)
qs('#addinfoform').addEventListener('submit', (e) => {
    e.preventDefault()
    fetch(location.pathname, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            fullName: e.target.fullName.value,
            address: e.target.address.value,
            phone: e.target.phone.value
        })
    }).then(res => res.json())
        .then(data => {
            if (data.success) {
                window.open('/dashboard/personal','_self')
            }
        })
})