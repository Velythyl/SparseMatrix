import numpy as np
import matplotlib.pyplot as plt
from sparse import *

import sys

print(sys.version)

mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))

# QUESTION 2...

def bitmap_to_triplets(bitmap):
    # Retourne les triplets des elements non-nuls d'un bitmap
    triplets = np.transpose(np.nonzero(bitmap))  # Prends les couples non-nuls et les agence en x, y
    triplets = triplets.tolist()  # On cast en une liste de listes
    for triplet in triplets:  # Pour chaque couple de coordonnee
        x, y = triplet
        triplet.append(bitmap[x][y])  # On va chercher sa valeur et on lui ajoute

    return triplets  # On retourne la liste de triplets

def bitmap_to_sparse(bitmap, shape):
    # On retourne une nouvelle SparseMatrix. On doit avoir la liste de triplets representant le bitmap.
    return SparseMatrix(bitmap_to_triplets(bitmap), shape)


first_image = mnist_dataset[0].tolist()  # first_image est de taille (28, 28)
#plt.imshow(first_image, cmap='gray_r')
#plt.show()

# Transformation en matrice eparse
sparse = bitmap_to_sparse(first_image, (28, 28))

#plt.imshow(sparse.todense(), cmap='gray_r')  # Oui, identique a l'oeil!
#plt.show()

# test pixel par pixel
print("Est-ce que ces matrices sont egales?:", sorted(first_image) == sorted(sparse.todense()))

# ...FIN QUESTION 2

sparse = None
first_image = None

# QUESTION 4 ....

def bitmap_to_quads(bitmap):
    # Retourne les triplets des elements non-nuls d'un bitmap
    quads = np.transpose(np.nonzero(bitmap))  # Prends les couples non-nuls et les agence en x, y
    quads = quads.tolist()  # On cast en une liste de listes

    for quad in quads:  # Pour chaque couple de coordonnee
        z, x, y = quad
        quad.append(bitmap[z][x][y])  # On va chercher sa valeur et on lui ajoute

    return quads  # On retourne la liste de triplets

def bitmap_to_tensor(bitmap, shape):
    return SparseTensor(bitmap_to_quads(bitmap), shape)

try:
    tridbitmap = mnist_dataset.tolist()

    prof = 10   # Pas assez de ram pour faire les 60 000

    tridbitmap = tridbitmap[:prof]

    tensortodense = bitmap_to_tensor(tridbitmap, (prof, 28, 28)).todense()

    if sorted(tridbitmap) != sorted(tensortodense):
        raise AssertionError

    print("Assertion reussie")
except AssertionError:
    print("Assertion echouee")
