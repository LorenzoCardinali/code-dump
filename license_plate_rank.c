#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int BASES[] = {17576000, 676000, 26000, 1000};

char* to_upper_case(char plate[]);

int is_plate_valid(char plate[]);

int letter_value(int c);

int main(int argc, char* argv[]) {
    // Check if any plate is given
    if (argc == 1) {
        printf("\nERROR: No plate given");
        return 0;
    }

    // Check if the plate has the correct lenght
    if (strlen(argv[1]) != 7) {
        printf("\nERROR: Plate must be 7 characters long");
        return 0;
    }

    // Check if plate is valid
    if (!is_plate_valid(argv[1])) {
        printf("\nERROR: Plate not valid.");
        return 0;
    }

    // Plate infos
    char numbs[] = {argv[1][2], argv[1][3], argv[1][4]};
    struct plate {
        char letters[5];
        int numbers;
    } plate = {{argv[1][0], argv[1][1], argv[1][5], argv[1][6]}, atoi(numbs)};

    // Calculating plate value
    int value = 0;
    for (int i = 0; i < 4; i++)
        value += letter_value(plate.letters[i]) * BASES[i];
    value += plate.numbers + 1;

    // Printing data
    printf("\nPlate---> \t%s", argv[1]);
    printf("\nValue---> \t%d", value);

    return 0;
}

char* to_upper_case(char str[]) {
    for (int i = 0; i < 7; i++) {
        if (str[i] >= 'a' && str[i] <= 'z')
            str[i] = str[i] - 32;
    }

    return str;
}

// Returns the value of a letter (es. a=1, b=2 ..)
// Returns -1 if the given char is not a letter
int letter_value(int c) {
    if (c >= 97 && c <= 122) {
        return c - 97;
    }

    if (c >= 65 && c <= 90) {
        return c - 65;
    }

    return -1;
}

// Returns 1 if a plate is valid, 0 otherwise
int is_plate_valid(char plate[]) {
    // Variable to store initial regex()
    regex_t reegex;

    // Creation of regEx
    regcomp(&reegex, "^[A-HJ-NPR-TV-Z]{2}[0-9]{3}[A-HJ-NPR-TV-Z]{2}$", REG_EXTENDED);

    // Checking if the plate matches the regex()
    int result = !regexec(&reegex, to_upper_case(plate), 0, NULL, 0);

    // Free memory allocated to the pattern buffer by regcomp()
    regfree(&reegex);

    return result;
}