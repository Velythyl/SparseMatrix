"""
Auteure: Charlie Gauthier
Matricule: 20105623
Date: septembre 25 2015
"""


class SparseMatrix:
    def __init__(self, fromiter, shape):
        n, m = shape
        self.n = n
        self.m = m

        self.nnz = len(fromiter)
        self.rowptr = []  # liste de taille n + 1 des intervalles des colonnes
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        triplets = fromiter.sorted()  # on sait que les triplets sont en ordre de rangee maintenant

        self.rowptr.append(0)
        nb_on_row = 0
        last_row = 0

        for triplet in triplets:
            # Peu importe ce qui se passe, on sait que chaque triplet n'est pas 0.
            # Donc, on ajoute triplet[1] et triplet[2] a colind et data (respectivement) peu importe la valeur
            #  de triplet[0]

            self.colind.append(triplet[1])  # On ajoute l'index de cet element au colind
            self.data.append(triplet[2])  # On ajoute la valeur de l'element a data

            if last_row == triplet[0]:
                # Si on est sur le meme row que le dernier triplet:
                nb_on_row += 1  # On incremente simplement le nombre de valeurs sur le row

            else:
                # Sinon, on doit assumer qu'on change de row
                # Donc, ajouter:
                #  le nombre d'elements sur le row precedent + le nombre de row avant celui-ci au rowptr
                # Assigner le nouveau row a last_row
                # Remettre nb_on_row a 0. Mais! Ce triplet existe, donc on a pour sur au moins un element sur le row.
                #  Donc, on assigne 1 a nb_on_row.

                self.rowptr.append(self.rowptr[-1] + nb_on_row)     # On ajoute le rowptr du row precedent

                last_row = triplet[0]   # On prend la valeur du nouveau row
                nb_on_row = 1           # On sait qu'il y a au moins ce triplet comme valaur non-nulle sur ce row

    def __getitem__(self, k):       # TODO donc seulement retourne la diagonale????
        i, j = k
        # TODO: retourner la valeur correspondant à l'indice (i, j)

    def todense(self):
        # TODO: encoder la matrice en format dense
        pass
