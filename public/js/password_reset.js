var qs = document.querySelector.bind(document)
qs('#recover-form')?.addEventListener('submit', (e) => {
    e.preventDefault()
    fetch(location.pathname, {
        method: 'POST',
        body: new FormData(e.target)
    }).then(res => res.json())
        .then(data => {
            if (data.success) window.open('/password-recover?success=true', '_self')
            else alert(data.error)
        })
})
qs('#reset-form')?.addEventListener('submit', (e) => {
    e.preventDefault()
    fetch('/' + location.href.split('/').splice(3).join('/'), {
        method: 'POST',
        body: new FormData(e.target)
    }).then(res => res.json())
        .then(data => {
            if (data.success) window.open('/login','_self')
            else alert(data.error)
        })
})