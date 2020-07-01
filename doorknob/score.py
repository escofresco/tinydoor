from collections import Counter
from decimal import Decimal
from math import sqrt

__all__ = ("score", )

def score(ratings, weights, scale=100, M=100, P=.5):
    """
    A weighted scoring algorithm. Adapted from https://tinyurl.com/y88kvfth.

    Args:
        ratings: Array of valence ratings which can either be -1, 0, or 1.
        weights: Array of corresponding weights for each score ∈ [0, 1].
        M: A number representing a moderate value.
        P:  ∈ [0, 1]

    Returns:
        A score ∈ [0, 1]
    """
    assert len(ratings) == len(weights)
    hist = Counter(ratings)

    # Number of elements
    n = Decimal(len(ratings))

    # https://tinyurl.com/y2ka4gja
    # (1-confidence/2) quantile of the standard normal distribution
    # where confidence == .95
    z = Decimal(1.96)

    # Observed fraction of positive ratings
    p_hat = Decimal(hist[1]) / n

    # Lower bound of Wilson score confidence interval for a Bernoulli parameter
    return ((p_hat + z * z / (2 * n) - z * Decimal(sqrt(
        (p_hat * (1 - p_hat) + z * z / (4 * n)) / n))) / (1+z*z/n))

    # Quantity importance
    Q = -Decimal(M) / Decimal(1/2).ln()

    # Weighted mean
    p = (sum(Decimal(r+1)*Decimal(w)
             for r,w in zip(ratings, weights)) / n)
    # Normalized mean
    #p = sum(Decimal(num)*Decimal(count) for num, count in hist.items()) / q

    return (Decimal(P) * Decimal(p) +
            Decimal(2) * (1 - Decimal(P)) * (1 - Decimal(-n / Q).exp()))

if __name__ == "__main__":
    ratings = (1,1,1,1,1,1,1,1,5,1,0)
    weights = (.5,.2,.2,.1345,.666666,.93,.5,0,.999999999999999,.7645,.789)
    print(score(ratings, weights))

    ratings = (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    weights = (.5,.2,.2,.1345,.666666,.93,.5,0,.999999999999999,.7645,.789)
    print(score(ratings, weights))

    ratings = (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    weights = (1,1,1,1,1,1,1,1,1,1,1)
    print(score(ratings, weights))

    ratings = (1,)*1000000 + (-1,)*1000000
    weights = (1,)*2000000
    print(score(ratings, weights))

    ratings = (-1,)*1000000
    weights = (1,)*1000000
    print(score(ratings, weights))
