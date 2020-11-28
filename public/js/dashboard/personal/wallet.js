document.getElementById('add-balance-btn').addEventListener('click', e => {
    Swal.fire({
        html: document.getElementById('coupon-code-template').innerHTML,
        showConfirmButton: false
    }).then(() => {
    })
})
document.getElementById('send-money-btn').addEventListener('click', e => {
    Swal.fire({
        html: document.getElementById('send-money-template').innerHTML,
        showConfirmButton: false
    }).then(() => {

    })
    document.querySelector('#send-money-form').addEventListener('submit', (e) => {
        e.preventDefault()
        fetch('/dashboard/send-money', {
            method: 'POST',
            body: new FormData(e.target)
        }).then(res => res.json())
            .then(data=>{
                if(data.success) location.reload()
                else window.alert(data.error)
            })
    })
})