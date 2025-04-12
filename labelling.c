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

    // assuming image is of bin format, we start from '2' to avoid confusion
    int curr = 2;
    
    // start iterating the image
    for (int row = 0; row < rows; row++){
        for (int col = 0; col < cols; col++){

            // pixel is not in 1st row or 1st col, and pixel is active (i.e. 1)
            if (col && row && img[row][col]){
            
                // if both upper and left pixel are inactive, then create new label
                if (!img[row - 1][col] && !img[row][col - 1]){
                    img[row][col] = curr++;  // and update the current label
                }   

                else { // otherwise, atleast one of the upper or left pixel is active
                    // copy upper label if it's active, otherwise copy left label
                    img[row][col] = img[row - 1][col] > 0 ? img[row - 1][col] : img[row][col - 1];

                    // if left pixel is active and less than current label, we copy
                    img[row][col] = img[row][col - 1] < img[row][col] && img[row][col - 1] ? img[row][col - 1] : img[row][col];
                }
            }
            
            // if active pixel is in 1st row but not in 1st col
            else if (row == 0 && col > 0 && img[row][col]){
                img[row][col] = img[row][col - 1] ? img[row][col - 1] : curr++;
            }

            // if pixel is in 1st col
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
