import math
import time
import sys
import os

# --- Configuration ---
WIDTH = 80
HEIGHT = 40
SCALE = 35          # Zoom level
SPEED = 1.0
# Denser ASCII palette for better solidity
ASCII_CHARS = " .:-=+*#%@"

def get_pen_geometry(h, theta):
    """
    Returns x, y, z, and surface normals for a specific point on the pen.
    h: height along the pen (0.0 to 1.0)
    theta: angle around the pen (0 to 2pi)
    """
    
    # --- Dimensions (Relative to total length 1.0) ---
    NIB_LEN = 0.15
    GRIP_LEN = 0.15
    BARREL_LEN = 0.50
    # Cap takes up the rest
    
    # Total Length = 10 units in model space
    L = 10.0 
    y = (h * L) - (L / 2) # Center the pen at y=0
    
    radius = 0
    
    # --- 1. THE NIB (The sharp writing tip) ---
    if h < NIB_LEN:
        # A cone that tapers to a sharp point
        # Normalized progress within the nib (0 to 1)
        prog = h / NIB_LEN
        radius = 0.01 + (prog * 0.25) 
        
        # Flatten the nib slightly to look like a fountain pen tip
        # by squashing x axis
        x_scale = 0.6 if h < (NIB_LEN * 0.8) else 1.0
        
        rx = radius * math.cos(theta) * x_scale
        rz = radius * math.sin(theta)
        return rx, y, rz, math.cos(theta), 0, math.sin(theta)

    # --- 2. THE GRIP (Where you hold it) ---
    elif h < (NIB_LEN + GRIP_LEN):
        # Hourglass / tapered cylinder shape
        prog = (h - NIB_LEN) / GRIP_LEN
        # Radius goes from 0.25 -> 0.35 -> 0.30 (curved grip)
        radius = 0.26 + math.sin(prog * math.pi) * 0.05
        
    # --- 3. THE BARREL (Main body) ---
    elif h < (NIB_LEN + GRIP_LEN + BARREL_LEN):
        radius = 0.32
        
    # --- 4. THE CAP (Top part, slightly wider) ---
    else:
        radius = 0.36
        
        # --- THE CLIP DETAIL ---
        # Extrude a rectangle on one side of the cap
        # Check if we are in the angle range for the clip
        if -0.3 < theta < 0.3:
            # Make the clip stick out
            radius += 0.15
            
            # Add a little gap between clip and body at the bottom of the cap
            cap_local_h = h - (NIB_LEN + GRIP_LEN + BARREL_LEN)
            if cap_local_h < 0.05 and abs(theta) < 0.2:
                radius -= 0.15 # The gap under the clip

    # Calculate standard cylinder coordinates
    x = radius * math.cos(theta)
    z = radius * math.sin(theta)
    
    # Normals
    nx = math.cos(theta)
    ny = 0
    nz = math.sin(theta)
    
    return x, -y, z, nx, ny, nz # -y to flip so nib is down

def rotate(x, y, z, pitch, roll, yaw):
    # X-Axis Rotation (Pitch)
    yx = y * math.cos(pitch) - z * math.sin(pitch)
    zx = y * math.sin(pitch) + z * math.cos(pitch)
    y, z = yx, zx

    # Y-Axis Rotation (Yaw)
    xz = x * math.cos(yaw) - z * math.sin(yaw)
    zz = x * math.sin(yaw) + z * math.cos(yaw)
    x, z = xz, zz
    
    # Z-Axis Rotation (Roll)
    xy = x * math.cos(roll) - y * math.sin(roll)
    yy = x * math.sin(roll) + y * math.cos(roll)
    x, y = xy, yy
    return x, y, z

def render():
    t = 0
    frame = 0
    
    while True:
        # Initialize buffers
        buffer = [' '] * (WIDTH * HEIGHT)
        z_buffer = [-9999] * (WIDTH * HEIGHT)
        
        # --- Animation Math ---
        # Slow float
        float_y = math.sin(t) * 0.5
        
        # Writing motion (Lissajous curve for Figure 8)
        write_x = math.sin(t * 1.5) * 1.5
        write_z = math.cos(t * 3.0) * 0.5 # Depth movement
        
        # Rotations to make it look like a pen held in a hand
        base_pitch = 2.8  # Tilted ~45 degrees
        base_yaw = t * 0.4 # Slow spin to show off the 3D model
        base_roll = 0.3
        
        # --- Geometry Generation ---
        # Density: Steps for height (i) and circumference (j)
        for i in range(180): 
            h = i / 180.0 # Normalized height 0.0 to 1.0
            
            for j in range(24):
                theta = j * (2 * math.pi) / 24
                
                # Get Object Space
                ox, oy, oz, nx, ny, nz = get_pen_geometry(h, theta)
                
                # Apply Rotation
                rx, ry, rz = rotate(ox, oy, oz, base_pitch, base_roll, base_yaw)
                rn_x, rn_y, rn_z = rotate(nx, ny, nz, base_pitch, base_roll, base_yaw)
                
                # Apply Translation (World Space)
                rx += write_x
                ry += float_y
                rz += 8.0 + write_z # Move camera back
                
                # Perspective Projection
                fov = 1 / rz
                
                # Screen Coordinates
                sx = int(WIDTH / 2 + (SCALE * 2.0) * rx * fov)
                # Note: Multiply Y by 0.55 to account for terminal character aspect ratio (pixels are rectangular)
                sy = int(HEIGHT / 2 - (SCALE * 1.0) * ry * fov)
                
                # Lighting
                # Light source vector
                lx, ly, lz = 0.5, -1, -0.5
                # Normalize light
                lm = math.sqrt(lx*lx + ly*ly + lz*lz)
                lx /= lm; ly /= lm; lz /= lm
                
                # Dot product
                illumination = rn_x*lx + rn_y*ly + rn_z*lz
                
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    idx = sx + sy * WIDTH
                    
                    # Z-Buffer check
                    if fov > z_buffer[idx]:
                        z_buffer[idx] = fov
                        
                        # Calculate luminance index
                        if illumination > 0:
                            lum_idx = int(illumination * (len(ASCII_CHARS) - 1))
                            buffer[idx] = ASCII_CHARS[lum_idx]
                        else:
                            buffer[idx] = '.' # Shadow
        
        # --- Render Output ---
        sys.stdout.write("\x1b[H") # Move cursor home
        
        # Construct frame string
        output = []
        for k in range(HEIGHT):
            output.append("".join(buffer[k*WIDTH : (k+1)*WIDTH]))
            
        sys.stdout.write("\n".join(output))
        sys.stdout.flush()
        
        t += 0.05 * SPEED
        time.sleep(0.03)

if __name__ == "__main__":
    # Hide cursor (works in most unix terminals)
    sys.stdout.write("\033[?25l")
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        render()
    except KeyboardInterrupt:
        # Show cursor again
        sys.stdout.write("\033[?25h")
        print("\nDone.")