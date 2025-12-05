#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Struktur
typedef struct {
    char name[50];
    char message[1000];
} User;

// Funktionen
void init_users(User users[], int size);
void print_menu(User users[]);
void display_user(User user);
void handle_input(char *input, User users[]);
void chat_loop(User users[]);

int main() {
    int size = 10;
    User users[size];

    init_users(users, size);
    chat_loop(users);

    return 0;
}

void init_users(User users[], int size) {
    for (int i = 0; i < size; i++) {
        strcpy(users[i].name, "");
        strcpy(users[i].message, "");
    }

    strcpy(users[0].name, "Robin");
    strcpy(users[0].message, "Willkommen! Ich bin Robin.");

    strcpy(users[1].name, "Benutzer");
    strcpy(users[1].message, "Bitte geben Sie Ihre Frage oder Anfrage ein.");
}

void print_menu(User users[]) {
    printf("Chatoberfläche für %s\n", users[0].name);
    printf("--------------------\n");
    printf("1. Fragen stellen\n");
    printf("2. Antworten lesen\n");
    printf("3. Beenden\n");
}

void display_user(User user) {
    printf("%s: %s\n", user.name, user.message);
}

void handle_input(char *input, User users[]) {
    if (strcmp(input, "1\n") == 0) {
        printf("Ihre Frage: ");
        fgets(users[1].message, 1000, stdin);
    }
    else if (strcmp(input, "2\n") == 0) {
        display_user(users[0]);   // Robin
        display_user(users[1]);   // Benutzer
    }
    else if (strcmp(input, "3\n") == 0) {
        printf("Programm beendet.\n");
        exit(0);
    }
    else {
        printf("Ungültige Eingabe.\n");
    }
}

void chat_loop(User users[]) {
    char input[100];

    while (1) {
        print_menu(users);
        printf("Auswahl: ");
        fgets(input, sizeof(input), stdin);
        handle_input(input, users);
    }
}
