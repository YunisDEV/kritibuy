document.getElementById('add-balance-btn').addEventListener('click', e => {
    Swal.fire({
        html: document.getElementById('coupon-code-template').innerHTML,
        showConfirmButton: false
    }).then(()=>{
    })
})