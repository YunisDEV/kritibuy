var pathToPage = {
    '/': 'Home',
    '/about': 'About',
    '/contact': 'Contact',
    '/pricing': 'Pricing',
    '/blog': 'Blog',
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
