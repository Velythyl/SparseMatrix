"""
Auteure: Charlie Gauthier
Matricule: 20105623
Date: septembre 25 2015
"""


# Note: j'utilise le duck typing pour verifier le type des arguments et pour verifier si l'appel de fonction est valide

class SparseMatrix:
    def __init__(self, fromiter, shape):
        try:
            n, m = shape
            temp = iter(fromiter)
            if len(fromiter) != 3: raise Exception
        except Exception:
            # mauvais types de fromiter ou shape
            return


        self.n = n
        self.m = m

        self.nnz = len(fromiter)
        self.rowptr = []  # liste de taille n + 1 des intervalles des colonnes
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        fromiter.sort()  # on sait que les triplets sont en ordre de rangee maintenant

        self.rowptr.append(0)
        nb_on_row = 0
        last_row = fromiter[0][0]
        for x in range(0, last_row):
            self.rowptr.append(0)

        for triplet in fromiter:
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
                # De plus, on doit sauvegarder les rows nuls. Donc, on ajoute les valeurs de row jusqu'au row depuis le dernier row

                self.rowptr.append(self.rowptr[-1] + nb_on_row)  # On ajoute le rowptr du row precedent

                for x in range(last_row+1, triplet[0]):   # On ajoute des intervalles vides pour les row entre last_row et
                                                        #  le row precedent
                    self.rowptr.append(self.rowptr[-1])

                last_row = triplet[0]  # On prend la valeur du nouveau row
                nb_on_row = 1  # On sait qu'il y a au moins ce triplet comme valaur non-nulle sur ce row

        self.rowptr.append(self.rowptr[-1] + nb_on_row)

    def __getitem__(self, k):
        try:
            i, j = k  # TODO: retourner la valeur correspondant à l'indice (i, j)
        except Exception:
            # k n'est pas un tuple
            return None

        try:
            return self.data[self.rowptr[i] + j]
        except Exception:
            # j trop grand pour i
            # ou i trop grand pour rowptr
            return 0

    def todense(self):
        # TODO: encoder la matrice en format dense TODO Numpy array? 2d list? triples et shape?
        pass


print("\n")
mat = SparseMatrix(fromiter=[(1, 0, 1), (1, 1, 30), (1, 3, 40), (2, 2, 50), (2, 3, 60), (2, 4, 70), (3, 5, 80)], shape=(4, 6))
print(mat.m)
print(mat.n)
print(mat.nnz)
print(mat.rowptr)
print(mat.colind)
print(mat.data)
