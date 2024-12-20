from PIL import Image
import numpy as np
import moviepy.editor as mp
import math

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
 
        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]
 
        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)
 
        img = img.resize(new_size, Image.LANCZOS)
 
        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)
 
        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)
 
        result = np.array(img)
        img.close()
 
        return result
 
    return clip.fl(effect)

def zoom_out_effect(clip, zoom_max_ratio=0.2, zoom_out_factor=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
 
        # Reverse the zoom effect by starting zoomed in and zooming out
        scale_factor = zoom_max_ratio - (zoom_out_factor * t)
        scale_factor = max(scale_factor, 0)  # Ensure scale factor doesn't go negative
 
        new_size = [
            math.ceil(base_size[0] * (1 + scale_factor)),
            math.ceil(base_size[1] * (1 + scale_factor))
        ]
 
        # The new dimensions must be even.
        new_size[0] = new_size[0] - (new_size[0] % 2)
        new_size[1] = new_size[1] - (new_size[1] % 2)
 
        img = img.resize(new_size, Image.LANCZOS)
 
        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)
 
        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ])
 
        # Resize back to base size
        img = img.resize(base_size, Image.LANCZOS)
 
        result = np.array(img)
        img.close()
 
        return result
 
    return clip.fl(effect)

def zoom_in_out_effect(clip, zoom_ratio=0.04, duration_ratio=0.5):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        half_duration = float(clip.duration) * float(duration_ratio)
        print("clip duration: ",  clip.duration)
        print("half duration: ", half_duration)
        print("t: ", t)
        print("duration ratio: ", duration_ratio)
        if t <= half_duration:
            scale_factor = 1 + (int(zoom_ratio) * (t / half_duration))
        else:
            scale_factor = 1 + (zoom_ratio * ((clip.duration - t) / half_duration))

        new_size = [
            math.ceil(base_size[0] * scale_factor),
            math.ceil(base_size[1] * scale_factor)
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)