var wave1 = $('#feel-the-wave').wavify({
    height: 80,
    bones: 4,
    amplitude: 50,
    color: primaryDark,
    speed: .15
});

var wave2 = $('#feel-the-wave-two').wavify({
    height: 60,
    bones: 3,
    amplitude: 40,
    color: primaryLightTransparent,
    speed: .25
});
$(document).ready(function () {
    $('.first-button').on('click', function () {
        $('.animated-icon1').toggleClass('open');
    });
});
var navLinks = document.querySelectorAll('.nav-item.nav-link')
var pathToPage = {
    '/dashboard/personal': 'Order',
    '/dashboard/personal/order': 'Order',
    '/dashboard/personal/stats': 'Stats',
    '/dashboard/personal/wallet': 'Wallet',
    '/dashboard/personal/contact': 'Contact'
}
var pageNow = pathToPage[window.location.pathname]
if (pageNow) {
    navLinks.forEach(i => {
        if (i.innerHTML == pageNow) {
            i.setAttribute('href', '#')
            i.classList.add('active')
        }
    })
    document.querySelector('title').innerHTML += " &mdash; " + pathToPage[window.location.pathname]
}
function ToggleChatPage() {
    document.querySelector('.chat-modal-mobile').classList.toggle('hide')
}
var newMessages = document.querySelectorAll('.message.new')
newMessages.forEach((i) => {
    i.insertAdjacentHTML('beforeend', '<div class="dot"></div>')
})
document.addEventListener('change',()=>{
    newMessages.forEach((i) => {
        i.insertAdjacentHTML('beforeend', '<div class="dot"></div>')
    })
})
var messagesPARTS = document.querySelectorAll('.message')
messagesPARTS.forEach(i=>{
    i.setAttribute('onclick','ToggleChatPage()')
})