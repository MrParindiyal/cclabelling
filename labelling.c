#include <stdio.h>
#include <stdlib.h>

void printer(int x, int y, int [x][y]);
int** label(int x, int y, int [x][y]);

// merge everything to main
// too many type restrictions

int main(){
    int img[10][10] = {
        {0, 0, 0, 0, 1, 1, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 1, 0, 0, 0, 0},
        {0, 0, 1, 0, 0, 0, 0, 1, 0, 0},
        {0, 1, 1, 1, 0, 0, 1, 1, 1, 0},
        {0, 1, 1, 0, 0, 1, 1, 0, 1, 0},
        {0, 0, 1, 1, 0, 1, 1, 1, 1, 0},
        {0, 0, 0, 1, 0, 0, 0, 0, 1, 0},
        {0, 0, 1, 1, 0, 0, 0, 1, 1, 0},
        {0, 0, 0, 0, 0, 1, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 1, 0, 0, 0}
    };

    // int** postproc = label(sizeof(img)/sizeof(img[0]), sizeof(img[0])/sizeof(img[0][0]), img);
    printer(sizeof(img)/sizeof(img[0]), sizeof(img[0])/sizeof(img[0][0]), img);

    // common
    // printer(sizeof(postproc)/sizeof(postproc[0]), sizeof(postproc[0])/sizeof(postproc[0][0]), postproc);

    // free(postproc);
    return 0;
}

void printer(int h, int w, int arr[h][w]){
    for (int i = 0; i < h; i++){
        for (int j = 0; j < w; j++){
            printf("%i ", arr[i][j]);
        }
        printf("\n");
    }
}

int** label(int h, int w, int img[h][w]) {
    int **out = malloc(h * sizeof(int*));

    for (int i = 0; i < h; i++) {
        out[i] = malloc(w * sizeof(int));
    
        for (int j = 0; j < w; j++) {
            out[i][j] = img[i][j] + 1;
        }
    }

    // FREE ??
    return out;
}