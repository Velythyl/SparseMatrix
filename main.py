import numpy as np
import matplotlib.pyplot as plt
from sparse import SparseMatrix


def bitmap_to_triplets(bitmap):
    # Retourne les triplets des elements non-nuls d'un bitmap
    triplets = np.transpose(np.nonzero(bitmap))     # Prends les couples non-nuls et les agence en x, y
    triplets = triplets.tolist()                    # On cast en une liste de listes
    for triplet in triplets:                        # Pour chaque couple de coordonnee
        x, y = triplet
        triplet.append(first_image[x][y])           # On va chercher sa valeur et on lui ajoute

    return triplets                                 # On retourne la liste de triplets


# QUESTION 2...

def bitmap_to_sparse(bitmap, shape):
    # On retourne une nouvelle SparseMatrix. On doit avoir la liste de triplets representant le bitmap.
    return SparseMatrix(bitmap_to_triplets(bitmap), shape)


mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))
first_image = mnist_dataset[0].tolist()  # first_image est de taille (28, 28)
plt.imshow(first_image, cmap='gray_r')
plt.show()

# Transformation en matrice eparse
sparse = bitmap_to_sparse(first_image, (28, 28))

plt.imshow(sparse.todense(), cmap='gray_r')  # Oui, identique a l'oeil!
plt.show()

# test pixel par pixel
print("Est-ce que ces matrices sont egales?:", sorted(first_image) == sorted(sparse.todense()))

# ...FIN QUESTION 2
