Yeah, well, I guess I ain't got much to put here, besides what I already put in the discription.
Basically, this is a photo/image filter that kinda sorta turns it into an oil painting.
Since I was only allowed to use matplotlib and barely able to use numpy, I wasn't able to create it to full extent. Oh well.
Below I have posted a full documentation on how I did it. For my source code, just look in the .py file under the main branch.
However, for a more serious, step-by-step explanation, jump directly to line 100. Here, everything is explained clearly.

P. S.: Please don't mind my questionable variable names ;)

P. S. S.: Had to change this to be accurate again because I updated my code.

Here I have written a story for all of you called the Kuwahara Quest

________________________________________________________________________________________________________________________________________________________________________
THE GREAT KUWAHARA QUEST

Prologue: The Dark Ages (A Brief History of Our Suffering)
Before we had the glorious, optimized engine of today, the prototype phase was a lawless wasteland. If future developers read this, know that we bled to get here.

The Ghost Image Era: We initially tried to feed it PNGs (ikr stupid). Matplotlib laughed in our faces, divided everything by 255, and handed us back digital ghosts and pure white canvases because a 0.0039 opacity is mathematically pitch black, yay.

The FileNotFound Crisis: Python gaslit us into thinking our files didn't exist, when in reality, our terminal was just chilling in a parent directory. Always check your working directory.
It hides strange secrets. And check it well, 'cuz I did check it and still didn't see it. Perhaps I'm just blind.

The 4th Channel of Doom: We realized PNGs carry a cursed "Alpha" channel that absolutely nukes variance math.

But we survived. And out of the ashes, this script was born.

CHAPTER 0
Initializing the goatedarray
The script kicks off by dragging my chosen image (inp.jpg) into the Python realm and converting it into a 3D NumPy matrix (Height x Width x RGB Colors).

Because we don't want to accidentally corrupt our original data, we immediately spawn changeable, a perfect clone cast as a float so we have room to do heavy decimal math without breaking the integers.

Next, we establish the Brush Size (r). We politely ask the user for a radius between 2 and 8. If they act up and enter a 12, the while loop essentially calls them an idiot ("Value out of range of niceness") and traps them until they pick a valid number.

Sanity Check: We forcefully strip away that cursed 4th Alpha channel with changeable[:, :, :3], just in case a stray PNG wanders into the code.

CHAPTER 1
The Save My CPU Diet Plan
Pure Python for loops are known to be sluggish. If you were to drop a raw, uncompressed 16-megapixel photo straight outa your files a into this matrix, your computer would kinda melt trying to calculate the variance of 15 million pixels.

To prevent spontaneous combustion, the script calculates the total_pixels (usually hate this kind of snake_case but once, in I while, I am allowed to make exceptions, right?) and puts the image on a forced "diet":

< 500k pixels: Small ahh image. It runs raw and unfiltered (scale = 1).

< 3M pixels: A little fat. The array is mathematically sliced in half (scale = 2).

< 10M pixels: Fat ahh pic. The array is sliced by 3.

smaller than 10M pixels: What's that, a full petabyte? The array is violently smooshed to a quarter of its size (scale = 4) so you actually get to see your output before you die.

CHAPTER 2
Building the Bumper Cars
If you look for a 5x5 window around a pixel at the literal edge of the image (0, 0), Python will look into the void, panic, and crash (as we know our computers).

To fix this, we create padified. We use np.pad to build a protective bumper around the entire image. The thickness of this border matches your brush radius (r). We use mode = 'edge' so it duplicates the outer pixels instead of slapping a black frame around the image, which would ruin the color math (or any other math).

CHAPTER 3
The Meat & Potatoes
We generate an empty void called frstrounded to hold our final masterpiece. Then, the nested Y and X for loops begin their march across every single pixel of the original image dimensions.

For every pixel, the algorithm does the following:

-> Shifts Coordinates: It looks at cy, cx (center Y, center X) inside the bigger, padified array so we don't hit the walls.

-> Slices the Quadrants: It carves out four distinct squares around that center point: Top-Left (tl), Top-Right (tr), Bottom-Left (bl), and Bottom-Right (br).

