#include <stdlib.h>
#include <stdio.h>
#include <time.h> 
#include <stdbool.h>
#include <float.h>
#include <string.h>
#include <math.h>

#define PI 3.1415926535897932384626433832795
#define EARTH_RADIUS 6378.137
#define index(i,j,cities)((i*cities)+j)



void read_data(unsigned int cities, float *x_coordinate, float *y_coordinate, char **location, FILE *fp);
void read_line(char *line, int index, float *x_coordinate, float *y_coordinate, char **location);
void get_distances(float *distance, float *x_coordinate, float *y_coordinate, unsigned int cities);
void read_optimum_file(FILE *fp, unsigned int *tour, unsigned int cities);
void read_files(FILE *fp, float *distance, unsigned int *tour, char **location, unsigned int cities);


void read_files(FILE *fp, float *distance, unsigned int *tour, char **location, unsigned int cities){

	float *x_coordinate = (float *)malloc(cities*sizeof(float));
	float *y_coordinate = (float *)malloc(cities*sizeof(float));

	if(fp == NULL){
      fprintf(stderr, "Error in opening the file");
      exit(1);
   	}
	read_data(cities, x_coordinate, y_coordinate, location, fp);
	get_distances(distance, x_coordinate, y_coordinate, cities);

	
	if(fp == NULL){
      fprintf(stderr, "Error in opening optimum file\n");
      exit(1);
   	}

}

void read_optimum_file(FILE *fp, unsigned int *tour, unsigned int cities){
	int i;
	int temp;
	for(i = 0; i < cities; i++){
		fscanf(fp,"%d",&temp);
		tour[i] = temp - 1;
	}
	tour[cities] = tour[0];

}

float haversine(float lat1, float lon1, float lat2, float lon2)
    {
    //float dlat, dlon, c1, c2, d1, d2, a, c, t;
    float dlat, dlong, a, c, distance;
    float radLat1, radLat2;
    dlat = ((lat2 - lat1) / 180) * PI;
    dlong = ((lon2 - lon1) / 180) * PI;
    radLat1 = (lat1 / 180) * PI;
    radLat2 = (lat2 / 180) * PI;
    a = pow(sin(dlat/2),2) + (cos(radLat1) * cos(radLat2) * pow(sin(dlong/2),2));
    c = 2. * atan2(sqrt(a),sqrt(1-a));
    distance = 6378.137 * c;
    return distance;
}

void get_distances(float *distance, float *x_coordinate, float *y_coordinate, unsigned int cities){
	int i = 0;
	int j = 0;
	
	for(i = 0; i < cities; i++){
		for(j = 0; j < cities; j++){
			distance[index(i,j,cities)] = haversine(x_coordinate[i], y_coordinate[i], x_coordinate[j], y_coordinate[j]);
		}
	}
	return;
}


void read_data(unsigned int cities, float *x_coordinate, float *y_coordinate, char **location, FILE *fp){
   	int i;
   	ssize_t read;
   	size_t len = 0;
   	char * line = NULL;
   

   	for(i = 0; i < cities; i++){
   		read = getline(&line, &len, fp);
   		if(read == -1){
   			fprintf(stderr, "Error in reading file");
      		exit(1);
   		}
   		read_line(line, i, x_coordinate, y_coordinate, location);
   	}
   	return;
}

void read_line(char *line, int index, float *x_coordinate, float *y_coordinate, char **location){
	char *tuples;
	tuples = strtok(line,"@");

	int temp = 0, i;
	while (tuples != NULL) {
		if(temp == 0){
			for (i = 0; i < strlen(tuples); i++)
				location[index][i] = tuples[i];
			location[index][i] = '\0';
		}
    	if(temp == 1){
    		x_coordinate[index] = (float) atof(tuples);
    	}
    	if(temp == 2){
    		y_coordinate[index] = (float) atof(tuples);
    	}
    	tuples = strtok(NULL, " ");
    	temp++;
	}
	return;
}


void print_min_cost(float *cost_array, unsigned int cities){

	int i;
	int j;
	for(i = 0; i < cities; i++){
		for(j = 0; j < cities; j++){
			printf("%0.1f ",cost_array[index(i,j,cities+1)]);
		}
		printf("\n");
	}
}

void print_cycle(unsigned int *cycle, unsigned int cities){
	int i;
	for(i = 0; i < cities+1; i++){
		printf("%d ",cycle[i]);
	}
	printf("\n");
}