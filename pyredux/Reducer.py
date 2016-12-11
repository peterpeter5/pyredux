from __future__ import absolute_import, unicode_literals

import collections

from pyredux.ErrorsAndConstants import StoreInitAction
from pyrsistent import pmap


def combine_reducer(reducers):
    combined_initial_state = pmap()

    reducer_names, reducer_funcs = _determine_reducer_names_and_funcs(reducers)

    combined_initial_state = pmap(
        map(
            lambda red_name, red_func: (red_name, _get_initial_reducer_state(red_func)),
            reducer_names, reducer_funcs
        )
    )
    final_reducers = pmap(zip(reducer_names, reducer_funcs))

    def combination(state=combined_initial_state, action=None):
        next_state = state.copy()
        has_changed = False
        for name_of_reducer, _reducer in final_reducers.items():
            old_state = state[name_of_reducer]
            new_state = _reducer(old_state, action)
            has_changed |= new_state is not old_state
            next_state = next_state.set(name_of_reducer, new_state)
        return next_state if has_changed else state

    return combination


def _get_reducer_name_from_func(func):
    return func.__name__


def _determine_reducer_names_and_funcs(reducers):
    if isinstance(reducers, (collections.Mapping,)):
        reducer_names = reducers.keys()
        reducer_funcs = reducers.values()

    elif isinstance(reducers, collections.Iterable):
        reducer_names = map(lambda red: _get_reducer_name_from_func(red), reducers)
        reducer_funcs = reducers
    return reducer_names, reducer_funcs


def _get_initial_reducer_state(reducer_func):
    return reducer_func(action=StoreInitAction())



