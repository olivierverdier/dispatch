# Dispatch: signal broadcasting in python

This python library is extracted from [django](http://djangoproject.com)'s [dispatch module](http://code.djangoproject.com/browser/django/trunk/django/dispatch).

This very documentation is also adapted from [the django documentation on signals](http://docs.djangoproject.com/en/1.1/topics/signals/).


Overview
========

Signals are useful when two otherwise unrelated pieces of code depend on each other.
The general pattern is that a *receiver* (or listener) may *subscribe* (or listen) to the *signal* of a *sender*.
When the sender sends (or broadcasts) a signal, the receiver is called.

Here is an excerpt from the [PyPubSub](http://pypi.python.org/pypi/PyPubSub/) documentation about the advantages of the signal pattern:

* the sender/listener do not need to import each other;
* a sender doesn't need to know
  * "who" gets the messages,
  * what the listeners will do with the data,
  * or even *if* any listener will get the message data;
* similarly, listeners do not necessarily need to worry about where messages come from.

Lazy Evaluation Pattern
-----------------------

A typical use case is the *lazy evaluation* pattern, very useful whenever any expensive computing is involved.
Imagine that some expensive function `F` depends on one variable `x`.
Since the evaluation of the function is expensive, the value `F(x)` will be cached.

Assume further that `x` is defined in a totally unrelated module.
How to cache the value of `F(x)` so that it is only recomputed when `x` changes?

A naive approach would be for `x` (or the object responsible for it) to explicitly tell the function `F` that `x` has changed.
The drawback is that `x` must know all the functions that depend on it!
It makes the code difficult to reuse, since each time you add a function depending on `x` you will have to change the code responsible for `x`.
This is not acceptable.

This is where signals come to the rescue.
The object responsible for changing `x` just has to send a signal whenever the value of `x` changes.
The function `F` then listens to that signal, and sets its cached value as needing to be recomputed.

The latter approach is very flexible.
It allows for several functions to depend on one variable `x`, without the variable `x` being aware of it.
It also allows for one function to depend on several variables, as long as all those variables send signals when their value changes.


Defining and sending signals
============================


Defining signals
----------------


All signals are `dispatch.Signal` instances.
The `providing_args` is a list of the names of arguments the signal will provide to listeners.

For example:

```python
import dispatch

pizza_done = dispatch.Signal(providing_args=["toppings", "size"])
```

This declares a `pizza_done` signal that will provide receivers with `toppings` and `size` arguments.
Remember that you're allowed to change this list of arguments at any time, so getting the API right on the first try isn't necessary.

Sending signals
---------------

To send a signal, call `Signal.send`.
You must provide the `sender` argument, and may provide as many other keyword arguments as you like.

For example, here's how sending our `pizza_done` signal might look:

```python
class PizzaStore(object):
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self, toppings=toppings, size=size)
        ...
```
        

Listening to signals
====================

To receive a signal, you need to register a *receiver* function that gets called when the signal is sent.
Let's see how this works by registering a signal that gets called after each pizza is finished.
We'll be connecting to the `pizza_done` signal.

Receiver functions
------------------

First, we need to define a receiver function.
A receiver can be any Python function or method:

```python
def my_callback(sender, **kwargs):
    print "Pizza ready!"
```

Notice that the function takes a `sender` argument, along with wildcard keyword arguments (`**kwargs`);
all signal handlers must take these arguments.

Look at the `**kwargs` argument.
All signals send keyword arguments, and may change those keyword arguments at any time.
In the case of `pizza_done`, it's documented as sending two arguments, topping and size, which means we might be tempted to write our signal handling as `my_callback(sender, toppings, size)`.


This would be wrong – in fact, `dispatch` will throw an error if you do so.
That's because at any point arguments could get added to the signal and your receiver must be able to handle those new arguments.

Connecting receiver functions
-----------------------------

Next, we'll need to connect our receiver to the signal:

```python
pizza_done.connect(my_callback)
```

Now, our `my_callback` function will be called each time a pizza is ready.


Connecting to signals sent by specific senders
----------------------------------------------

Some signals get sent many times, but you'll only be interested in receiving a certain subset of those signals.
For example, consider the `pizza_done` signal.
Most of the time, you don't need to know when *any* pizza is ready – just when a pizza from a *specific* pizza store is ready.

In these cases, you can register to receive signals sent only by particular senders.
In the case of the pizza example, the sender will be the pizza store, so you can indicate that you only want
signals sent by one particular kind of pizza store, or one particular pizza store:

```python
class VegetarianPizzaStore(PizzaStore):
    ...

def my_handler(sender, **kwargs):
    ...

pizza_done.connect(my_handler, sender=VegetarianPizzaStore)
```

The `my_handler` function will only be called when a pizza from any `VegetarianPizzaStore` is ready.

Similarly, you might only be interested in pizzas prepared in one specific pizza store:

```python
my_pizza_store = PizzaStore()
    ...

def my_handler(sender, **kwargs):
    ...

pizza_done.connect(my_handler, sender=my_pizza_store)
```

The `my_handler` function will only be called when a pizza from the object `my_pizza_store` is ready.
