## Picombo
Picombo is a Python library that offers interactive filtering functionality. When a list object is provided to Picombo, it displays a filtering interface to the user, allowing them to interactively filter through the list. Once a user selects an item, Picombo returns that value.

In essence, it's like having Percol as a library that can be freely integrated into any program.

## Installation

```
$ pip install picombo
```

## Example
```
import picombo

my_list = [i for i in range(1,101)]
pw = picombo.PickWindow(my_list)
res = pw.search()

print(res)
```

## Demo
If you clone the repository, you can demo the filtering of a list of all country names.

```
$ pipenv install
$ pipenv run demo
```
