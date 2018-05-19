# Constants
CC=gcc
CFLAGS=-Wall -Werror
OUTPUT_DIR=build
OBJ=doubly-linked-list-example

# Targets
.PHONY: clean dll valgrind

all: $(OBJ)

clean:
	rm -rf $(OUTPUT_DIR)

build-dir:
	mkdir -p $(OUTPUT_DIR)

$(OBJ): build-dir $(OBJ).c
	$(CC) $(CFLAGS) $(OBJ).c -o $(OUTPUT_DIR)/$(OBJ)

valgrind: $(OBJ)
	valgrind --leak-check=full $(OUTPUT_DIR)/$(OBJ)
