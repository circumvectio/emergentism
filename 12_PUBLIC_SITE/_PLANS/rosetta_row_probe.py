"""Synthetic probe of partial G7 signatures, not a world/action classifier.

Domain: two labelled bearers, two separately ordered factors per bearer.
Frames in this probe use SELF as their explicitly selected scope. Comparisons
are supplied inputs, not inferred measurements. No arithmetic on factor codes.
"""
from itertools import product, permutations

FIELDS = ('self.phi', 'self.v', 'other.phi', 'other.v')
RULES = {
    'kali_take_phi': {'self.phi':'up', 'other.v':'down'},
    'kali_take_v': {'self.v':'up', 'other.phi':'down'},
    'krishna_give_v': {'self.phi':'down', 'other.v':'up'},
    'arjuna_give_phi': {'self.v':'down', 'other.phi':'up'},
    'brahma_create': {'self.phi':'up', 'self.v':'up'},
    'shiva_dissolve': {'self.phi':'down', 'self.v':'down'},
    'vishnu_preserve': {'self.phi':'same', 'self.v':'same'},
}


def matches(comparisons):
    if set(comparisons) != set(FIELDS):
        raise ValueError('Exact bearer/factor fields required')
    if any(v not in {'up','down','same','unknown','incomparable'} for v in comparisons.values()):
        raise ValueError('Order relation required, not a numeric delta')
    return sorted(key for key, clauses in RULES.items()
                  if all(comparisons[field] == direction for field,direction in clauses.items()))


def census():
    histogram = {'unmatched':0, 'single_match':0, 'multiple_matches':0}
    for signs in product(('down','same','up'), repeat=4):
        count = len(matches(dict(zip(FIELDS, signs))))
        histogram['unmatched' if count==0 else 'single_match' if count==1 else 'multiple_matches'] += 1
    return {'domain':'two bearers × two factors, total order comparisons; F3 scope=self',
            'comparison_records':3**4, **histogram,
            'label_orders_preserving_same_predicates':sum(1 for _ in permutations(RULES)),
            'limits': ['not all feasible actions', 'strict partial signatures before any degenerate quotient',
                       'permutation count assumes no additional order relation', 'no universal impossibility conclusion'],
            'result_type':'synthetic local probe, no empirical result'}


if __name__ == '__main__':
    import json
    print(json.dumps(census(), indent=2))
