# DISCLAIMER
I'm not responsible for how you manage your stuff.  Use are your own risk and understanding.

## What you need
- python 2.7
- pip
## Setup
```bash
pip install requirements.txt
mkdir portfolios
touch portfolios/portfolio-1.txt
```

## Declare your Portfolio
```yaml
usd_investment: 2941
exchange: bittrex

coins:
  - name: Bitcoin
    symbol: btc
    qty: 0.05941182
  - name: Litecoin
    symbol: ltc
    qty: 4.22
  - name: Monero
    symbol: xmr
    qty: 2
  - name: Elastic
    symbol: xel
    qty: 250
  - name: Count.Party
    symbol: xcp
    qty: 4
  - name: Ripple
    symbol: xrp
    qty: 102.00913092
columns:
  - short_name
  - long
```

## Run
```bash
python dashboard.py
```
