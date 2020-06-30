from decimal import Decimal

__all__ = ("score", )

def score(ratings, weights, scale=100, M=100, P=.5):
    ## adapted from https://tinyurl.com/y88kvfth
    assert len(ratings) == len(weights)

    # Number of ratings or weights
    q = Decimal(len(ratings))

    # Quantity importance
    Q = -Decimal(M) / Decimal(1/2).ln()

    # Weighted mean
    p = (sum(Decimal(r)*Decimal(w)
             for r,w in zip(ratings, weights)) / q)

    return (Decimal(P) * Decimal(p) +
            Decimal(10) * (1 - Decimal(P)) * (1 - Decimal(-q / Q).exp()))

if __name__ == "__main__":
    ratings = (1,1,-1,-1,1,1,1,1,-1,1,-1)
    weights = (.5,.2,.2,.1345,.666666,.93,.5,0,.999999999999999,.7645,.789)
    print(score(ratings, weights))

    ratings = (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    weights = (.5,.2,.2,.1345,.666666,.93,.5,0,.999999999999999,.7645,.789)
    print(score(ratings, weights))

    ratings = (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    weights = (1,1,1,1,1,1,1,1,1,1,1)
    print(score(ratings, weights))
