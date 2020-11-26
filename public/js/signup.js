document.querySelector('#country').addEventListener('change', (e) => {
    var country = e.target.value
    axios.post('/get-cities', {
        country
    }).then(({ data }) => {
        if (data.success) {
            var citySelect = document.querySelector('#city')
            var cities = data.data
            var citiesHTML = ''
            for (var i = 0; i < cities.length; i++) {
                citiesHTML += `<option value="${cities[i]}">${cities[i]}</option>`
            }
            citySelect.innerHTML = `
                <option value="" hidden>Select city:</option>
                ${citiesHTML}
                `
            citySelect.disabled = false
        } else {
            window.alert('Could not fetch Cities')
            citySelect.disabled = true
        }
    })
})
document.querySelector('form#signupForm').addEventListener('submit', (e) => {
    e.preventDefault()
    var f = e.target
    e.target.submitBtn.disabled = true
    axios.post('/signup', {
        username: f.username.value,
        email: f.email.value,
        password:f.password.value,
        passwordConfirm:f.passwordConfirm.value,
        permission: f.permission.value,
        country: f.country.value,
        city: f.city.value
    }).then(data => {
        if (data.data.success) {
            window.open('/dashboard', '_self')
        } else {
            const { error } = data.data
            console.log(error)
            var text = error
            document.querySelector('#errorLine').innerHTML = text
        }
    }).finally(() => {
        e.target.submitBtn.disabled = false
    })
})