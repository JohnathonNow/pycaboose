PyCaboose
=========

[![Build Status](https://github.com/johnathonnow/pycaboose/workflows/Build/badge.svg)](https://github.com/JohnathonNow/pycaboose/actions)
[![PyPI version](https://badge.fury.io/py/pycaboose.svg)](https://badge.fury.io/py/pycaboose)


Idea
----

Existing persistent storage solutions suck because they decouple your code from
the data that it needs to run. Under current solutions you must either use a
local file, a database, or some external service in order to store your data
in between executions of your script. These solutions are bad because with any
local storage you have to remember to copy your data over too when you want
to use your script somewhere else while still retaining the stored data.
External services require internet connections, and those can be unreliable,
which is very bad. Another potential solution is to just have your script
never terminate, thus it would have no need to persist data as it will retain
it in memory. This is obviously stupid.

Enter **PyCaboose**, a Python library for persisting data within the script file
itself.

Usage
-----

Using **PyCaboose** is very easy. Consider the following example:

```python
from pycaboose import Value
a = Value(0)
print(a.value)
a.value += 1
```

The first time you run this script, it will print out `0`. Then, the next time
you run the script, once the `Value` object is instantiated, it will perform a 
lookup for the most recent value, which is 1. So the `print` will instead print
`1` instead of `0`.

How does it do this? Good question.

Mechanism
---------

The secret sauce to **PyCaboose** is its in-script database. When the **pycaboose**
module is imported, it opens your script file and scans it for a special marker
that it places there the first time it is imported. Then, any time a **PyCaboose**
**Value** is changed, it writes the new value to the script. So, using the
above example, after running the script the first time, it will instead look
like this:


```python
from pycaboose import Value
a = Value(0)
print(a.value)
a.value += 1
# pycaboose #
# gANLA0sBhnEALg==
```

Breaking that down, it inserted a comment, `# pycaboose #`, which indicates where
it will be storing data. This must be at the end of the file. Next, there is
another comment, but this time it is more involved. 
There is a bunch of garbage. This garbage is a base64 encoded string. But what
does it encode? Another good question.

The b64 encoded string encodes a pickle. That pickle encodes a tuple
`(line, value)`. The `line` is how we know which variable we are talking about,
which is important if there is more than one **Value** in the script.
(Note this means that at the moment two **Value**s cannot be declared
on the same line. Deal with it.)
In this case, `line` will be `2`, because we stored `a` on line `2`.
The `value` is the stored value of the object, which in this case is `1`
as that is the most recent value of the **Value**.

Now if we were to run the script again, upon instantiating the **Value**,
**PyCaboose** will know that it has stored a value for that **Value** and loads
that rather than using the value the user specified.

For writes, **PyCaboose** truncates the file, removing the line that stored the
old value of the **Value** if it was previously stored. It then writes back
any data it may have removed, and then writes the new data to the end of the
file. In doing so it creates something of a LRU cache where accessing
**Value**s that haven't been accessed in a while is slower than accessing the
**Value** that was most recently modified.

Disclaimer
----------

Please note that this is more or less a joke and not really meant to be used.
Please don't hold me responsible for data that is not persisted, or scripts
that are completely mangled. For any import data you should have backups,
backups of those backups, several GitHub repos containing the data, and the
data should also be stored in DropBox, OneDrive, encoded and uploaded to
YouTube, and should be stored on an insecure mongodb instance running on
a raspberry pi in your closet.
