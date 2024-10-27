#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>

// Testing in libc-2.39
// gcc band.c -o band -fno-stack-protector -fPIE -fPIC -Wl,-z,relro -Wl,-z,now

char *slime_ptrs[0x7];
int slime_size[0x7];
int slime_status[0x7];
int idx = 0;

void init()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
}

void menu()
{
    puts("=== NAUP'S SLIME MACHINE ===");
    puts("1) Create SLIME");
    puts("2) Get SLIME information");
    puts("3) Set SLIME information");
    puts("4) KILL SLIME");
    puts("5) End");
    printf(">>> ");
}

void create()
{
    int size;

    if (idx >= 0x7) {
        return;
    }

    printf("size: ");
    scanf("%d", &size);
        
    slime_size[idx] = size;
    slime_ptrs[idx] = malloc(size);
    slime_status[idx] = 1;
    
    printf("Create!!! SLIME[%d]\n", idx);

    idx++;
}


void get()
{
    int idx;

    printf("index: ");
    scanf("%d", &idx);
    if(idx < 0 || idx > 0x7){
        printf("error index\n");
        return;
    }
    printf("SLIME[%d]: %s\n", idx, slime_ptrs[idx]);

}

void set()
{
    int idx;

    printf("index: ");
    scanf("%d", &idx);
    if(idx < 0 || idx > 0x7){
        printf("error index\n");
        return;
    }
    printf("data: ");
    read(0, slime_ptrs[idx], slime_size[idx]);
    
}

void delete()
{
    int idx;

    printf("index: ");
    scanf("%d", &idx);
    
    if (slime_ptrs[idx] && slime_status[idx]) {
        free(slime_ptrs[idx]);
        slime_status[idx] = 0;
    }
}


void gift(){
    size_t stack_var;
    printf("gift: %p \n", (char *)&stack_var);
}

int a=1;

int main(void)
{
    init();
    gift();
    while(a) {
        menu();
        int num;
        scanf("%d", &num);
        switch(num) {
        case 1:
            create();
            break;
        case 2:
            get();
            break;
        case 3:
            set();
            break;
        case 4:
            delete();
            break;
        case 5:
            a=0;
            break;
        default:
            printf("Err!!!");
            break;
        }
    }
    return 0;
}