import matplotlib.pyplot as plt
import numpy as np

goatedarray = plt.imread('inp.jpg') #convert to array with width, hight and rgb channels
changeable = np.copy(goatedarray).astype(float) #make copy to modify


#space for mah math
r = int(input("Enter brush size (recommended around 2-8): ")) #brushstroke radius
while (r < 1 or r > 10):
    print("Value out of range of niceness, retry.")
    r = int(input("Enter brush size (recommended around 2-8): ")) 

goatedarray = goatedarray[:, :, :3] #removed fourth "a" channel
#print(f"Original shape: {goatedarray.shape}")
padified = np.pad(goatedarray, ((r, r), (r, r), (0, 0)), mode = 'edge') #add padded version
#print(f"Padded shape: {padified.shape}")



frstrounded = np.zeros_like(goatedarray) #finally written result here

#Get original height/width
height, width = goatedarray.shape[:2]

for y in range(height):
    for x in range(width):
        
        # In the padded array ->current pixel's actual center is shifted by r
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
    plt.imsave('outp.jpg', frstrounded) #save directly after first pass


