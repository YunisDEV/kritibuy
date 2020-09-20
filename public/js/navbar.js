var pathToPage = {
    '/': 'Home',
    '/index.html': 'Home',
    '/about.html': 'About',
    '/contact.html': 'Contact',
    '/pricing.html': 'Pricing',
    '/blog.html': 'Blog',
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
