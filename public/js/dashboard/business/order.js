var qs = document.querySelector.bind(document)
var qsa = document.querySelectorAll.bind(document)
const commentSave = (el) => {
    console.log('a')
    var orderID = el.parentNode.parentNode.getAttribute('key')
    var comment = el.parentNode.querySelector('textarea.comment-textarea').value
    fetch('/dashboard/business/order-comment', {
        method: 'POST',
        body: JSON.stringify({
            orderID,
            comment
        })
    }).then((res) => res.json())
        .then((data) => {
            console.log(data)
            if (data.success) location.reload()
            else {
                alert(data.error)
            }
        })
}

qsa('.comment-order-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault()
        var comment = e.target.parentNode.parentNode.parentNode.querySelector('.table-column-comment')
        var inner = comment.innerHTML
        comment.innerHTML = `
        <textarea class="form-control comment-textarea col-md-12 mb-4">${inner}</textarea>
        <button onclick="commentSave(this)" class="btn btn-primary comment-submit-order-btn">Save</button>
        `
        e.target.disabled = true
    })
})

qsa('.add-product-to-list').forEach(i => {
    i.addEventListener('click', (e) => {
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
qsa('.done-order-btn').forEach(i => {
    i.addEventListener('click', (e) => {
        e.preventDefault()
        var orderID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
        fetch('/dashboard/business/order-done', {
            method: 'POST',
            body: JSON.stringify({
                orderID
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

qsa('.order-info-btn').forEach(i => {
    i.addEventListener('click', e => {
        e.preventDefault()
        var orderID = e.target.parentNode.parentNode.parentNode.getAttribute('key')
        fetch('/dashboard/business/order-info', {
            method: 'POST',
            body: JSON.stringify({
                orderID
            })
        }).then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    showModal(generateInvoice(data.data), orderID)
                }
            })
    })
})

function generateInvoice(obj) {
    html = ''
    Object.keys(obj).forEach(key => {
        html += `<h3>${key}</h3> <div class="invoice-body">`
        Object.keys(obj[key]).forEach(k => {
            html += `<p><span>${k}</span><span>${obj[key][k]}</span></p>`
        })
        html += '</div>'
    })
    return html
}
function showModal(html, id) {
    $('#invoiceModal').modal('show');
    $('#invoiceModal .modal-body').html(html)
    $('.modal-footer .btn.btn-primary').click(e => {
        var iframe = document.querySelector('#printableInvoiceFrame')
        iframe.src = '/dashboard/business/order-info/' + id
        var iframeWindow = (iframe.contentWindow || iframe.contentDocument);
        iframeWindow.print()
    })
    console.log('a')
}
var iframe = document.createElement('iframe')
iframe.id = 'printableInvoiceFrame'
iframe.style = 'z-index:-9999!important;opacity:0;'
document.body.appendChild(iframe)