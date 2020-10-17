var messageForm = document.querySelector('.chat_inputs form')
var messageBx = document.querySelector('.chat_body')
messageForm.addEventListener('submit', (e) => {
    e.preventDefault()
    var message = e.target.message.value
    messageBx.insertAdjacentHTML('beforeend', `
    <div class="chat_message_part">
        <div class="chat_message me">
            <div>
                <p>${message}</p>
            </div>
        </div>
    </div>
    `)
    autoscroll()
    axios.post('/query', {
        "queryText": message
    })
        .then(response => {
            messageBx.insertAdjacentHTML('beforeend', `
            <div class="chat_message_part">
                <div class="chat_message you">
                    <div>
                        <p>${response.data.response}</p>
                    </div>
                </div>
            </div>
            `)
            autoscroll()
        })
    e.target.message.value = ''
})
function autoscroll() {
    messageBx.scrollTop = messageBx.scrollHeight
}
autoscroll()