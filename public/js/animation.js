var path = window.location.pathname
var pathToPage = {
    '/': 'Home',
    '/about': 'About',
    '/contact': 'Contact',
    '/pricing': 'Pricing',
    '/blog': 'Blog',
}
if (pathToPage[path] === 'Home') {
    $(window).on("load", function () {
        document.querySelector('#header-title-text').innerHTML = ''
        new Typed('#header-title-text', {
            strings: ["Order anything with just texting", "Sell anything with just texting"],
            typeSpeed: 30,
            loop: true, 
            showCursor: false,
            onStringTyped() {
                let el = document.querySelector('#header-title-text')
                let str = el.innerHTML
                let arr = str.split(' ')
                let sum = '<span class="texting-word">' + arr[arr.length - 1] + '</span>'
                arr[arr.length - 1] = sum
                el.innerHTML = arr.join(' ')
                document.querySelector('.texting-word').classList.add('animation-for-header-home')
                setTimeout(() => {
                    document.querySelector('.texting-word').classList.remove('animation-for-header-home')
                }, 2000)
            },
            backDelay: 2000,
            backSpeed: 20
        })
    })
} else if (pathToPage[path]) {
    $(window).on("load", function () {
        let el = document.querySelector('#header-title-text')
        let arr = pathToPage[path].split('')
        let arr2 = arr.slice(1)
        let part = '<span class="animation-for-header">' + arr.join('') + '</span>'
        el.innerHTML = part
    })
}
var wave1 = $('#feel-the-wave').wavify({
    height: 80,
    bones: 4,
    amplitude: 50,
    color: 'white',
    speed: .15
});

var wave2 = $('#feel-the-wave-two').wavify({
    height: 60,
    bones: 3,
    amplitude: 40,
    color: 'rgba(255, 255, 255, .8)',
    speed: .25
});
$(document).ready(function () {
    $('.first-button').on('click', function () {
        $('.animated-icon1').toggleClass('open');
    });
});