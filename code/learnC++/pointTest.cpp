#include<iostream>
#include <cstdio>
#include <cstring>
#include "point.h"
using namespace std;

struct Point
{
	int x;
	int y;
};

PPoint PtCreate(int x,int y){

	PPoint t = new Point;
	t->x = x;
	t->y = y;

}

void PtDestroy(PPoint point){

	if (point)
	{
		delete point;
	}
}

void PtGetValue(PPoint point,int *x,int*y){
	if (point)
	{
		if (x)
		{
			*x=point->x;/* code */
		}
		if (y)
		{
			*y=point->y/* code */
		}
		/* code */
	}

}
void PtSetValue(PPoint point,int x,int y){

	if (point)
	{
		point->x=x;
		point->y=y;/* code */
	}
}

bool PtCompare(PPoint point1,PPoint point2){
	if (!point2||!point1)
	{
		cout<<"this is invalid compare"<<endl;/* code */
	}
	return (point1->x==point2->x)&&(point2->y==point1->x)
}
int main(int argc, char const *argv[])
{
	
	return 0;
}