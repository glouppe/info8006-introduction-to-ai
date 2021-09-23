# Python tutorial

Programming projects will be done in Python 3.9.
In this tutorial, you will install Python and learn its basics.

Credits: This tutorial is strongly based on [CS188 project 0](https://inst.eecs.berkeley.edu/~cs188/su19/project0/) from UC Berkeley.

## Table of contents

- [Tools](#tools)
    - [Python](#python)
    - [Unix & OS X basics](#unix--os-x-basics)
    - [Windows basics](#windows-basics)
    - [Python environment management](#python-environment-management)
      	- [Creating a Conda Environment](#creating-a-conda-environment)
      	- [Entering the Environment](#entering-the-environment)
      	- [Leaving the Environment](#leaving-the-environment)
- [Python Basics](#python-basics)
    - [Required Files](#required-files)
    - [Introduction](#introduction)
    - [Invoking the Interpreter](#invoking-the-interpreter)
    - [Operators](#operators)
    - [Strings](#strings)
    - [Exercise: Dir and Help](#exercise-dir-and-help)
    - [Built-in Data Structures](#built-in-data-structures)
      	- [Lists](#lists)
      	- [Exercise: Lists](#exercise-lists)
      	- [Tuples](#tuples)
      	- [Sets](#sets)
      	- [Dictionaries](#dictionaries)
      	- [Exercise: Dictionaries](#exercise-dictionaries)
    - [Writing Scripts](#writing-scripts)
    - [Exercise: List Comprehensions](#exercise-list-comprehensions)
    - [Beware of Indendation!](#beware-of-indendation)
    - [Tabs vs Spaces](#tabs-vs-spaces)
    - [Writing Functions](#writing-functions)
    - [Advanced Exercise](#advanced-exercise)
    - [Object Basics](#object-basics)
      	- [Defining Classes](#defining-classes)
      	- [Using Objects](#using-objects)
    - [Static vs Instance Variables](#static-vs-instance-variables)
    - [More Python Tips and Tricks](#more-python-tips-and-tricks)
    - [Troubleshooting](#troubleshooting)
- [Exercises](#exercises)
    - [Question 1: Addition](#question-1-addition)
    - [Question 2: buyLotsOfFruit function](#question-2-buylotsoffruit-function)
    - [Question 3: shopSmart function](#question-3-shopsmart-function)
- [Going further](#going-further)

## Tools

In order to work with Python, we encourage you to use a text editor and a terminal (instead of an IDE). Make sure to read the entire [Tools](#tools) section before starting your installation.

On Unix and OS X, you can use the basic terminal while on Windows, you will use the *Anaconda prompt* (see further).

There are plenty of text editors that can be used but [Atom](https://atom.io/) or [Sublime Text](https://www.sublimetext.com/) are good candidates.

Also, there exist many IDEs such as [Spyder](https://www.spyder-ide.org/) or [PyCharm](https://www.jetbrains.com/pycharm/) that could be used **CAREFULLY**.

### Python
We recommend you to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html). It allows you to manage many environments, with distinct Python versions and dependencies.

For Windows users, Miniconda comes with the *Anaconda prompt* that will be used as a terminal to execute Python code.

### Unix & OS X basics
When you open a terminal window, you’re placed at a command prompt:

```console
username@computername:~$
```

The prompt shows your username, the host you are logged onto, and your current location in the directory structure (your path). The tilde character is shorthand for your home directory. Note your prompt may look slightly different. To make a directory, use the `mkdir` command. Use `cd` to change to that directory:

```console
username@computername:~$ mkdir foo
username@computername:~$ cd foo
username@computername:foo$
```

Use `ls` to see a listing of the contents of a directory, and `touch` to create an empty file:

```console
username@computername:foo$ ls
username@computername:foo$ touch hello
username@computername:foo$ ls
hello
username@computername:foo$ cd ..
username@computername:~$
```

Download **[tutorial_code.zip](https://github.com/glouppe/info8006-introduction-to-ai/raw/master/python-tutorial/tutorial_code.zip)** into a directory and change your terminal to that directory (note: the zip file's name may be slightly different when you download it). Use `unzip` to extract the contents of the zip file:

```console
username@computername:python-tutorial$ ls
tutorial_code.zip
username@computername:python-tutorial$ unzip tutorial_code.zip
username@computername:python-tutorial$ ls
tutorial_code		tutorial_code.zip
username@computername:python-tutorial$ cd tutorial_code
username@computername:tutorial_code$ ls
exercises python_basics
username@computername:tutorial_code$ cd python_basics/
username@computername:python_basics$ ls
foreach.py
listcomp.py
mean.py
shop.py
helloWorld.py
listcomp2.py
quickSort.py
shopTest.py
```

Some other useful Unix commands:

- `cp` copies a file or files
- `rm` removes (deletes) a file
- `mv` moves a file (i.e., cut/paste instead of copy/paste)
- `man` displays documentation for a command
- `pwd` prints your current path
- Press "Ctrl + c" to kill a running process
- Append `&` to a command to run it in the background
- `fg` brings a program running in the background to the foreground

### Windows basics
Since you are on Windows, you will use the *Anaconda prompt* that is installed with Miniconda. In this terminal, the commands are different from those of UNIX.

Download **[tutorial_code.zip](https://github.com/glouppe/info8006-introduction-to-ai/raw/master/python-tutorial/tutorial_code.zip)** into a directory of your choice, unzip it using your file explorer and change the current directory of the *Anaconda prompt* to this new directory.

You can find several commands to manipulate files and the current directory of your prompt in the following:

- If you are not on the desired disk, you just have to type its name in the prompt:

```console
C:\Users>D:
D:\>
```

- `md` to create a new directory
- `cd` to change directory
- `dir` to see a listing of the contents of a directory
- `copy` to copy a file or files
- `del` to remove (delete) a file
- `move` to move a file
- `echo %cd%` prints your current path
- To create an empty file, prefer the file explorer

### Python environment management
In the following, the commands are the same either you are working on Anaconda prompt or a UNIX terminal.

#### Creating a Conda Environment
The command for creating a conda environment with Python 3.9 is:

```console
conda create --name <env-name> python=3.9
```

We name our environment info8006 with the following command.

```console
username@computername:python_basics$ conda create --name info8006 python=3.9
```

Enter y to confirm the installation of any missing packages.

#### Entering the Environment
We do the following to enter the conda environment that we just created and to check the python version.
Note that the Python version within the environment is 3.9, just what we want.

```console
username@computername:python_basics$ conda activate info8006
(info8006) username@computername:python_basics$ python -V
Python 3.9.7 :: Anaconda, Inc.
```

Note: the tag (<env-name>) shows you the name of the conda environment that is active. In our case, we have (info8006), as what we’d expect.

#### Leaving the Environment
Leaving the environment is just as easy.
```console
(info8006) username@computername:python_basics$ conda deactivate
username@computername:python_basics$ python -V
Python 2.7.10
```

Our Python version has now returned to whatever the system default is!

## Python Basics
### Required Files
Following the terminal basics of your OS, you should have downloaded a zip file, extracted the content of this archive in a chosen directory and the current directory of your terminal should contains those files.

### Introduction

The programming assignments of this course will be written in Python, an interpreted, object-oriented language that shares some features with both Java and Scheme. This tutorial will walk you through the primary syntactic constructions in Python, using short examples.

We encourage you to try to type by yourself the python code of this tutorial. Check that your code produces the same results.

You may find the [Troubleshooting](#troubleshooting) section helpful if you run into problems. It contains a list of the frequent problems previous students have encountered when following this tutorial.

### Invoking the Interpreter

Python can be run in one of two modes. It can either be used interactively, via an interpeter, or it can be called from the command line to execute a script. We will first use the Python interpreter interactively.

You invoke the interpreter using the command `python` at the command prompt.

```console
(info8006) username@computername:python_basics$ python
Python 3.9.7 |Anaconda, Inc.| (default, Jul 30 2019, 13:42:17)
[GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### Operators

The Python interpreter can be used to evaluate expressions, for example simple arithmetic expressions. If you enter such expressions at the prompt (`>>>`) they will be evaluated and the result will be returned on the next line.

```python
>>> 1 + 1
2
>>> 2 * 3
6
```


Boolean operators also exist in Python to manipulate the primitive `True` and `False` values.

```python
>>> 1 == 0
False
>>> not (1 == 0)
True
>>> (2 == 2) and (2 == 3)
False
>>> (2 == 2) or (2 == 3)
True
```

### Strings

Like Java, Python has a built in string type. The `+` operator is overloaded to do string concatenation on string values.

```python
>>> 'artificial' + "intelligence"
'artificialintelligence'
```
There are many built-in methods which allow you to manipulate strings.

```python
>>> 'artificial'.upper()
'ARTIFICIAL'
>>> 'HELP'.lower()
'help'
>>> len('Help')
4
```
Notice that we can use either single quotes `' '` or double quotes `" "` to surround string. This allows for easy nesting of strings.

We can also store expressions into variables.

```python
>>> s = 'hello world'
>>> print(s)
hello world
>>> s.upper()
'HELLO WORLD'
>>> len(s.upper())
11
>>> num = 8.0
>>> num += 2.5
>>> print(num)
10.5
```

In Python, you do not have to declare a variable before assigning it a value.

### Exercise: Dir and Help

Learn about the methods Python provides for strings. To see what methods Python provides for a datatype, use the `dir` and `help` commands:

```python
>>> s = 'abc'

>>> dir(s)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__str__', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'replace', 'rfind', 'rindex', 'rjust', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

>>> help(s.find)
Help on built-in function find:

find(...) method of builtins.str instance
    S.find(sub[, start[, end]]) -> int

    Return the lowest index in S where substring sub is found,
    such that sub is contained within S[start:end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.


>>> s.find('b')
1
```

Try out some of the string functions listed in `dir` (ignore those with underscores '_' around the method name).

### Built-in Data Structures

Python comes equipped with some useful built-in data structures, broadly similar to Java’s collections package.

#### Lists

Lists store a sequence of mutable items:

```python
>>> fruits = ['apple', 'orange', 'pear', 'banana']
>>> fruits[0]
'apple'
```

We can use the `+` operator to do list concatenation:

```python
>>> otherFruits = ['kiwi', 'strawberry']
>>> fruits + otherFruits
>>> ['apple', 'orange', 'pear', 'banana', 'kiwi', 'strawberry']
```

Python also allows negative-indexing from the back of the list. For instance, `fruits[-1]` will access the last element `'banana'`:

```python
>>> fruits[-2]
'pear'
>>> fruits.pop()
'banana'
>>> fruits
['apple', 'orange', 'pear']
>>> fruits.append('grapefruit')
>>> fruits
['apple', 'orange', 'pear', 'grapefruit']
>>> fruits[-1] = 'pineapple'
>>> fruits
['apple', 'orange', 'pear', 'pineapple']
```
We can also index multiple adjacent elements using the slice operator. For instance, `fruits[1:3]`, returns a list containing the elements at position 1 and 2. In general `fruits[start:stop]` will get the elements in `start, start+1, ..., stop-1`. We can also do `fruits[start:]` which returns all elements starting from the `start` index. Also `fruits[:end]` will return all elements before the element at position `end`:

```python
>>> fruits[0:2]
['apple', 'orange']
>>> fruits[:3]
['apple', 'orange', 'pear']
>>> fruits[2:]
['pear', 'pineapple']
>>> len(fruits)
4
```

The items stored in lists can be any Python data type. So for instance we can have lists of lists:

```python
>>> lstOfLsts = [['a', 'b', 'c'], [1, 2, 3], ['one', 'two', 'three']]
>>> lstOfLsts[1][2]
3
>>> lstOfLsts[0].pop()
'c'
>>> lstOfLsts
[['a', 'b'], [1, 2, 3], ['one', 'two', 'three']]
```

#### Exercise: Lists

Play with some of the list functions. You can find the methods you can call on an object via the dir and get information about them via the help command:

```python
>>> dir(list)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__',
'__delslice__', '__doc__', '__eq__', '__ge__', '__getattribute__',
'__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__',
'__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__',
'__rmul__', '__setattr__', '__setitem__', '__setslice__', '__str__',
'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse',
'sort']
```
```python
>>> help(list.reverse)
          Help on built-in function reverse:

          reverse(...)
          L.reverse() -- reverse \*IN PLACE\*

```

```python
>>> lst = ['a', 'b', 'c']
>>> lst.reverse()
>>> ['c', 'b', 'a']

```

Note: Ignore functions with underscores "_" around the names; these are private helper methods. Press 'q' to back out of a help screen.

#### Tuples

A data structure similar to the list is the tuple, which is like a list except that it is immutable once it is created (i.e. you cannot change its content once created). Note that tuples are surrounded with parentheses while lists have square brackets.

```python
>>> pair = (3, 5)
>>> pair[0]
3
>>> x, y = pair
>>> x
3
>>> y
5
>>> pair[1] = 6
TypeError: object does not support item assignment
```

The attempt to modify an immutable structure raised an exception. Exceptions indicate errors: index out of bounds errors, type errors, and so on will all report exceptions in this way.

#### Sets

A set is another data structure that serves as an unordered list with no duplicate items. Below, we show how to create a set:

```python
>>> shapes = ['circle', 'square', 'triangle', 'circle']
>>> setOfShapes = set(shapes)
```

Another way of creating a set is shown below:

`>>> setOfShapes = {‘circle’, ‘square’, ‘triangle’, ‘circle’}`

Next, we show how to add things to the set, test if an item is in the set, and perform common set operations (difference, intersection, union):

```python
>>> setOfShapes
set(['circle', 'square', 'triangle'])
>>> setOfShapes.add('polygon')
>>> setOfShapes
set(['circle', 'square', 'triangle', 'polygon'])
>>> 'circle' in setOfShapes
True
>>> 'rhombus' in setOfShapes
False
>>> favoriteShapes = ['circle', 'triangle', 'hexagon']
>>> setOfFavoriteShapes = set(favoriteShapes)
>>> setOfShapes - setOfFavoriteShapes
set(['square', 'polygon'])
>>> setOfShapes & setOfFavoriteShapes
set(['circle', 'triangle'])
>>> setOfShapes | setOfFavoriteShapes
set(['circle', 'square', 'triangle', 'polygon', 'hexagon'])
```

**Note that the objects in the set are unordered; you cannot assume that their traversal or print order will be the same across machines!**

#### Dictionaries

The last built-in data structure is the dictionary which stores a map from one type of object (the key) to another (the value). The key must be an immutable type (string, number, or tuple) and therefore, it cannot be a list for example. The value can be any Python data type.

Note: In the example below, the printed order of the keys returned by Python could be different than shown below. The reason is that unlike lists which have a fixed ordering, a dictionary is simply a hash table for which there is no fixed ordering of the keys (like HashMaps in Java). The order of the keys depends on how exactly the hashing algorithm maps keys to buckets, and will usually seem arbitrary. Your code should not rely on key ordering, and you should not be surprised if even a small modification to how your code uses a dictionary results in a new key ordering.

```python
>>> studentIds = {'knuth': 42.0, 'turing': 56.0, 'nash': 92.0}
>>> studentIds['turing']
56.0
>>> studentIds['nash'] = 'ninety-two'
>>> studentIds
{'knuth': 42.0, 'turing': 56.0, 'nash': 'ninety-two'}
>>> del studentIds['knuth']
>>> studentIds
{'turing': 56.0, 'nash': 'ninety-two'}
>>> studentIds['knuth'] = [42.0, 'forty-two']
>>> studentIds
{'knuth': [42.0, 'forty-two'], 'turing': 56.0, 'nash': 'ninety-two'}
>>> studentIds.keys()
['knuth', 'turing', 'nash']
>>> studentIds.values()
[[42.0, 'forty-two'], 56.0, 'ninety-two']
>>> studentIds.items()
[('knuth', [42.0, 'forty-two']), ('turing',56.0), ('nash', 'ninety-two')]
>>> len(studentIds)
3
```

As with nested lists, you can also create dictionaries of dictionaries.

#### Exercise: Dictionaries

Use `dir` and `help` to learn about the functions you can call on dictionaries.

### Writing Scripts

Now that you’ve got a handle on using Python interactively, let’s write a simple Python script that demonstrates Python’s `for` loop. Open the file called `foreach.py`, which should contain the following code:

```python
# This is what a comment looks like
fruits = ['apples', 'oranges', 'pears', 'bananas']
for fruit in fruits:
    print(fruit + ' for sale')

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}
for fruit, price in fruitPrices.items():
    if price < 2.00:
        print('%s cost %f a pound' % (fruit, price))
    else:
        print(fruit + ' are too expensive!')
```

In the command line, use the following command in the directory containing `foreach.py`:

```console
(info8006) username@computername:python_basics$ python foreach.py
apples for sale
oranges for sale
pears for sale
bananas for sale
apples are too expensive!
oranges cost 1.500000 a pound
pears cost 1.750000 a pound
```

Remember that the print statements listing the costs may be in a different order on your screen than in this tutorial; it comes from the fact that we are looping over dictionary keys, which are unordered. To learn more about control structures (e.g., `if` and `else`) in Python, check out the official [Python tutorial section on this topic](https://docs.python.org/3.6/tutorial/).

If you like functional programming you might also like map and filter:

```python
>>> list(map(lambda x: x * x, [1, 2, 3]))
[1, 4, 9]
>>> list(filter(lambda x: x > 3, [1, 2, 3, 4, 5, 4, 3, 2, 1]))
[4, 5, 4]
```

The next snippet of code demonstrates Python’s list comprehension construction:

```python
nums = [1, 2, 3, 4, 5, 6]
plusOneNums = [x + 1 for x in nums]
oddNums = [x for x in nums if x % 2 == 1]
print(oddNums)
oddNumsPlusOne = [x + 1 for x in nums if x % 2 == 1]
print(oddNumsPlusOne)
```

This code is in a file called `listcomp.py`, which you can run:

```console
(info8006) username@computername:python_basics$ python listcomp.py
[1, 3, 5]
[2, 4, 6]
```

### Exercise: List comprehensions

Write a list comprehension which, from a list, generates a lowercased version of each string which length is greater than 5. You can find the solution in `listcomp2.py`.

### Beware of Indendation!

Unlike many other languages, Python uses the indentation in the source code for interpretation. For instance, the following script:

```python
if 0 == 1:
    print('We are in a world of arithmetic pain')
print('Thank you for playing')
```

will output: Thank you for playing

But if we had written the script as

```python
if 0 == 1:
    print('We are in a world of arithmetic pain')
    print('Thank you for playing')
```

there would be no output. The moral of the story: **be careful how you indent!** It’s best to use four spaces for indentation – that’s what the course code uses.

### Tabs vs Spaces

Because Python uses indentation for code evaluation, it needs to keep track of the level of indentation across code blocks. This means that if your Python file switches from using tabs as indentation to spaces as indentation, the Python interpreter will not be able to resolve the ambiguity of the indentation level and throw an exception. Even though the code can be lined up visually in your text editor, Python “sees” a change in indentation and most likely will throw an exception (or rarely, produce unexpected behavior).

This most commonly happens when opening up a Python file that uses an indentation scheme that is opposite from what your text editor uses (e.g., your text editor uses spaces and the file uses tabs). When you write new lines in a code block, there will be a mix of tabs and spaces, even though the whitespace is aligned. For a longer discussion on tabs vs spaces, see [this](https://stackoverflow.com/questions/119562/tabs-versus-spaces-in-python-programming) discussion on StackOverflow.

### Writing Functions

As in Java, in Python you can define your own functions:

```python
fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}

def buyFruit(fruit, numPounds):
    if fruit not in fruitPrices:
        print("Sorry we don't have %s" % (fruit))
    else:
        cost = fruitPrices[fruit] * numPounds
        print("That'll be %f please" % (cost))

# Main Function
if __name__ == '__main__':
    buyFruit('apples', 2.4)
    buyFruit('coconuts', 2)

```
Rather than having a `main` function as in Java, the `__name__ == '__main__'` check is used to delimit expressions which are executed when the file is called as a script from the command line. The code after the main check is thus the same sort of code you would put in a `main` function in Java or C.

Save this script as fruit.py and run it:

```console
(info8006) username@computername:python_basics$ python fruit.py
That'll be 4.800000 please
Sorry we don't have coconuts
```

#### Advanced exercises

- Write a `mean` function in Python. You can find two solutions in `mean.py`.
- Write a `quickSort` function in Python using list comprehensions. Use the first element as the pivot. You can find a solution in `quickSort.py`.

### Object Basics

Although this is not a class in object-oriented programming, you will have to use some objects in the programming projects, and so it is worth covering the basics of objects in Python. An object encapsulates data and provides functions for interacting with that data.

#### Defining Classes

Here’s an example of defining a class named `FruitShop`:

```python
class FruitShop:

    def __init__(self, name, fruitPrices):
        """
            name: Name of the fruit shop

            fruitPrices: Dictionary with keys as fruit
            strings and prices for values e.g.
            {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}
        """
        self.fruitPrices = fruitPrices
        self.name = name
        print('Welcome to %s fruit shop' % (name))

    def getCostPerPound(self, fruit):
        """
            fruit: Fruit string
        Returns cost of 'fruit', assuming 'fruit'
        is in our inventory or None otherwise
        """
        if fruit not in self.fruitPrices:
            return None
        return self.fruitPrices[fruit]

    def getPriceOfOrder(self, orderList):
        """
            orderList: List of (fruit, numPounds) tuples

        Returns cost of orderList, only including the values of
        fruits that this fruit shop has.
        """
        totalCost = 0.0
        for fruit, numPounds in orderList:
            costPerPound = self.getCostPerPound(fruit)
            if costPerPound != None:
                totalCost += numPounds * costPerPound
        return totalCost

    def getName(self):
        return self.name
```

The `FruitShop` class has some data, the name of the shop and the prices per pound of some fruit, and it provides functions, or methods, on this data. What advantage is there to wrapping this data in a class?

1. Encapsulating the data prevents it from being altered or used inappropriately,
  2. The abstraction that objects provide make it easier to write general-purpose code.

#### Using Objects

So how do we make an object and use it? Make sure you have the `FruitShop` implementation in `shop.py`. We then import the code from this file (making it accessible to other scripts) using `import shop`, since `shop.py` is the name of the file. Then, we can create `FruitShop` objects as follows:

```python
import shop

shopName = 'the Berkeley Bowl'
fruitPrices = {'apples': 1.00, 'oranges': 1.50, 'pears': 1.75}
berkeleyShop = shop.FruitShop(shopName, fruitPrices)
applePrice = berkeleyShop.getCostPerPound('apples')
print(applePrice)
print('Apples cost $%.2f at %s.' % (applePrice, shopName))

otherName = 'the Stanford Mall'
otherFruitPrices = {'kiwis': 6.00, 'apples': 4.50, 'peaches': 8.75}
otherFruitShop = shop.FruitShop(otherName, otherFruitPrices)
otherPrice = otherFruitShop.getCostPerPound('apples')
print(otherPrice)
print('Apples cost $%.2f at %s.' % (otherPrice, otherName))
print("My, that's expensive!")
```

This code is in `shopTest.py`; you can run it like this:

```console
(info8006) username@computername:python_basics$ python shopTest.py
Welcome to the Berkeley Bowl fruit shop
1.0
Apples cost $1.00 at the Berkeley Bowl.
Welcome to the Stanford Mall fruit shop
4.5
Apples cost $4.50 at the Stanford Mall.
My, that's expensive!
```

So what just happened? The `import shop` statement told Python to load all of the functions and classes in `shop.py`. The `line berkeleyShop = shop.FruitShop(shopName, fruitPrices)` constructs an instance of the `FruitShop` class defined in `shop.py`, by calling the `__init__` function in that class. Note that we only passed two arguments in, while `__init__` seems to take three arguments: `(self, name, fruitPrices)`. The reason for this is that all methods in a class have `self` as the first argument. The `self` variable’s value is automatically set to the object itself; when calling a method, you only supply the remaining arguments. The `self` variable contains all the data (`name` and `fruitPrices`) for the current specific instance (similar to `this` in Java). The print statements use the substitution operator (described in the [Python docs](https://docs.python.org/3.6/) if you’re curious).

### Static vs Instance Variables

The following example illustrates how to use static and instance variables in Python.

Create the `person_class.py` containing the following code:

```python
class Person:
    population = 0

    def __init__(self, myAge):
        self.age = myAge
        Person.population += 1

    def get_population(self):
        return Person.population

    def get_age(self):
        return self.age
```

We first compile the script:

`(info8006) username@computername:python_basics$ python person_class.py`

Now use the class as follows:

```python
>>> import person_class
>>> p1 = person_class.Person(12)
>>> p1.get_population()
1
>>> p2 = person_class.Person(63)
>>> p1.get_population()
2
>>> p2.get_population()
2
>>> p1.get_age()
12
>>> p2.get_age()
63
```
In the code above, `age` is an instance variable and `population` is a static variable. `population` is shared by all instances of the `Person` class whereas each instance has its own `age` variable.

### More Python Tips and Tricks

This tutorial has briefly touched on some major aspects of Python that will be relevant to the course. Here are some more useful tidbits:

- Use `range` to generate a sequence of integers, useful for generating traditional indexed for loops:

	```python
    for index in range(3):
        print(lst[index])
	```

- After importing a file, if you edit a source file, the changes will not be immediately propagated in the interpreter. For this, use the `reload` command:

	```python
    >>> reload(shop)
	```

### Troubleshooting

These are some problems (and their solutions) that new Python learners commonly encounter.

- **Problem**: ImportError: No module named py

  **Solution**: For import statements with `import <package-name>`, do not include the file extension (i.e. the `.py` string). For example, you should use: `import shop` NOT: `import shop.py`

- **Problem**: NameError: name ‘MY VARIABLE’ is not defined even after importing you may see this.

	**Solution**: To access a member of a module, you have to type `MODULE NAME.MEMBER NAME`, where `MODULE NAME` is the name of the `.py` file, and `MEMBER NAME` is the name of the variable (or function) you are trying to access.

- **Problem**: TypeError: ‘dict’ object is not callable

	**Solution**: Dictionary looks up are done using square brackets: [ and ]. NOT parenthesis: ( and ).

- **Problem**: ValueError: too many values to unpack

    **Solution**: Make sure the number of variables you are assigning in a for loop matches the number of elements in each item of the list. Similarly for working with tuples.

    For example, if `pair` is a tuple of two elements (e.g. `pair =('apple', 2.0)`) then the following code would cause the “too many values to unpack error”:

    `(a, b, c) = pair`

    Here is a problematic scenario involving a for loop:

	```python
      pairList = [('apples', 2.00), ('oranges', 1.50), ('pears', 1.75)]
      for fruit, price, color in pairList:
          print('%s fruit costs %f and is the color %s' % (fruit, price, color))
	```

- **Problem**: AttributeError: ‘list’ object has no attribute ‘length’ (or something similar)

    **Solution**: Finding length of lists is done using `len(NAME OF LIST)`.

- **Problem**: Changes to a file are not taking effect.

	**Solution**:
	1. Make sure you are saving all your files after any changes.
	2. If you are editing a file in a window different from the one you are using to execute python, make sure you `reload(_YOUR_MODULE_)` to guarantee your changes are being reflected. `reload` works similarly to `import`.

## Exercises

In the following, we will ask you to code, test, and find solutions for three problems.

First, you need to change the current directory to `exercices`.

```console
(info8006) username@computername:python_basics$ cd ..
(info8006) username@computername:tutorial_code$ ls
exercises python_basics
(info8006) username@computername:tutorial_code$ cd exercises/
(info8006) username@computername:exercises$ ls
addition.py
autograder.py
buyLotsOfFruit.py
shop.py
shopSmart.py
tools
test_cases
```

There are a number of files you’ll edit or run:

- `addition.py`: source file for question 1
- `buyLotsOfFruit.py`: source file for question 2
- `shop.py`: source file for question 3
- `shopSmart.py`: source file for question 3
- `autograder.py`: autograding script (see below)

and others you can ignore in the directory `tools`.

The command `python autograder.py` grades your solution to all three problems. If we run it before editing any files we get a page or two of output:

```console
(info8006) username@computername:exercises$ python autograder.py
Starting on 9-12 at 15:49:35

Question q1
===========
*** FAIL: test_cases/q1/addition1.test
*** 	add(a, b) must return the sum of a and b
*** 	student result: "0"
*** 	correct result: "2"
*** FAIL: test_cases/q1/addition2.test
*** 	add(a, b) must return the sum of a and b
*** 	student result: "0"
*** 	correct result: "5"
*** FAIL: test_cases/q1/addition3.test
*** 	add(a, b) must return the sum of a and b
*** 	student result: "0"
*** 	correct result: "7.9"
*** Tests failed.

### Question q1: 0/1 ###


Question q2
===========
*** FAIL: test_cases/q2/food_price1.test
*** 	buyLotsOfFruit must compute the correct cost of the order
*** 	student result: "0.0"
*** 	correct result: "12.25"
*** FAIL: test_cases/q2/food_price2.test
*** 	buyLotsOfFruit must compute the correct cost of the order
*** 	student result: "0.0"
*** 	correct result: "14.75"
*** FAIL: test_cases/q2/food_price3.test
*** 	buyLotsOfFruit must compute the correct cost of the order
*** 	student result: "0.0"
*** 	correct result: "6.4375"
*** Tests failed.

### Question q2: 0/1 ###


Question q3
===========
Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
*** FAIL: test_cases/q3/select_shop1.test
*** 	shopSmart(order, shops) must select the cheapest shop
*** 	student result: "None"
*** 	correct result: "<FruitShop: shop1>"
Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
*** FAIL: test_cases/q3/select_shop2.test
*** 	shopSmart(order, shops) must select the cheapest shop
*** 	student result: "None"
*** 	correct result: "<FruitShop: shop2>"
Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
Welcome to shop3 fruit shop
*** FAIL: test_cases/q3/select_shop3.test
*** 	shopSmart(order, shops) must select the cheapest shop
*** 	student result: "None"
*** 	correct result: "<FruitShop: shop3>"
*** Tests failed.

### Question q3: 0/1 ###


Finished at 23:39:51

Provisional grades
==================
Question q1: 0/1
Question q2: 0/1
Question q3: 0/1
------------------
Total: 0/3

Your grades are NOT yet registered.  To register your grades, make sure
to follow your instructor's guidelines to receive credit on your project.
```

For each of the three questions, this shows the results of that question’s tests, the questions grade, and a final summary at the end. Because you haven’t yet solved the questions, all the tests fail. As you solve each question you may find some tests pass while other fail. When all tests pass for a question, you get full marks.

Looking at the results for question 1, you can see that it has failed three tests with the error message “add(a, b) must return the sum of a and b”. The answer your code gives is always 0, but the correct answer is different. We’ll fix that in the next tab.


### Question 1: Addition

Open `addition.py` and look at the definition of `add`:

```python
def add(a, b):
    "Return the sum of a and b"
    "*** YOUR CODE HERE ***"
    return 0
```

The tests called this with `a` and `b` set to different values, but the code always returned zero. Modify this definition to read:

```python
def add(a, b):
    "Return the sum of a and b"
    print("Passed a = %s and b = %s, returning a + b = %s" % (a, b, a + b))
    return a + b
```

Now rerun the autograder (omitting the results for questions 2 and 3):

```console
(info8006) username@computername:exercises$ python autograder.py -q q1
Starting on 1-21 at 23:52:05

Question q1
===========
Passed a = 1 and b = 1, returning a + b = 2
*** PASS: test_cases/q1/addition1.test
*** 	add(a, b) returns the sum of a and b
Passed a = 2 and b = 3, returning a + b=5
*** PASS: test_cases/q1/addition2.test
*** 	add(a, b) returns the sum of a and b
Passed a = 10 and b = -2.1, returning a + b = 7.9
*** PASS: test_cases/q1/addition3.test
*** 	add(a, b) returns the sum of a and b

### Question q1: 1/1 ###

Finished at 23:41:01

Provisional grades
==================
Question q1: 1/1
Question q2: 0/1
Question q3: 0/1
------------------
Total: 1/3
```

You now pass all tests, getting full marks for question 1. Notice the new lines “Passed a=…” which appear before “*** PASS: …”. These are produced by the print statement in `add`. You can use print statements like that to output information useful for debugging.

### Question 2: `buyLotsOfFruit` function

Add a `buyLotsOfFruit(orderList)` function to `buyLotsOfFruit.py` which takes a list of `(fruit,pound)` tuples and returns the cost of your list. If there is some `fruit` in the list which doesn’t appear in `fruitPrices` it should print an error message and return `None`. Please do not change the `fruitPrices` variable.

Run `python autograder.py` until question 2 passes all tests and you get full marks. Each test will confirm that `buyLotsOfFruit(orderList)` returns the correct answer given various possible inputs. For example, `test_cases/q2/food_price1.test` tests whether:

`Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25`

### Question 3: `shopSmart` function

Fill in the function `shopSmart(orders,shops)` in `shopSmart.py`, which takes an `orderList` (like the kind passed in to `FruitShop.getPriceOfOrder`) and a list of `FruitShop` and returns the `FruitShop` where your order costs the least amount in total. Don’t change the file name or variable names, please.

Run `python autograder.py` until question 3 passes all tests and you get full marks. Each test will confirm that `shopSmart(orders,shops)` returns the correct answer given various possible inputs. For example, with the following variable definitions:

```python
orders1 = [('apples', 1.0), ('oranges', 3.0)]
orders2 = [('apples', 3.0)]
dir1 = {'apples': 2.0, 'oranges': 1.0}
shop1 =  shop.FruitShop('shop1',dir1)
dir2 = {'apples': 1.0, 'oranges': 5.0}
shop2 = shop.FruitShop('shop2', dir2)
shops = [shop1, shop2]
```

`test_cases/q3/select_shop1.test` tests whether: `shopSmart.shopSmart(orders1, shops) == shop1`

and `test_cases/q3/select_shop2.test` tests whether: `shopSmart.shopSmart(orders2, shops) == shop2`


## Going further

For more documentation and tutorials about Python, we recommend the following references:
- [Official Python tutorial](https://docs.python.org/3.6/tutorial/)
- [W3School](https://www.w3schools.com/python/default.asp)
- [Tutorialspoint](https://www.tutorialspoint.com/python/index.htm)
