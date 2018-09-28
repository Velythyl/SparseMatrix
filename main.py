import numpy as np
import matplotlib.pyplot as plt
from sparse import *

import sys

mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))


# QUESTION 2...

# Retourne les triplets des elements non-nuls d'un bitmap 2D
def bitmap_to_triplets(bitmap):
    triplets = np.transpose(np.nonzero(bitmap))  # Prends les couples non-nuls et les agence en x, y
    triplets = triplets.tolist()  # On cast en une liste de listes
    for triplet in triplets:  # Pour chaque couple de coordonnee
        x, y = triplet
        triplet.append(bitmap[x][y])  # On va chercher sa valeur et on lui ajoute

    return triplets  # On retourne la liste de triplets


# Retourne une nouvelle SparseMatrix d'apres un bitmap 2D
def bitmap_to_sparse(bitmap, shape):
    return SparseMatrix(bitmap_to_triplets(bitmap), shape)


first_image = mnist_dataset[0].tolist()  # first_image est de taille (28, 28)
# plt.imshow(first_image, cmap='gray_r')
# plt.show()

# Transformation en matrice eparse
sparse = bitmap_to_sparse(first_image, (28, 28))

# plt.imshow(sparse.todense(), cmap='gray_r')  # Oui, identique a l'oeil!
# plt.show()

# test pixel par pixel
try:
    if sorted(first_image) != sorted(sparse.todense()):
        raise AssertionError

    print("Assertion question 2 reussie")

except AssertionError:
    print("Assertion question 2 echouee")

# ...FIN QUESTION 2

# liberer memoire
sparse = None
first_image = None

# QUESTION 4 ....


# Retourne les quads des elements non-nuls d'un set de bitmap
def bitmap_to_quads(bitmap):
    quads = np.transpose(np.nonzero(bitmap))  # Prends les couples non-nuls et les agence en z, x, y
    quads = quads.tolist()  # On cast en une liste de listes

    for quad in quads:  # Pour chaque triplet de coordonnee
        z, x, y = quad
        quad.append(bitmap[z][x][y])  # On va chercher sa valeur et on lui ajoute

    return quads  # On retourne la liste de quads


# Retourne un SparseTensor a partir d'un set de bitmaps
def bitmap_to_tensor(bitmap, shape):
    return SparseTensor(bitmap_to_quads(bitmap), shape)


tridbitmap = mnist_dataset.tolist()

prof = 10  # Pas assez de ram pour faire les 60 000

tridbitmap = tridbitmap[:prof]  # Donc on prend une tranche des 60 000

tensortodense = bitmap_to_tensor(tridbitmap, (prof, 28, 28)).todense()

# Comparaison pixel par pixel
try:
    if sorted(tridbitmap) != sorted(tensortodense):
        raise AssertionError

    print("Assertion question 5 reussie")
except AssertionError:
    print("Assertion question 5 echouee")
