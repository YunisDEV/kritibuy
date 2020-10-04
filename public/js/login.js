document.querySelector('form#loginForm').addEventListener('submit', (e) => {
    e.preventDefault()
    var f = e.target
    e.target.submitBtn.disabled = true
    axios.post('/login', {
        username: f.username.value,
        password:f.password.value
    }).then(data => {
        if (data.data.success) {
            window.open('/dashboard', '_self')
        } else {
            const { error } = data.data
            var text = ''
            if (error.type == 'WRONG_CREDENTIALS') {
                text = 'Please check your credentials.'
            }
            document.querySelector('#errorLine').innerHTML = text
        }
    }).finally(() => {
        e.target.submitBtn.disabled = false
    })
})