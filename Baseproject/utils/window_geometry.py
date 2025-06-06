# utils/window_geometry.py

def apply_geometry_tracking(window, config, key="default"):
    """Attach saved geometry and track it on close."""
    geo_key = f"geometry_{key}"
    saved_geo = config.get(geo_key)
    if saved_geo:
        window.geometry(saved_geo)

    def on_close():
        config.set(geo_key, window.geometry())
        config.save()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
