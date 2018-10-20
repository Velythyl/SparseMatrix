import numpy as np
import gc
from sparse import *

mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))


# QUESTION 2...

# Retourne les triplets des elements non-nuls d'un bitmap 2D
def bitmap_to_triplets(bitmap):
    triplets = np.transpose(np.nonzero(bitmap))  # Prends les couples non-nuls et les agence en x, y
    triplets = triplets.tolist()    # On cast en une liste de listes
    for triplet in triplets:        # Pour chaque couple de coordonnee
        x, y = triplet
        triplet.append(bitmap[x][y])  # On va chercher sa valeur et on l'ajoute pour faire des triplets

    return triplets  # On retourne la liste de triplets


# Retourne une nouvelle SparseMatrix d'apres un bitmap 2D
def bitmap_to_sparse(bitmap, shape):
    return SparseMatrix(bitmap_to_triplets(bitmap), shape)


first_image = mnist_dataset[0].tolist()  # first_image est de taille (28, 28)

# Transformation en matrice eparse
sparse = bitmap_to_sparse(first_image, (28, 28))

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

gc.collect()

# QUESTION 4 ET 5 ....
tridbitmap = mnist_dataset.tolist()

quads = (np.transpose(np.nonzero(mnist_dataset))).tolist()  # Prends les couples non-nuls et les agence en z, x, y
for quad in quads:  # Pour chaque triplet de coordonnee
    z, x, y = quad
    quad.append(tridbitmap[z][x][y])  # On va chercher sa valeur et on lui ajoute pour faire un quad

mnist_dataset = None    # On l'a encore dans tridbitmap, sous forme de listes de listes au lieu d'array Numpy
gc.collect()

tensor = SparseTensor(quads, (60000, 28, 28))

# QUESTION 5b
print("nb of nb SparseTensor (nombre de valeurs enregistrees):", tensor.get_nb_of_nb())
print("nb of nb tensor original (nombre de valeurs enregistrees):", 60000*28*28)

tensordense = tensor.todense()

tensor = None
quads = None
gc.collect()

# QUESTION 4b: Comparaison pixel par pixel
try:
    if sorted(tridbitmap) != sorted(tensordense):
        raise AssertionError

    print("Assertion question 5 reussie")
except AssertionError:
    print("Assertion question 5 echouee")
