#include "cubiomes/generator.h"
#include "cubiomes/util.h"
#include "stdio.h"

/* 
How to Compile: 

1. Compile cubiomes first. 

```
$ cd cubiomes/ 
$ make
```

2. Compile with `libcubiomes.a`

```
$ cd ..
$ gcc generate-image.c cubiomes/libcubiomes.a -fwrapv -lm -O3 -o ./generate-image
```
*/

int main(int argc, char* argv[])
{
    if (argc < 2) 
    {
        fprintf(stderr, "USAGE: generate-image [seed] [/path/to/output.ppm]\n");
        exit(EXIT_FAILURE);
    }

    Generator g;
    setupGenerator(&g, MC_1_21_3, 0);

    uint64_t seed = atoi(argv[1]);
    applySeed(&g, DIM_OVERWORLD, seed);

    Range r;
    r.scale = 16;
    r.x = 0, r.z = 0;   
    r.sx = 500, r.sz = 500; 
    r.y = 256, r.sy = 1;

    int *biomeIds = allocCache(&g, r);

    genBiomes(&g, biomeIds, r);

    int pix4cell = 4;
    int imgWidth = pix4cell*r.sx, imgHeight = pix4cell*r.sz;
    unsigned char biomeColors[256][3];
    initBiomeColors(biomeColors);
    unsigned char *rgb = (unsigned char *) malloc(3*imgWidth*imgHeight);
    biomesToImage(rgb, biomeColors, biomeIds, r.sx, r.sz, pix4cell, 2);

    savePPM(argv[2], rgb, imgWidth, imgHeight);

    free(biomeIds);
    free(rgb);

    return EXIT_SUCCESS;
}