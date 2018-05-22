/* Includes */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* Defines */
// 
// This is simply to prettify output, and was suggested
// via https://stackoverflow.com/questions/3219393/stdlib-and-colored-output-in-c
#define ANSI_RED     "\x1b[31m"
#define ANSI_GREEN   "\x1b[32m"
#define ANSI_YELLOW  "\x1b[33m"
#define ANSI_BLUE    "\x1b[34m"
#define ANSI_MAGENTA "\x1b[35m"
#define ANSI_CYAN    "\x1b[36m"
#define ANSI_RST   "\x1b[0m"


/* Structures */
// This structure holds a single character, and contains pointers to the next and previous nodes
// in the singly-linked list (if applicable).
typedef struct dll_node {
    char c;
    struct dll_node *next;
    struct dll_node *prev;
} dll_node;

// This struct keeps track of the head and tail of the doubly-linked list.
typedef struct dll {
    struct dll_node *head;
    struct dll_node *tail;
} dll;


/* Prototypes */
dll* dll_new(void);
int dll_delete(dll_node *head);
int dll_add_node(dll *list, char c);
int dll_delete_node(dll *list, char c);
int dll_insert_word(char* word, dll* list);
void pretty_print(const dll* list);


/* Main function */
int main(int argc, char* argv[]) {

    // Prompt the user for input
    if (argc != 2) {
        printf("Usage: %s just_some_string\n", argv[0]);
        printf("\nHere's an example I cooked up earlier:\n\n");
    }

    // Coalese the input if required
    char* word = argc == 2 ? argv[1] : "Richard";

    // Allocate memory for the doubly-linked list metadata struct
    dll *list = dll_new();
    if (list == NULL) {
        fprintf(stderr, "Error: dll_new returned a NULL.\n");
        return 1;
    }

    // Perform char-by-char insertion
    int insertion = dll_insert_word(word, list);
    if (insertion != 0) {
        fprintf(stderr, "Error: Insertion of word failed - a non-zero value was returned by dll_insert_word");
        return 1;
    }

    // Display pretty output
    pretty_print(list);

    // Cleanup time!
    int delete_result = dll_delete(list->head);
    if (delete_result != 0) {
        fprintf(stderr, "You must specify a valid dll_node pointer in order to delete the list\n");
        return 1;
    }
    free(list);
    list = NULL;
}


/* Functions */
dll* dll_new(void) {

    // Allocate memory for the doubly-linked list metadata struct
    dll* list = malloc(sizeof(struct dll));
    if (list == NULL) {
        // Let the caller handle this NULL
        fprintf(stderr, "dll_new: Unable to allocate memory\n");
        return NULL;
    }

    // Set both head and tail pointers to NULL
    list->head = NULL;
    list->tail = NULL;

    return list;
}


// dll_delete destroys the doubly-linked list by iteratively freeing allocated memory
int dll_delete(dll_node *head) {
    if (head == NULL) {
        return -1;
    }

    dll_node *old_head = head;
    while (head != NULL) {
        head = head->next;
        free(old_head);
        old_head = head;
    }
    return 0;
}


// dll_add_node inserts a new dll_node into the head position of the doubly-linked list
int dll_add_node(dll *list, char c) {
    // Create a new doubly-linked list node
    dll_node *node = malloc(sizeof(struct dll_node));
    if (node == NULL) {
        fprintf(stderr, "malloc returned NULL, not a pointer to a dll_node!\n");
        return 1;
    }

    // If this is the first time we've been called, nominate the new node as
    // both the head and the tail of the doubly-linked list
    if (list->tail == NULL) {
        list->tail = node;
    }

    // Populate the node, and attach the necessary pointers
    node->c = c;
    node->prev = NULL;
    node->next = list->head;
    if (list->head != NULL) {
        list->head->prev = node;
    }
    list->head = node;

    return 0;
}


// This function returns inserts an entire word
// It's defined as a void* return function, as it will only ever return NULL
int dll_insert_word(char* word, dll* list) {
    // Populate the list with the user's string
    for (int i = 0, len = strlen(word); i < len; i++) {
        int result = dll_add_node(list, word[i]);
        if (result != 0) {
            fprintf(stderr, "Failed to insert word, as dll_add_node returned an error");
            return 1;
        }
    }
    return 0;
}


// Walk the dll forwards and backwards, and create some test output while doing so.
void pretty_print(const dll* list) {
    // Output formatting below
    printf(ANSI_GREEN"[+]"ANSI_RST" Traverse the list forwards (the resultant 'word' is backwards):\n");
    dll_node *mut_node = list->head;

    printf("        [");
    while (mut_node != NULL) {
        printf("'" ANSI_MAGENTA "%c" ANSI_RST "', ", mut_node->c);
        mut_node = mut_node->next;
    }
    printf("]\n");


    printf(ANSI_GREEN"[+]"ANSI_RST" Traverse the link forwards (the resultant 'word' is forwards):\n");
    mut_node = list->tail;
    printf("        [");
    while (mut_node != NULL) {
        printf("'" ANSI_MAGENTA "%c" ANSI_RST "', ", mut_node->c);
        mut_node = mut_node->prev;
    }
    printf("]\n");
}
