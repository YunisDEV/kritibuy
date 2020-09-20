const navbar = document.querySelector('nav')
const actionButtons = document.querySelector('#actionbtns')
var navLinks = document.querySelectorAll('.nav-item.nav-link')
var navHoverAnimation = 'hvr-underline-from-left'
function optimize(platform) {
    try {
        if (platform === 'mobile') {
            navbar.style.background = "white"
            navbar.classList.remove('navbar-dark')
            navbar.classList.add('navbar-light')
            actionButtons.classList.remove('navbar-nav')
            actionButtons.classList.add('mobile-action')
            navLinks.forEach(i => {
                i.classList.remove(navHoverAnimation)
            })
        } else if (platform === 'desktop') {
            navbar.style.background = "none"
            navbar.classList.remove('navbar-light')
            navbar.classList.add('navbar-dark')
            try {
                actionButtons.classList.add('navbar-nav')
                actionButtons.classList.remove('mobile-action')
            } catch (e) { console.log(e) }
            navLinks.forEach(i => {
                if (!i.classList.contains('active'))
                    i.classList.add(navHoverAnimation)
            })
        }
    }
    catch (e) {
        console.log(e)
    }
}
if (window.innerWidth < 992) {
    optimize('mobile')
} else {
    optimize('desktop')
}
const resize = () => {
    if (window.innerWidth < 992) {
        optimize('mobile')
    } else {
        optimize('desktop')
    }
}
const scroll = () => {
    document.querySelector('header').style.backgroundPositionY = (window.scrollY / 5) + 'px'
    document.querySelector('header div').style.marginTop = (window.scrollY / 1.5) + 'px'
    document.querySelector('header div').style.opacity = (window.innerHeight - window.scrollY) / window.innerHeight
    if (window.innerWidth < 992) {
        navbar.style.background = "white"
        navbar.classList.remove('navbar-dark')
        navbar.classList.add('navbar-light')
        return null;
    }
    if (window.scrollY < 250) {
        navbar.style.background = "none"
        navbar.classList.remove('navbar-light')
        navbar.classList.add('navbar-dark')
    } else if (window.scrollY >= 250) {
        navbar.style.background = "white"
        navbar.classList.remove('navbar-dark')
        navbar.classList.add('navbar-light')
    }
}