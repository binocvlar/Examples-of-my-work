Fetching and building C-lang examples
=====================================

```bash
$ git clone https://github.com/binocvlar/Examples-of-my-work.git
$ cd Examples-of-my-work/C/
$ make all
```

Table of contents
-----------------

| Name                       | Purpose                                                                        |
| -------------------------- | ------------------------------------------------------------------------------ |
| doubly-linked-list-example | Implementation of a singly-linked list datastructure that does not use globals |


Example run: doubly-linked-list-example
---------------------------------------
```bash
$ build/doubly-linked-list-example
Usage: build/doubly-linked-list-example just_some_string

Here's an example I cooked up earlier:

[+] Traverse the list forwards (the resultant 'word' is backwards):
        ['d', 'r', 'a', 'h', 'c', 'i', 'R', ]
[+] Traverse the link forwards (the resultant 'word' is forwards):
        ['R', 'i', 'c', 'h', 'a', 'r', 'd', ]
```

Example run: doubly-linked-list-example - with an argument
----------------------------------------------------------
```bash
$ build/doubly-linked-list-example GitHub
[+] Traverse the list forwards (the resultant 'word' is backwards):
        ['b', 'u', 'H', 't', 'i', 'G', ]
[+] Traverse the link forwards (the resultant 'word' is forwards):
        ['G', 'i', 't', 'H', 'u', 'b', ]

```
