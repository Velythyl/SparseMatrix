import numpy as np
import matplotlib.pyplot as plt
from sparse import SparseMatrix

def bitmap_to_triplets(bitmap):
    triplets = np.transpose(np.nonzero(bitmap))
    triplets = triplets.tolist()
    for triplet in triplets:
        x, y = triplet
        triplet.append(first_image[x][y])

    return triplets


mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))
first_image = mnist_dataset[0].tolist()     # first_image est de taille (28, 28)
plt.imshow(first_image, cmap='gray_r')
plt.show()

# Transformation en liste de triplets
triplets = bitmap_to_triplets(first_image)

sparse = SparseMatrix(triplets, (28, 28))

plt.imshow(sparse.todense(), cmap='gray_r')
plt.show()

