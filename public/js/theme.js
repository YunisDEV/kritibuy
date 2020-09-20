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
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#00aba9" />
        <meta name="msapplication-TileColor" content="#00aba9" />
        <meta name="theme-color" content="#2ab4a6" />
`)
document.querySelector('meta[name="viewport"]').insertAdjacentHTML('afterend',`
<meta name="description" content="Buy/Sell everything through texting" />
        <meta property="og:type" content="webpage" />
        <meta property="og:title" content="Kritibuy" />
        <meta property="og:description" content="Buy/Sell everything through texting" />
        <meta property="og:image" content="" />
        <meta property="og:site_name" content="kritibuy.com" />
        <meta name="keywords" content="buy, chat, order, sell, ai assistan, brand, business, business plus, personal" />
        <meta http-equiv="expires" content="3600" />
`)