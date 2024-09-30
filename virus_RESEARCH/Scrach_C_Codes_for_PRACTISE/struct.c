#include<stdio.h>
struct point{
    int x,y;
};


int main()
{
    struct point p1={1,2};
    printf("%d %d",p1.x,p1.y);


    return 0;
}