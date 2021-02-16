```python
import requests
import json
```


```python
w = requests.get('https://api.nomics.com/v1/currencies/ticker?key=ea386addbac03f4bb67ceb1f333a8d0a&ids=BTC,ETH&interval=1d&convert=USD&per-page=100&page=1')
```


```python
data = w.json()
```


```python
bit = data[0]['price']
eth = data[1]['price']

print(bit,eth)
```

    48947.13101467 1794.69075522
    

Current holdings:
    - Bitcoin = 0.981
    - Ethereum = 24.294


```python
bitH = 0.981
ethH = 24.294

eth = eth*ethH
bit = bitH*bit

value = eth+bit

Print('Current Value is: 'value)
```
