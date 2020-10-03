document.querySelector('#country').addEventListener('change', (e) => {
    var country = e.target.value
    fetch('/get-cities', {
        method: 'POST',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            country
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                var citySelect = document.querySelector('#cities')
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