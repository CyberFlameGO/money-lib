import abc
from abc import ABC
from decimal import Decimal
from importlib import import_module

from money.exceptions import InvalidExchangeBackend


class BaseBackend(ABC):
    """Abstract base class API for exchange backends."""

    @property
    @abc.abstractmethod
    def base(self):
        """Returns the base currency."""

    @abc.abstractmethod
    def rate(self, currency):
        """Returns quotation between the base and another currency."""

    def quotation(self, origin, target):
        """Returns quotation between two currencies (origin, target)."""

        a = self.rate(origin)
        b = self.rate(target)
        if a and b:
            return b / a
        return None


class SimpleBackend(BaseBackend):
    def __init__(self):
        self._base = None
        self._rates = {}

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, currency):
        self._base = currency

    def set_rate(self, currency, rate):
        self._rates[currency] = rate

    def rate(self, currency):
        if currency == self.base:
            return Decimal(1)
        return self._rates.get(currency, None)


class ExchangeRates:
    def __init__(self):
        self._backend = None

    @property
    def backend(self):
        """Returns the current backend."""

        return self._backend

    @property
    def backend_name(self):
        """Returns the class name of the current backend."""

        return self._backend.__class__.__name__

    @backend.setter
    def backend(self, backend):
        """Sets the current backend."""

        if backend is None:
            self._backend = None
            return

        if isinstance(backend, str):
            path, name = backend.rsplit('.', 1)
            module = import_module(path)
            backend = getattr(module, name)()
        elif isinstance(backend, type):
            backend = backend()

        if not isinstance(backend, BaseBackend):
            raise InvalidExchangeBackend()

        self._backend = backend


xrates = ExchangeRates()