/**
 * Document: MaxCompiler Tutorial (maxcompiler-tutorial.pdf)
 * Chapter: 12      Example: 3      Name: Dualport mapped ROM
 * MaxFile name: DualPortMappedRom
 * Summary:
 *       CPU code for a design which uses a dual port mapped ROM.
 */
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#include "Maxfiles.h"
#include <MaxSLiCInterface.h>

void generateInputData(int size, int centroids, double *centroids_x,double *centroids_y, float *x, float *y)
{
	for (int i = 0; i < centroids; i++) {
		centroids_x[i] = rand();
		centroids_y[i] = rand();
	}
    for (int i = 0; i < size; i++) {
		x[i] = rand();
		y[i] = rand();
	}
}

int main()
{
	const int size = 256;
	const int centroids = 16;
	int sizeBytesFloat = size * sizeof(float);
	int sizeBytesDouble = centroids * sizeof(double);
	double *centroids_x = malloc(sizeBytesDouble);
	double *centroids_y = malloc(sizeBytesDouble);
	float *in_x = malloc(sizeBytesFloat);
	float *in_y = malloc(sizeBytesFloat);
	float *result = malloc(sizeBytesFloat);

	generateInputData(size,	centroids, centroids_x, centroids_y, in_x, in_y);

	printf("Running DFE.\n");
	DualPortMappedRom(size, in_x, in_y,	result,	centroids_x, centroids_y);
	for(int i=0;i<size;i++){
	    printf("%f", result[i]);
	}

	return 0;
}
