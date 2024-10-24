// clang -c $file.c && rm $file.o

int c1;
int (c2[32]);
int (*(c3[32]));

int d1;
int (*d2);
int ((*d3)[32]);

int e1;
int (*e2);
int (*(*e3));

int f = sizeof(int([32]));