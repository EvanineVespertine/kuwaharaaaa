#Self warning: Make sure the thing is directed into the CORRECT GODDAMN FOLDER GOOD GRIEF
'''So I have finally completed my wonderful kuwahara filter to a certain extent.
I must say that for a filter of such mathematical complexity, I am satisfied with the result.
All the further things I do to this filter will just be minor improvements. Something I learned is,
that the smoothing really does give an extra paintstroke effect, I feel like before I was kind of 
not trusting it to be of any use. Also, this thing with downscaling the image when it's large is really
extremely useful, without it, the user either has to put up with a rediculous runtime, 
or decide themself if they think their image is large (which no normal human really wants to do.). And
now we are at a nice point where the filter doesn't take forever on large images (some time, yes,
but not infinetly long) and works nicely with the smoothing round. So long for now, and my next challenge
shall be the Anisotropic Kuwahara. Wish me luck ;) !'''

import matplotlib.pyplot as plt
import numpy as np

goatedarray = plt.imread('inp.jpg') #convert to array with width, hight and rgb channels
changeable = np.copy(goatedarray).astype(float) #make copy to modify
chk = np.max(changeable)
if chk > 1.0:
   changeable = changeable/255.0 

#print("max=", np.max(changeable))
#print("min=", np.min(changeable))

#space for mah math
r = int(input("Enter brush size (recommended around 2-8): ")) #brushstroke radius
while (r < 1 or r > 10):
    print("Value out of range of niceness, retry.")
    r = int(input("Enter brush size (recommended around 2-8): ")) 

if len(changeable.shape) >= 3:
    changeable = changeable[:, :, :3] #removed fourth "a" channel if necessary and not a black white photo

rawheight, rawwidth = changeable.shape[:2]
total_pixels = rawheight * rawwidth

print(f"\nLoaded image with {total_pixels:,} pixels.")

#Make sure the image doesn't overload mah poor cpu
if total_pixels < 500_000:
    scale = 1
    print("You picked a small ahh image. Running at full resolution.")
elif total_pixels < 3_000_000:
    scale = 2
    print("Your image is a little fat. Slicing by 2 for the sake of my CPU.")
elif total_pixels < 10_000_000:
    scale = 3
    print("That's a fat ahh pic. Imma have to slice it by 3 'cuz its gonna be a while otherwise.")
else:
    scale = 4
    print("What's that, a full petabyte? Slicing by 4 if you wanna see your image in this lifetime.")

changeable = changeable[::scale, ::scale] #then actually remember to slice it sheesh

#print(f"Original shape: {goatedarray.shape}")
padified = np.pad(changeable, ((r, r), (r, r), (0, 0)), mode = 'edge') #add padded version
#print(f"Padded shape: {padified.shape}")



frstrounded = np.zeros_like(changeable) #finally written result here

#Get original height/width
height, width = changeable.shape[:2]

for y in range(height):
    for x in range(width):
        
        #In the padded array ->current pixel's actual center is shifted by r
        cy, cx = y + r, x + r
        
        #time to sliceeee
        #Numpy slicing is [start_y : end_y, start_x : end_x]
        #!!!Remember the end index in py slicing is exclusive, so +1 to include the center pixel!!! 
        
        tl = padified[cy - r : cy + 1, cx - r : cx + 1] #topleft
        tr = padified[cy - r : cy + 1, cx : cx + r + 1] #topright
        bl = padified[cy : cy + r + 1, cx - r : cx + 1] #bottomleft
        br = padified[cy : cy + r + 1, cx : cx + r + 1] #bottomright

        notnices = [  #calculate variance
            np.var(tl),
            np.var(tr),
            np.var(bl),
            np.var(br)
        ]

        avs = [ #calculate averagbe
            np.mean(tl, axis = (0, 1)),
            np.mean(tr, axis = (0, 1)),
            np.mean(bl, axis = (0, 1)),
            np.mean(br, axis = (0, 1))
        ]

        bestquad = np.argmin(notnices)

        frstrounded[y, x] = avs[bestquad]

scnd = input("Kuwahara finished. \n" "Smoothing round? (Yes/No): ")

if (scnd == "Yes"):
    radiusblur = 1 #A radius of 1 creates a 3x3 window
    scndrounded = np.zeros_like(frstrounded)

    #Pad the blocky kuwahara output so we can blur the edges
    blurpadding = np.pad(frstrounded, ((radiusblur, radiusblur), (radiusblur, radiusblur), (0, 0)), mode = 'edge')

    for y in range(height):
        for x in range(width):
            cy, cx = y + radiusblur, x + radiusblur #Shift coordinates for the padded array
            window = blurpadding[cy - radiusblur : cy + 2, cx - radiusblur : cx + 2] #Carve out a 3x3 window around pixel
            scndrounded[y, x] = np.mean(window, axis = (0, 1)) #Average surrounding pixes and paint it to the final thing
    print("Smoothing complete y'all ungrateful uglies.")
    plt.imsave('outp.jpg', scndrounded) #save basically yeah
else: 
    print("That's all ya get then.")
    plt.imsave('outp.jpg', frstrounded) #save directly after first pass
