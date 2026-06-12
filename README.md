Yeah, well, I guess I ain't got much to put here, besides what I already put in the discription.
Basically, this is a photo/image filter that kinda sorta turns it into an oil painting.
Since I was only allowed to use matplotlib and barely able to use numpy, I wasn't able to create it to full extent. Oh well.
Below I have posted a full documentation on how I did it. For my source code, just look in the .py file under the main branch.

P. S.: Please don't mind my questionable variable names ;)

P. S. S.: Had to change this to be accurate again because I updated my code.

Here I have written a story for all of you called the Kuwahara Quest


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

> 10M pixels: What's that, a full petabyte? The array is violently smooshed to a quarter of its size (scale = 4) so you actually get to see your output before you die.

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

So yeah, that's all ya get. Hope you had fun reading!
