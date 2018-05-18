.PHONY: dll valgrind

doubly-linked-list-example: doubly-linked-list-example.c
	gcc -Werror -Wall doubly-linked-list-example.c -o doubly-linked-list-example

dll: doubly-linked-list-example

valgrind: doubly-linked-list-example
	valgrind --leak-check=full ./doubly-linked-list-example
