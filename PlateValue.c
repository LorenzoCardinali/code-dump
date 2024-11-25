#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int BASES[] = {17576000, 676000, 26000, 1000};

int isPlateValid(char plate[]);

int letterValue(int c);

int main(int argc, char* argv[]) {
    // Check if any plate is given
    if (argc == 1) {
        printf("\nERROR: No plate given");
        return 0;
    }

    // Check if plate is valid
    if (!isPlateValid(argv[1])) {
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
        value += letterValue(plate.letters[i]) * BASES[i];
    value += plate.numbers + 1;

    // Printing data
    printf("\nPlate---> \t%s", argv[1]);
    printf("\nValue---> \t%d", value);

    return 0;
}

// Returns the value of a letter (es. a=1, b=2 ..)
// Returns -1 if the given char is not a letter
int letterValue(int c) {
    if (c >= 97 && c <= 122) {
        return c - 97;
    }

    if (c >= 65 && c <= 90) {
        return c - 65;
    }

    return -1;
}

// Returns 1 if a plate is valid, 0 otherwise
int isPlateValid(char plate[]) {
    if (strlen(plate) != 7) return 0;

    for (int i = 0; i < 7; i++) {
        if (i > 1 && i < 5) {
            if (plate[i] < 48 || plate[i] > 57) return 0;
        }

        else {
            if (letterValue(plate[i]) == -1) return 0;
        }
    }

    return 1;
}