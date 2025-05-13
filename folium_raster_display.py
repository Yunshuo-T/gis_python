def folium_raster_display(file_path,file_name,tile_name = "OpenstreetMap",control_scale=False,zoom_start=10):
    """
    Display a raster file using "folium.raster_layers.ImageOverlay" in Folium.
    Attention: tha raster file's bounds should be in lat and lon format, otherwise it has to transfrom in advance.
    Args:
        file_path (str): Path to the raster file.
        file_name(str): The name of the raster file.
        tile_name (str): Default is "OpenstreetMap". Name of the tile layer to use. 
        control_scale (bool): Default is False. Whether to show the scale control. 
        zoom_start(int):  int, default 10. Initial zoom level for the map.
    Returns:
        folium.Map: Folium map with the raster overlay.
    Depencies:
        - folium
        - rasterio
        - numpy
        - PIL (Pillow)
    """
    import folium
    from PIL import Image
    import rasterio
    import folium.raster_layers
    # Open the raster file using rasterio
    with rasterio.open(file_path) as src:
        
        # Get the bounds of the raster
        bounds = src.bounds
        converted_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]
        # Convert the bands to a PIL image
        image = Image.open(file_path)
        # Create a Folium map centered on the raster bounds
        m = folium.Map(
            location=[
                (bounds.top + bounds.bottom) / 2, 
                (bounds.left + bounds.right) / 2], 
            zoom_start=zoom_start,
            tiles=tile_name,
            control_scale=control_scale,
        )
        # Add the raster overlay to the map
        folium.raster_layers.ImageOverlay(
            image=image,
            bounds=converted_bounds,
            mercator_project=True,
            overlay=True,
            name = str(file_name),
        ).add_to(m)
        folium.LayerControl().add_to(m)
        return m
