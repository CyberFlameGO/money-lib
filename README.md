# money-lib

![PyPI - Version](https://img.shields.io/pypi/v/money-lib.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/money-lib.svg)
![PyPI - License](https://img.shields.io/pypi/l/money-lib.svg)

Python 3 money lib with decimal precision and currency exchange support.

## Installation

Install the latest release with:
```
pip install money-lib
```

## Usage

A Money object can be created with an *amount* (can be any valid value in `decimal.Decimal(value)`) and a *currency* (can be a string or a `Currency(code)` object).

```python
>>> from money.money import Money
>>> money = Money('7.37', 'USD')
>>> money
USD 7.37
```

Money objects are immutable by convention and hashable. Once created, you can use read-only properties *real* (decimal.Decimal), *amount* (decimal.Decimal) and *currency* (str) to access its internal components.
The *real* property returns the stored amount used for calculations and *amount* returns the amount rounded to the correct number of decimal places for the currency.

```python
>>> money = Money('6.831', 'USD')
>>> money.real
Decimal('6.831')
>>> money.amount
Decimal('6.83')
>>> money.currency
USD
```

Money emulates a numeric type and you can apply most arithmetic and comparison operators between money objects, integers (int) and decimal numbers (decimal.Decimal).

```python
>>> money = Money('5', 'USD')
>>> money / 2
USD 2.50
>>> money + Money('10', 'USD')
USD 15.00
```

All arithmetic operators support automatic currency conversion as long as you have a [currency exchange backend](#currency-exchange) setup.
The currency of the leftmost object has priority.

```python
# Assuming the rate from USD to EUR is 2
>>> money = Money('7.50', 'USD')
>>> money + Money('5', 'EUR')
USD 10.00
```

## Currency exchange

Currency exchange works by setting a backend class that implements the abstract base class `money.exchange.BaseBackend`.
Its API is exposed through `money.xrates`, along with `xrates.backend` and `xrates.backend_name`.

A simple proof-of-concept backend `money.exchange.SimpleBackend` is included.

```python
from decimal import Decimal
from money.money import Money, xrates

xrates.backend = 'money.exchange.SimpleBackend'
xrates.base = 'USD'
xrates.setrate('AAA', Decimal('2'))
xrates.setrate('BBB', Decimal('8'))

a = Money(1, 'AAA')
b = Money(1, 'BBB')

assert a.to('BBB') == Money('4', 'BBB')
assert b.to('AAA') == Money('0.25', 'AAA')
assert a + b == Money('1.25', 'AAA')
```

## Credits

Most of the code is based of https://github.com/carlospalol/money.

Currencies list was taken from https://github.com/sebastianbergmann/money.