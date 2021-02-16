// Nomics API

let url = 'https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids=BTC,ETH&interval=1d&convert=USD&per-page=100&page=1';

fetch(url, {method: 'GET'
}).then((response) => {
        response.json().then((jsonResponse) => {
            console.log(jsonResponse)
        })
        response.json().then(i => i.forEach(i => console.log(i.price)))
    }).catch((err) => {
        console.log(`Error: ${err}`)
    });


//Coinmarketcap API

// let url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=aeeff74b-6d72-42b7-92b1-4483ed97f455&start=1&limit=5&convert=USD'

// fetch(url)
//     .then(function(resp) {
//         console.log(resp);
//     });