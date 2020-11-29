document.querySelector("#add-balance-btn").addEventListener("click", (e) => {
    Swal.fire({
        showConfirmButton: false,
        html: document.getElementById("coupon-code-template").innerHTML,
    });
    document.getElementById("apply-coupon-code").addEventListener("submit", (e) => {
        e.preventDefault()
        fetch("/dashboard/apply-coupon-code", {
            method: "POST",
            body: new FormData(e.target),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) location.reload();
                else
                    Swal.fire({
                        icon: "error",
                        text: data.error,
                    });
            });
    });
});
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
                else Swal.fire({
                    icon:'error',
                    text:data.error
                })
            })
    })
})