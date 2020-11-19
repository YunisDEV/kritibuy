var qs = document.querySelector.bind(document)
var qsa = document.querySelectorAll.bind(document)
qsa('.delete-order-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault()
        var clickedID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
        var d = confirm('Do you want to delete order id: ' + clickedID + '?\nNote: Customer will get message about order deletion.')
        if (d) {

        }
    })
})
qsa('.done-order-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault()
        var clickedID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
        var d = confirm('Do you want to make order id: ' + clickedID + ' done?\nNote: Customer will get message order is done.')
        if (d) {

        }
    })
})
qsa('.add-product-to-list').forEach(i => {
    i.addEventListener('click', (e) => {
        console.log('a')
        e.preventDefault()
        var productName = e.target.getAttribute('data-product')
        fetch('/dashboard/business/add-product-to-list', {
            method: 'POST',
            body: JSON.stringify({
                productName
            })
        }).then((res) => res.json())
            .then((data) => {
                console.log(data)
                if (data.success) location.reload()
                else {
                    alert(data.error)
                }
            })
    })
})