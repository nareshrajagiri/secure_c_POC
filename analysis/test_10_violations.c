#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void TestViolations(void)
{
    /* STR31-C */
    char small_buffer[8];
    strcpy(small_buffer, "THIS_STRING_IS_TOO_LONG");

    /* STR30-C */
    char *msg = "HELLO";
    msg[0] = 'X';

    /* EXP34-C */
    int *ptr = NULL;
    *ptr = 10;

    /* EXP33-C */
    int uninitialized_var;
    int result = uninitialized_var + 1;

    /* ARR30-C */
    int arr[5];
    arr[10] = 100;

    /* INT33-C */
    int a = 10;
    int b = 0;
    int c = a / b;

    /* INT31-C */
    unsigned char value = 300;

    /* MEM35-C */
    int *numbers = malloc(2);
    numbers[1] = 10;

    /* EXP45-C */
    int flag = 0;
    if (flag = 1)
    {
        printf("Assignment inside if\n");
    }

    /* ERR33-C */
    FILE *fp = fopen("dummy.txt", "r");
    fclose(fp);

    printf("%d %d\n", result, c);
}