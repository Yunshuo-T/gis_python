def zonal_stat(rp,vp,merge=False,stats_funcs=None):
    """
    Calculate zonal statistics on a raster based on the polygons from a vector.
    Args:
        rp(str): Raster file path;
        
        vp(str): Vector file path, which can be read by geopandas;
        
        merge (bool): Defalut Flase. If True, returns the vector's GeoDataFrame with stats merged; otherwise, DataFrame of stats;
        
        stats_funcs (dict):Defalut: {
                "min": np.min,"max": np.max,"count": len, "std": np.std}; 
                Optional mapping of stat name to function, e.g., {'mean': np.mean, 'sum': np.sum}. 
    Returns:
        The vector's GeoDataFrame with stats merged or DataFrame of stats
    Depencies:
        rasterio
        numpy
        geopandas
        pandas
        rasterio.mask
    """
    import rasterio as rio
    import numpy as np
    import geopandas as gpd
    import pandas as pd
    from rasterio.mask import mask
    
    result = []
    zones = gpd.read_file(vp)
    if stats_funcs is None:
        stats_funcs = {
        "mean": np.mean,
        "min": np.min,
        "max": np.max,
        "count": len,
        "std": np.std
        }
    with rio.open(rp) as src:
        if zones.crs != src.crs:
            zones.to_crs(src.crs)
        
        for idx,row in zones.iterrows():
            geom = [row['geometry']]
            out_image,out_transform = mask(src,geom,crop=True)
            
            # Mask out nodata
            data = out_image[0]
            if src.nodata is not None:
                data = data[data != src.nodata]
            else:
                data = data[data != 0]
            if data.size == 0:
                stats = {name: np.nan for name in stats_funcs.keys()}
            else:
                stats = {name: func(data) for name, func in stats_funcs.items()}
            stats['index'] = idx
            result.append(stats)
    
    # convert stats dic to dataframe
    zonal_stat = pd.DataFrame(result).set_index('index')
    
    if merge:
        zones = zones.merge(zonal_stat,left_index=True, right_index=True)
        return zones
    else:
        return zonal_stat
