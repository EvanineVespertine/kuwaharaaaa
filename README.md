Yeah, well, I guess I ain't got much to put here, besides what I already put in the discription.
Basically, this is a photo/image filter that kinda sorta turns it into an oil painting.
Since I was only allowed to use matplotlib and barely able to use numpy, I wasn't able to create it to full extent. Oh well.
Below I have posted a full documentation on how I did it. For my source code, just look in the .py file under the main branch.

P. S.: Please don't mind my questionable variable names ;)

Overview

Step 1: Setup and Image Loading
The Imports: We import matplotlib.pyplot for reading/saving the image and numpy for handling the heavy 3D matrix math.

Loading the Array (goatedarray): The target image (inp.jpg) is converted into a 3D NumPy array consisting of Height, Width, and Color Channels.

Creating a Working Copy: A copy (changeable) is immediately created and cast to float to prevent any read-only errors during mathematical manipulation.

Step 2: User Interaction & Validation
Dynamic Radius (r): Instead of hardcoding the brush size, the script asks the user to define the intensity of the oil painting effect.

Input Validation: A while loop acts as a safeguard. If the user inputs a radius less than 1 or greater than 10 (which would either crash the script or cause massive rendering lag), the terminal prompts them to retry until a valid integer is provided.

Step 3: Data Cleaning and Matrix Padding
Alpha Channel Purge: goatedarray = goatedarray[:, :, :3] forcefully drops any invisible 4th Alpha channel data, ensuring the variance math is strictly dealing with Red, Green, and Blue values.

Building the Bumper (padified): np.pad builds a protective border around the entire image. The thickness of this border matches the user's radius (r). We use mode='edge' to duplicate the outermost pixels, preventing black borders from skewing the color math.

Step 4: The Core Kuwahara Logic (Pass 1)
An empty canvas (frstrounded) is created to hold the new pixels. The script then iterates through every single y (row) and x (column) of the original image dimensions.

For every pixel, the following sequence occurs:

Coordinate Shifting: The algorithm adjusts the (y, x) coordinates by + r to match the shifted dimensions of the padified array.

Quadrant Slicing: Four distinct overlapping squares are carved out around the center pixel:

tl (Top-Left)

tr (Top-Right)

bl (Bottom-Left)

br (Bottom-Right)

Variance Calculation (notnices): np.var() measures how chaotic or "noisy" the RGB colors are inside each of the four quadrants.

Mean Calculation (avs): np.mean() collapses the 3D grid of each quadrant to find its average flat Red, Green, and Blue color.

The Winner Takes All: np.argmin() identifies which quadrant has the lowest variance (the "smoothest" area). The average color of that winning quadrant is assigned to the (y, x) coordinate on the frstrounded output canvas.

Step 5: The Interactive Smoothing Pass (Pass 2)
Because the standard Kuwahara uses rigid squares, the output can look blocky. The script pauses and asks the user if they want to run a smoothing round (Yes/No).

If "Yes":

A second empty canvas (scndrounded) is generated.

The blocky frstrounded matrix is padded with a tiny radiusblur = 1 bumper.

The script runs a fast 3x3 Box Blur algorithm: it looks at a 3x3 window around every pixel, averages all 9 colors together, and paints that blended color onto scndrounded.

The script prints a highly necessary success message ("Smoothing complete y'all ungrateful uglies.") and saves the blurred image as outp.jpg.

If "No" (or anything else):

The script skips the blur logic entirely and instantly saves the raw, blocky frstrounded matrix as outp.jpg.
