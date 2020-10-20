var primaryColor = '#2ab4a6'
var primaryDark = '#229287'
var primaryLight = '#33dac9'
var primaryLightTransparent = '#33dac96b'
document.querySelector('#themevars').innerHTML = `
    :root {
        --primary-color: ${primaryColor};
        --primary-dark: ${primaryDark};
        --primary-light: ${primaryLight};
        --primary-light-transparent: ${primaryLightTransparent};
    }
`
document.querySelector('#themevars').insertAdjacentHTML('afterend', `
    <link rel="apple-touch-icon" sizes="180x180" href="/meta/apple-touch-icon.png" />
    <link rel="icon" type="image/png" sizes="32x32" href="/meta/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/meta/favicon-16x16.png" />
    <link rel="manifest" href="/meta/site.webmanifest" />
    <link rel="mask-icon" href="/meta/safari-pinned-tab.svg" color="#00aba9" />
    <meta name="msapplication-TileColor" content="#00aba9" />
    <meta name="theme-color" content="#2ab4a6" />
`)
document.querySelector('meta[name="viewport"]').insertAdjacentHTML('afterend', `
    <meta name="description" content="Buy and Sell almost everything with help of Artificial Intelligence." />
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://kritibuy.com/">
    <meta property="og:title" content="Kritibuy - AI Assisted Shopping">
    <meta property="og:description" content="Buy and Sell almost everything with help of Artificial Intelligence.">
    <meta property="og:image" content="/meta/Banner.png">
    <meta property="og:site_name" content="kritibuy.com" />
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://kritibuy.com/">
    <meta property="twitter:title" content="Kritibuy - AI Assisted Shopping">
    <meta property="twitter:description" content="Buy and Sell almost everything with help of Artificial Intelligence.">
    <meta property="twitter:image" content="/meta/Banner.png">
    <meta name="keywords" content="buy, chat, order, sell, ai assistant, brand, business, personal" />
`)
