# PyRedux
[![Build Status](https://travis-ci.org/peterpeter5/pyredux.svg?branch=master)](https://travis-ci.org/peterpeter5/pyredux)

This is a port of the popular library [redux](https://github.com/reactjs/redux) to pyhton.

This library is a pythonic implementation
of the original javascript-implementation with full-api support.


This package is currently compatible with python2.7 and python >= 3.5.
(At least tested for these versions)

## Dependencies
- pyrsistent: persistent immutable data-structure
- singledispatch: for python2 its a backport, for python3 its build-in


## Documentation

For a very good and detailed description how to use redux, please refer to the
[javascript-documentation](http://redux.js.org/)

Here i will describe the api and more importantly the changes I made comparing to
 the javascript-api

## Store

To create a Store just call the ```create_store``` function:

```python
from pyredux import create_store

store = create_store(reducer)
```

This will give you a fully initialized store-object to work with. This
method is nothing more than a simple factory- / builder-method to
initialize a store.

The Store-api is a little different to the js-api:

    1. To retrieve the actual state instead of a getter a property is used: *actual_state = store.state*
    2. unsubscribe is done via store-method

The state of the store is safed in an immutable [pmap](http://pyrsistent.readthedocs.io/en/latest/api.html#pyrsistent.pmap)
Therefor you can not mutably change it in the reducer and you will
always have to return ```state.update({...})``` from your reducer. The second constraint
is that you will always have to deal with an immutable dict as the current-state, even though
you would have just needed a list or a variable in your current reducer!
On the other hand you don't have to worry about immutability your self.

Keep in mind that although the state-object it self is immutable, you can
store mutable data in it. This will lead to unwanted behaviour as i will
only call the listeners when ```old_state is not new_state```. So if you
will only mutably change your data, than your listeners will never be called.

For further information how to use pyrsitent please refer to the
[documentation](http://pyrsistent.readthedocs.io/en/latest/index.html) and
the examples in their [examples-section](http://pyrsistent.readthedocs.io/en/latest/intro.html#examples)


## Reducers

A reducer is named after the function that gets called from the ```reduce``` function.
One of the key-concepts of redux is, that the current state gets computed in the
following manner:

```python
new_state = reduce(reducer_func, [initial_state, action1, action2, ..., actionN])
```

For performance reasons the old state is saved and every time a
new Action is dispatched only the one function-call is necessary to
calculate the new state. In pseudo-code:
```
state [N] = reduce(reducer_func, [state[N-1], action])
```

Because the state is safed it's essential that updates to the state
will be applied in an immutable manner.

Although it's more or less a standard state-reducer-pattern
the signature of the reducer for this library is changed!
To write your own reducer-function the following signature has to provided:

```python

def my_custom_reducer(action, state=pmap({}):
    return state
```

Whereas the "normal" reducer signature would be: ``` reducer(state, action)```

The default-value of ```state``` is the initial-state of your reducer, which **has**
to be provided by any reducer.
This design-choice was made for two reasons:

### Reason 1. A more pythonic function-signature

A more pythonic function - signature, as it is not allowed in pyhton
to have
positional arguments after named arguments. So with the traditional
signature you would have to write something like this:

```python
# NOT the function-signature to use with pyredux!!!!
def my_custom_reducer(state=pmap({}), action=None):
    return state
```

This does not look nice, and theoratically you would have to handle
the case where an action was not provided (maybe be some middleware) and it is
actually ```None```.

### Reason 2. A more elegant way of handling actions by the reducers

 Because of the lack of a case-statement or an comprehensive pattern-matching functionality,
 writing a reducer that handles more than one action would result in a long
 chained ```if-elif-else``` statement. Instead of this, the python-functionality of
 [singledispatch](https://www.python.org/dev/peps/pep-0443/) can be used.
 Singledispatch works only on the first argument of a function, but results in
 a very cool / clean / pythonic way of writing reducers for different actions:

 ```python
 from pyredux import default_reducer


@default_reducer
def my_reducer(action, state=pmap({"static": True})):
    return state

@my_reducer.register(ActionA)
def _(action, state):
    print("received action of type 'ActionA'")
    return state
 ```

The decorator ```@default_reducer``` is just another name for ```@singledispatch```
By using this facility your default case (actions your reducer does not care about)
can always look like the one provided in this example (just return the state). For every
action not registered before, the function decorated with ``` @default_reducer ``` will
automatically been called.

Every action action you want to process with this reducer, must be registered
and can now be processed in a function strictly responsible for that action-type.
Even more actions (which are namedtuples, more on this later in this guide)
can have "subtypes":

```python
@default_reducer
def my_reducer(action, state=pmap({"static": True})):
    return state

@my_reducer.register(ActionA)
def _(action, state):
    print("received action of type 'ActionA'")
    return state

@my_reducer.register(FancyAction)
def _(action, state):
    if action.type == "fancy_1":
        print("Received action of type 'FancyAction' with a fanciness of 1")
    elif action.type == "fancy_2":
        print("Received an even more fancy action")
    else:
        print("Too fancy for me")

    return state
 ```

 This way the action-handling becomes a less error-pone task and you get
 a way of processing actions with a "subtype" without having to care
 about **nested** long ```if-elif-else``` structures

### Combining reducers
As your application will grow there is a point where you don't want to
handle all actions in one reducer. So it's time to split them up into several
reducers and provide a combined reducer to the store.
To combine reducers the function ```combine_reducer``` can be used.

```python
def a_reducer(action, state):
    return state

def b_reducer(action, state):
    return state

store = create_store(combine_reducer([a_reducer, b_reducer]))

```
Note than when splitting up your reducers into many functions your
code becomes better structured and more readable, but each reducer can now only access
it's own "subtree" of the state!

Now your state will roughly have this shape:

```python
print(store.state)
 >>> {"a_reducer": ..., "b_reducer": ...}
```
If you provide your functions via list or tuple to the function ```combine_reducer```,
your "state-dict" will have the function-names as keys.
Instead of splitting-up the state tree by the function-names
you can use a dict that provides the key for the state and the
corresponding function:
```python
store = create_store(combine_reducer(
            {"a": a_reducer, "b": b_reducer})
)
assert store.state == pmap({"a": ..., "b": ...})
```
For a combined reducer, every "subreducer" will receive every
action dispatched, but only their "own" state-subtree.

## Actions

### TL;DR
The function ``` create_action_type``` creates a namedtuple with with the attributes:
``` type``` and ``` payload```. During creation, the ``` type``` attribute
will get the name of the class as default value and the default value of
 ``` payload``` will be ``` None```. When you instantiate
your custom-action-type you can override both attributes, whereas the
type of the class will stay the same.

As a convenience-function ```create_typed_action_creator ``` is provided.
The function returns the action-type for registering at the reducer
and a builder-function which can be used in the following way:

```python

ActionBaseType, basic_action_creator = create_typed_action_creator("ActionA")
a_action = basic_action_creator()
c_action = basic_action_creator("payload_c", "myCustomSubType")
assert type(a_action) == type(c_action)
assert c_action.type == "myCustomSubType" and c_action.payload == "payload_c"
```

By that ,the application is not bound to a certain type, but has just
to handle a function call. That should increase loose coupling.

### Action-Type

Actions can be dispatched through the store and are transmitted
to the (combined-)reducer. To make the dispatch mechanism work
actions can't just be a dictionary. Therefor namedtuples are used.
To create your own Action-type the function ```create_action_type```
can be used:

```python
CustomActionType = create_action_type("Custom")
action = CustomActionType()
assert action.type == "Custom"
assert isinstance(action, CustomActionType)
```

The argument of ```create_action_type``` determines the type
of the named tuple:

```python
CustomActionType = create_action_type("Custom")
str(CustomActionType)
>>> "<class 'pyredux.Actions.Custom'>"
str(CustomActionType().type)
>>> "Custom"
```
If during the instantiation of ```CustomActionType ``` no subtype
is provided than the attribute ```type``` will be set to be the same as
the class:

```python
CustomActionType = create_action_type("Custom")
str(CustomActionType)
>>> "<class 'pyredux.Actions.Custom'>"

action = CustomActionType(type="something_different")
action.type
>>> "something_different"

type(action)
>>> "<class 'pyredux.Actions.Custom'>"

```
An action can have a payload:

```python
CustomActionType = create_action_type("Custom")
action = CustomActionType("my super payload")
print(action.payload)
>>> "my super payload"
```

### Typed Action creator

Normally you wont tie your application to certain Action-types,
because it would couple your business-logic to a certain signal.
That decreases portability. Instead you can use the function:
``` create_typed_action_creator ``` to create a ActionType and
a corresponding creator-function.
```python
CustomActionType, creator_func =  create_typed_action_creator("Siganl")

@default_reducer()
def signal(action, state=pmap({})):
    return state

@signal.register(CustomActionType)
def _(action, state):
    ...  # Do somthing
    return new_state

class Application(object):
    def do_something(self):
        action = creator_func("my payload", "my_sub_type")
        store.dispatch(action)

...
```

This is similar to the Factory-Pattern. As another example here how you
can compose the creator function with the ``` store.dispatch ```
function to create "send my action right away function".

```python
from pyredux.utils import compose


CustomActionType, creator_func =  create_typed_action_creator("Signal")
send_my_stuff = compose(store.dispatch, creator_func)

class Application(object):

    def on_click():
        send_my_stuff("was clicked")
```

## Middleware

As you should not do anything with side-effects from inside your reducer,
a good place encapsulate all these behaviour of your application is in
the middleware. A custom middleware can be applied via ```apply_middleware```:

```
from pyredux import create_store, apply_middleware

store = create_store(
            reducer,
            enhancer=apply_middleware(middleware_b, middleware_a)
        )
```

This function-call will automatically wrap the the ```store.dispatch``` function,
so that every action travels through the middleware-chain before
reaching your reducer. A middleware-function has the following signature:

```python
def middleware_a(store):
    def _next_wrapper(next_middleware):
        def _middleware(action):

            ...  # Do something with or wihtout side-effects here


            return next_middleware(action)
        return _middleware
    return _next_wrapper

```

or as a short-hand with nicer syntax:

```python

from pyredux import middleware

@middleware
def middleware_decorated(store, next_middleware, action):
    ...  # Do somthing here

    return next_middleware(action)

```

For more detailed information about the redux-middleware-concept
please refer to the [reduxjs-documentation](http://redux.js.org/docs/advanced/Middleware.html)