-> Calculates Chaos (notnices): Using np.var(), it calculates the variance. This tells us exactly how "noisy" or chaotic the colors are inside each of those four boxes.

-> Calculates Averages (avs): Using np.mean(), it squishes the 3D grid down to find the average, flat Red, Green, and Blue color of each box.

Paints the Pixel: np.argmin finds the index of the quadrant with the lowest variance (the smoothest, least chaotic patch of color). It grabs that winning quadrant's average color from avs and slaps it onto our frstrounded canvas.

CHAPTER 4
The Smoothing Pass for y'all ungratefull uglies.
Because standard Kuwahara relies on perfectly rigid mathematical squares, the output can look like it was built in Minecraft (I've never played btw, yeah ikr, crazy sht). The script pauses and asks the user if they want a smoothing round.

If "Yes":

We define radiusblur = 1, which creates a microscopic 3x3 window.

We pad the blocky frstrounded image again, creating blurpadding.

We loop over the image again, looking at that tiny 3x3 window for every pixel, averaging all 9 colors together, and writing it to scndrounded. This acts like a wet brush, melting the harsh 90-degree corners into fluid, buttery oil paint strokes.

The script insults the user  and saves the final file to outp.jpg.

If "No" (or literally anything else):

"That's all ya get then."

It skips the blur and saves the chunky, blocky, first-pass matrix to outp.jpg.



✩ VOILÀ THE END ✩

____________________________________________________________________________________________________________________________________________________________________

The core concept to remember is that a digital image is just a massive grid of numbers. Each pixel is represented by a list of three values: Red, Green, and Blue (RGB). This script uses standard programming logic to manipulate those numbers.

Phase 1: Setup and Data Preparation
Before the main logic begins, the script must load the image and convert its data into a format that is safe for mathematical operations.

1. Importing Libraries
The script uses matplotlib.pyplot to read and save image files, and numpy to handle the grid of numbers. numpy is essentially a highly optimized tool for working with complex, multi-dimensional lists.

2. Loading and Normalizing the Image

Python
goatedarray = plt.imread('inp.jpg') 
changeable = np.copy(goatedarray).astype(float) 
chk = np.max(changeable)
if chk > 1.0:
   changeable = changeable/255.0 
What it does: It reads the image into a 3-dimensional grid (Height, Width, RGB Colors). It then creates a copy and converts all the numbers into decimals (float). Finally, it checks the highest number in the grid. If the numbers range from 0 to 255, it divides everything by 255 to force the numbers into a scale of 0.0 to 1.0.

Why we do this: Mathematical functions like calculating averages or variance are much more precise when using decimals. Furthermore, image saving tools expect colors to be strictly formatted between 0.0 and 1.0. If we skip this division, the output image will likely appear as a solid white canvas due to the numbers being too high.

3. User Input and Validation

Python
r = int(input("Enter brush size (recommended around 2-8): ")) 
while (r < 1 or r > 10):
    print("Value out of range of niceness, retry.")
    r = int(input("Enter brush size (recommended around 2-8): ")) 
What it does: It asks the user to define r (the radius), which determines the size of the "brush." A while loop ensures the user enters a number between 1 and 10.

Why we do this: If a user inputs a massive number (like 50), the mathematical area it has to check for every single pixel becomes too large, which will freeze the computer. The while loop acts as a safety barrier.

4. Cleaning the Data

Python
if len(changeable.shape) >= 3:
    changeable = changeable[:, :, :3] 
What it does: It uses list slicing to keep all rows and all columns, but strictly only the first three color channels (Red, Green, Blue).

Why we do this: Some image formats (like PNGs) have a fourth channel for transparency (Alpha). If the algorithm attempts to calculate the variance of four channels instead of three, the resulting math will be skewed, or the program will crash.

Phase 2: Performance Optimization (Downsampling)
Python for loops process items one at a time. If an image is 4000 pixels wide and 3000 pixels tall, the loops must process 12 million pixels.

1. Resolution Scaling

Python
rawheight, rawwidth = changeable.shape[:2]
total_pixels = rawheight * rawwidth

if total_pixels < 500_000:
    scale = 1
elif total_pixels < 3_000_000:
    scale = 2
elif total_pixels < 10_000_000:
    scale = 3
else:
    scale = 4

changeable = changeable[::scale, ::scale] 
What it does: It calculates the total number of pixels. Depending on the size, it assigns a scale multiplier. The script then slices the grid using [::scale, ::scale]. If scale = 2, the slice skips every other pixel, effectively shrinking the image by half in both directions.

Why we do this: This prevents the program from running for hours on modern, high-resolution photographs. By sacrificing a small amount of visual detail and shrinking the grid before the loops start, processing time is reduced from hours to seconds.

Phase 3: The Kuwahara Algorithm
This is the core logic. To create the "oil painting" effect, the algorithm calculates which neighboring area around a pixel is the "smoothest," and paints the pixel that solid color.

1. The Padding Bumper

Python
padified = np.pad(changeable, ((r, r), (r, r), (0, 0)), mode = 'edge') 
frstrounded = np.zeros_like(changeable) 
What it does: np.pad builds a border of extra pixels around the outside of the image. The thickness of this border matches the brush radius (r). It then creates a blank canvas (frstrounded) composed of zeros, ready to hold the final output.

Why we do this: If the loop looks at a pixel on the literal top edge of the image, and tries to check a 5x5 box around it, the code will look "outside" the grid and crash. Padding adds a safe border so the brush never hits an edge.

2. The Main Loop and Slicing

Python
for y in range(height):
    for x in range(width):
        cy, cx = y + r, x + r
        
        tl = padified[cy - r : cy + 1, cx - r : cx + 1] 
        tr = padified[cy - r : cy + 1, cx : cx + r + 1] 
        bl = padified[cy : cy + r + 1, cx - r : cx + 1] 
        br = padified[cy : cy + r + 1, cx : cx + r + 1] 
What it does: The nested for loops systematically visit every x and y coordinate. For each pixel, it carves out four smaller, overlapping grids (Top-Left, Top-Right, Bottom-Left, Bottom-Right).

Why we do this: These four regions represent the possible "brush strokes" for that specific pixel.

3. The Mathematics of Smoothing

Python
        notnices = [np.var(tl), np.var(tr), np.var(bl), np.var(br)]
        avs = [np.mean(tl, axis=(0, 1)), np.mean(tr, axis=(0, 1)), ...]
        bestquad = np.argmin(notnices)
        frstrounded[y, x] = avs[bestquad]
What it does: * np.var() calculates the variance of the colors in each quadrant. (Variance is a mathematical measurement of chaos. An area with high detail, like grass, has high variance. A clear blue sky has low variance).

np.mean() calculates the average RGB color of each quadrant.

np.argmin() finds which of the four quadrants has the lowest variance score.

Finally, it takes the average color of that winning, lowest-variance quadrant and paints it onto the new canvas at the [y, x] location.

Why we do this: By always picking the smoothest neighboring patch of color and expanding it, sharp lines (like the edge of a mountain against the sky) are preserved, but fine textures (like individual rocks) are blurred into solid "paint" blobs.

Phase 4: The Optional Box Blur
Because the Kuwahara filter uses perfect squares to check variance, the resulting "paint blobs" can look blocky, pixelated, or unnatural.

Python
if (scnd == "Yes"):
    radiusblur = 1 
    scndrounded = np.zeros_like(frstrounded)
    blurpadding = np.pad(frstrounded, ((radiusblur, radiusblur), ...))

    for y in range(height):
        for x in range(width):
            cy, cx = y + radiusblur, x + radiusblur 
            window = blurpadding[cy - radiusblur : cy + 2, cx - radiusblur : cx + 2] 
            scndrounded[y, x] = np.mean(window, axis = (0, 1)) 
What it does: If the user agrees, the script creates another blank canvas and pads the newly painted image. It runs a new, slightly different loop. This time, it looks at a tiny 3x3 window around every pixel, takes all 9 colors inside that window, averages them together into one mixed color, and paints it.

Why we do this: A box blur acts exactly like dragging a wet brush over drying oil paint. Averaging local pixels softens the harsh, 90-degree blocky corners created by the first algorithm, resulting in organic, flowing shapes.

So yeah, that's all ya get. Hope you had fun reading!
