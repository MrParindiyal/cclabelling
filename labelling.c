#include <stdio.h>
#include <stdlib.h>

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
    
    int rows = sizeof(img)/sizeof(img[0]);
    int cols = sizeof(img[0])/sizeof(img[0][0]);
    int curr = 2;
    
    for (int row = 0; row < rows; row++){
        for (int col = 0; col < cols; col++){

            if (col && row && img[row][col]){
            
                if (!img[row - 1][col] && !img[row][col - 1]){
                    img[row][col] = curr++;
                }   

                else {
                    img[row][col] = img[row - 1][col] > 0 ? img[row - 1][col] : img[row][col - 1];
                    img[row][col] = img[row][col - 1] < img[row][col] && img[row][col - 1] ? img[row][col - 1] : img[row][col];
                }
            }
            
            else if (row == 0 && col > 0 && img[row][col]){
                img[row][col] = !img[row][col - 1] ? curr++ : img[row][col - 1];
            }

            else if (col == 0 && img[row][col]){
                img[row][col] = img[row - 1][col] ? img[row - 1][col] : curr++;
            }

        }
    }


    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            printf("%i ", img[i][j]);
        }
        printf("\n");
    }

    return 0;
}
