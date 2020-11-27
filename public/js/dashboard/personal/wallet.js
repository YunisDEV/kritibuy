document.getElementById('add-balance-btn').addEventListener('click', e => {
    Swal.fire({
        html: document.getElementById('coupon-code-template').innerHTML,
        showConfirmButton: false
    }).then(()=>{
    })
    document.getElementById('apply-coupon-code').addEventListener('submit',e=>{
        e.preventDefault()
        e.target.subBtn.disabled = true
        console.log('b')
    })
})