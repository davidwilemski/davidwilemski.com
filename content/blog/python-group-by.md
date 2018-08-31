Title: group_by in Python
Date: 2018-08-30 9:15:45pm
Author: David Wilemski
Category: blog
Slug: python-group-by
Tags: python, programming
Status: draft

Frequently when processing data, it's useful to slice it by a certain dimension. It can quickly answer all sorts of questions and help 

Some examples of the types of questions it might answer are:
- What are the requests being made to my service, bucketed by source?  (Who is hammering my service?)
- What are the most common errors happening in my logs?
- Are those errors happening at an even rate across machines or are there specific outliers due to some other property?

...and endless others. It's one of the most frequent tools I reach for whether I'm debugging, refactoring, designing a new feature, or architecting a new system. Being able to look at the same data from multiple angles is invaluable. Programmers aggregate data like this all the time in [database queries](https://dev.mysql.com/doc/refman/5.5/en/group-by-modifiers.html) and [on the command line](https://linux.die.net/man/1/uniq).

An infrequently mentioned function called `groupby` in the `itertools` module does just that for iterables in Python. One frustration with the standard library's particular implementation that might not be obvious is that the data likely needs to be sorted first. Quoting [the docs](https://docs.python.org/3.7/library/itertools.html#itertools.groupby):

> The operation of groupby() is similar to the uniq filter in Unix. It generates a break or new group every time the value of the key function changes (which is why it is usually necessary to have sorted the data using the same key function). That behavior differs from SQL’s GROUP BY which aggregates common elements regardless of their input order.

This isn't always convenient and doesn't seem like it should be required in most cases. Fortunately, with the help of `collections.defaultdict` we can build a grouping function that doesn't have this requirement:

```python
import collections

def group_by(iterable, key_fn):
    """
    >>> def is_odd(num):
    ...     return num % 2 != 0
    ...
    >>> group_by(range(10), is_odd)
    defaultdict(<class 'list'>, {False: [0, 2, 4, 6, 8], True: [1, 3, 5, 7, 9]})
    """
    result = collections.defaultdict(list)
    for item in iterable:
        result[key_fn(item)].append(item)
    return result
```

The primary tradeoff of this version when compared to the standard library is that the input iterable has to be finite. The benefit of being able to assume pre-sorted data is that you can build an iterator over intermediate results, by each key type. Most often I already have the complete set of data so this isn't a concern for me but it is a consideration.

This isn't always the tool you want. In particular, your datastore is probably faster at grouping things before returning results than the Python VM is. However, data isn't always already in a datastore - it can also come from files, input streams, the network, whatever. Go forth and group things!
