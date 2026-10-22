"""Pure adapter around an injected, externally pinned rational codec.

Preparation only. Importing this file is reserved for a separately authorized
unit. No tail module is imported here. The caller pins the injected dependency.
"""
from fractions import Fraction

INPUT_BITS = 512
INTERMEDIATE_BITS = 4096
MAX_INPUT_TEXT = 156


class InvalidRational(ValueError):
    """The injected codec or its bounded canonical postcondition failed."""


class RationalResourceLimit(ValueError):
    """A conservative precheck refused an integer intermediate."""


class ExactArithmetic:
    """Exact rational operations with pre-product and pre-addition bit guards."""

    def __init__(self, rational_parser):
        if not callable(rational_parser):
            raise InvalidRational("INJECTED_CODEC_REQUIRED")
        self._parser = rational_parser

    @staticmethod
    def _integer(value, limit):
        if type(value) is not int or abs(value).bit_length() > limit:
            raise RationalResourceLimit("INTEGER_BIT_LIMIT_OR_TYPE")
        return value

    @classmethod
    def _fraction(cls, value):
        if type(value) is not Fraction:
            raise InvalidRational("INTERNAL_FRACTION_TYPE")
        cls._integer(value.numerator, INTERMEDIATE_BITS)
        cls._integer(value.denominator, INTERMEDIATE_BITS)
        if value.denominator <= 0:
            raise InvalidRational("INTERNAL_DENOMINATOR")
        return value

    @classmethod
    def _make(cls, numerator, denominator):
        cls._integer(numerator, INTERMEDIATE_BITS)
        cls._integer(denominator, INTERMEDIATE_BITS)
        if denominator <= 0:
            raise InvalidRational("INTERNAL_NONPOSITIVE_DENOMINATOR")
        # Fraction normalizes these already bounded integers using gcd.
        return cls._fraction(Fraction(numerator, denominator))

    def parse(self, value):
        # This is a size/shape guard and a codec postcondition, not a copied parser.
        if type(value) is not dict or set(value) != {"numerator", "denominator"}:
            raise InvalidRational("RATIONAL_SHAPE")
        if any(type(value[k]) is not str or not 1 <= len(value[k]) <= MAX_INPUT_TEXT
               for k in ("numerator", "denominator")):
            raise InvalidRational("RATIONAL_TEXT_SIZE_OR_TYPE")
        original = dict(value)
        try:
            pair = self._parser(dict(original))
        except Exception as error:
            raise InvalidRational("INJECTED_CODEC_REJECTED") from error
        if type(pair) is not tuple or len(pair) != 2:
            raise InvalidRational("CODEC_RETURN_SHAPE")
        a, b = pair
        if (type(a) is not int or type(b) is not int or
                abs(a).bit_length() > INPUT_BITS or b.bit_length() > INPUT_BITS or b <= 0):
            raise InvalidRational("CODEC_RETURN_RANGE_OR_TYPE")
        result = self._make(a, b)
        if (result.numerator != a or result.denominator != b or
                original != {"numerator": str(a), "denominator": str(b)}):
            raise InvalidRational("CODEC_CANONICAL_POSTCONDITION")
        return result

    @classmethod
    def integer(cls, value):
        return cls._make(cls._integer(value, INTERMEDIATE_BITS), 1)

    @classmethod
    def _product(cls, a, b):
        cls._integer(a, INTERMEDIATE_BITS)
        cls._integer(b, INTERMEDIATE_BITS)
        if not a or not b:
            return 0
        # Deliberately conservative: no product is formed above this bound.
        if abs(a).bit_length() + abs(b).bit_length() > INTERMEDIATE_BITS:
            raise RationalResourceLimit("PRODUCT_PRECHECK")
        return cls._integer(a * b, INTERMEDIATE_BITS)

    @classmethod
    def _sum(cls, a, b):
        cls._integer(a, INTERMEDIATE_BITS)
        cls._integer(b, INTERMEDIATE_BITS)
        if not a:
            return b
        if not b:
            return a
        if max(abs(a).bit_length(), abs(b).bit_length()) + 1 > INTERMEDIATE_BITS:
            raise RationalResourceLimit("SUM_PRECHECK")
        return cls._integer(a + b, INTERMEDIATE_BITS)

    @classmethod
    def add(cls, a, b):
        cls._fraction(a)
        cls._fraction(b)
        left = cls._product(a.numerator, b.denominator)
        right = cls._product(b.numerator, a.denominator)
        denominator = cls._product(a.denominator, b.denominator)
        return cls._make(cls._sum(left, right), denominator)

    @classmethod
    def negate(cls, a):
        cls._fraction(a)
        return cls._make(-a.numerator, a.denominator)

    @classmethod
    def subtract(cls, a, b):
        return cls.add(a, cls.negate(b))

    @classmethod
    def multiply(cls, a, b):
        cls._fraction(a)
        cls._fraction(b)
        return cls._make(cls._product(a.numerator, b.numerator),
                         cls._product(a.denominator, b.denominator))

    @classmethod
    def compare(cls, a, b):
        cls._fraction(a)
        cls._fraction(b)
        left = cls._product(a.numerator, b.denominator)
        right = cls._product(b.numerator, a.denominator)
        return (left > right) - (left < right)

    @classmethod
    def encode(cls, value):
        cls._fraction(value)
        return {"numerator": str(value.numerator), "denominator": str(value.denominator)}
