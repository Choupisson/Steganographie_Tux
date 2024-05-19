import numpy as np     		# multi-dimensional arrays
from PIL import Image  		# images
import matplotlib.pyplot as plt # used to display a matrix as an image

#-------------------------------------------------
# Utility functions for images.
#
# An image is represented as a 3-dimensional array of unsigned
# integers. The 3 dimensions represent:
# - the image columns (size: the image width in pixels)
# - the image lines (size: the image height in pixels)
# - the pixels (3 unsigned integers representing the RGB values)
#-------------------------------------------------

#-------------------------------------------------
# Read an image from a file and return a 3-dimensional array of
# unsigned integers.
#
# input:
#   filename: the name of the image file to be read
#
# output:
#   a 3-dimensional array of unsigned integers representing the image
#-------------------------------------------------
def read_img(filename):
    
    img = Image.open(filename)
    
    # get a read-only array of the image
    try:
        pixels = np.asarray(img, dtype='uint8')
    except SystemError:
        pixels = np.asarray(img.getdata(), dtype='uint8')

    # make the image writable
    # pixels.setflags(write=1)

    return pixels


#-------------------------------------------------
# Convert a 3-dimensional array of integers to an image and write it
# to a file.
#
# input:
#   filename: the name of the file where the image should be written
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#-------------------------------------------------
def write_img(filename, pixels):
    img = Image.fromarray(pixels)
    img.save(filename)

#-------------------------------------------------
# Make a 3-dimensional array of integers to represent an image having
# the given dimensions.
#
# input:
#   width: the image width in pixels
#   height: the image height in pixels
#
# output:
#   a 3-dimensional array of unsigned integers a black image (all
#   pixels are zeros)
#-------------------------------------------------
def empty_img(width, height):
    return np.zeros((width, height, 3), dtype='uint8')

#-------------------------------------------------
# Give the width in pixels of an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   width: the image width in pixels
#-------------------------------------------------
def get_width(pixels):
    return np.shape(pixels)[0]

#-------------------------------------------------
# Give the height in pixels of an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   height: the image height in pixels
#-------------------------------------------------
def get_height(pixels):
    return np.shape(pixels)[1]

#-------------------------------------------------
# Display an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   the image displayed
#-------------------------------------------------
def display_img(pixels):
    plt.imshow(pixels)
    plt.axis('off')  # Pour ne pas afficher les axes
    plt.show()


#- - - -- - -- --- - -- - - - -- - -- - - - -- - 
def convertion_gris(pixels):
    grey_scale = 0.299*pixels[:,:,0]+0.587*pixels[:,:,1] + 0.114 * pixels[:,:,2]
    grey_pixels = np.repeat(grey_scale[:, :, np.newaxis], 3, axis=2).astype('uint8')
    return grey_pixels


def save_img(pixels, output_filename):
    img = Image.fromarray(pixels)
    img.save(output_filename)



def rotate_image(pixels, angle):
    # Vérification du type d'angle
    if angle not in [-90, 90]:
        raise ValueError("L'angle doit être -90 ou 90.")
    
    # Obtenir les dimensions de l'image
    height,width,channels = pixels.shape
    # Création d'une nouvelle image pour stocker les pixels tournés
    rotated_pixels = np.zeros((width, height, channels), dtype='uint8')

    for i in range(height):
        for j in range(width):
            if angle == 90:
                rotated_pixels[j, height-i-1] = pixels[i,j]
            else:  # -90 degree rotation
                rotated_pixels[width-j-1,i] = pixels[i,j]
    return rotated_pixels



#METHODE PLUS SIMPLE (j'ai refais la version ci-dessus car je n'étais pas sûr de si on avait le droit d'utiliser .rotate() ):
# def rotate_image(filename, angle):
#     img = Image.open(filename)
    
#     if angle == 90:
#         rotated = img.rotate(-90)
#     elif angle == -90:
#         rotated = img.rotate(90)
#     else:
#         print("Problème au niveau de la rotation")
#         return

#     output_filename = "rotation_" + str(angle) + "_" + filename
#     rotated.save(output_filename)
#     rotated.show()


#Fonction pour cacher l'information, fonction d'encodage qui convertit un message en une liste de valeurs numériques
#Comme dans l'exemple du prof -> A=0,...,Z=25
def message_encodage(message):
    values=[]
    for char in message.upper():
        if 'A'<= char <= 'Z': # On vérifie que le caractère est une lettre de l'alphabet
            values.append(ord(char)-ord('A')) # Convertit le caractère en une valeur numérique
    return values

#Fonction qui cache un message dans l'image voulu en modifiant les pixels d'une image
def cacher(image,message):
    values = message_encodage(message) #Convertit le message en valeurs numériques
    image_modifier=image.copy() #Créer une copie pour agir sur celle-ci
    width,height,_=image_modifier.shape

    if len(values) > width*height: #ici on vérifie la taille du message au cas où
        raise ValueError("Le message est trop long")
    
    for i,value in enumerate(values):
        x,y = i // height, i %height
        image_modifier[x,y,0]+= value # Modifie la composante rouge du pixel pour cacher une valeur du message
    return image_modifier


# Fonction qui retourne le message caché d'une image modifiée
def extraire_message(image_origin, image_modifier, message_length):
    valeur_extraite = []

    width, height, _ = image_origin.shape
    for i in range(message_length):
        x, y = i // height, i % height
        diff = image_modifier[x, y, 0] - image_origin[x, y, 0] # Calcule la différence de la composante rouge
        valeur_extraite.append(diff)

    # Convertit les valeurs numériques extraites en un message
    message = ''.join([chr(value + ord('A')) for value in valeur_extraite])
    return message


######################################################
##################  Test  ############################
######################################################

#Q1#

# Chargement de l'image originale:
image = read_img('TUX.png')
display_img(image)

#Conversion en pixel gris:
pixels_gris = convertion_gris(image)
save_img(pixels_gris, 'TUX_Gris.png')
display_img(pixels_gris)

#Q2#
rotated_pixels = rotate_image(image, 90)
rotated_pixels2 = rotate_image(image, -90)
display_img(rotated_pixels)
display_img(rotated_pixels2)


# rotate_image('TUX.png', 90)
# rotate_image('TUX.png',-90)


#Q3#

# Cachage du message
message = "HACK"
pixels_modif = cacher(image, message)

# Sauvegarde de l'image modifiée
write_img('TUX_Modifie.png', pixels_modif)

# Extraction du message
message_extrait = extraire_message(image, pixels_modif, len(message))
print("Message extrait de l'image TUX modifiée:", message_extrait)

# Extraction d'un message nul
message_extrait2 = extraire_message(image,image, len(message))
print("Message extrait de l'image TUX d'origine:", message_extrait2)
#Pour ce cas, la différence de 0 entre l'image d'origine et elle même est de 0,
#Ainsi A = 0, d'où l'obtention de plusieurs A de la taille du message prit
