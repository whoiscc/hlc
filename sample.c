// clang -c $file.c && rm $file.o

typedef unsigned char uint8_t;
uint8_t (*(*foo1));
uint8_t ((foo2[32])[32]);
uint8_t (*(foo3[32]));
uint8_t ((*foo4)[32]);
int bar1 = sizeof(uint8_t (*(*)));
int bar2 = sizeof(uint8_t (([32])[32]));
int bar3 = sizeof(uint8_t (*([32])));
int bar4 = sizeof(uint8_t ((*)[32]));

int (*baz1());
int (*baz1()) { return 0; }
int (*(*baz2(int (*x))));
