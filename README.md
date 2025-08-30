# Minesoc Seedcracking 

Find good seeds for the next minesoc server. 

## Criteria 

- All biomes present within initial world border region 
- All structures present within initial world border region 

## Notes 

- `data.tar.gz` contents: 
    - `minesoc-seeds.session`: [cubiomes-viewer](https://github.com/Cubitect/cubiomes-viewer) seedcracking session
    - `biomes.txt`: Count of each biome for a given seed within -5k to 5k of `[0 0]`
    - `structures.txt`: Location and details of each structure for a given seed within -5k to 5k of `[0 0]`
    - `worlds.json`: Serialised world information 
- Each seed was generated with MC Version 1.21.3 worldgen, so some manual checking for stuff added post 1.21.3 is necessary