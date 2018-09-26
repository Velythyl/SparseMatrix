"""
Auteure: Charlie Gauthier
Matricule: 20105623
Date: septembre 25 2015
"""


# Note: j'utilise le duck typing pour verifier le type des arguments et pour verifier si l'appel de fonction est valide

class SparseMatrix:

    # Genere un encodage de Yale pour un iterable de triplets et un tuple de dimensions
    def __init__(self, fromiter, shape):
        try:
            n, m = shape
            temp = iter(fromiter)
            if len(fromiter[0]) != 3:
                raise Exception
        except Exception:
            # mauvais types de fromiter ou shape
            return

        # fill_blank ajoute des intervalles vides pour les rows de lower a upper, inclus-exclus
        def fill_blank(lower, upper):
            for counter in range(lower, upper):
                self.rowptr.append(self.rowptr[-1])

        # add_ptr ajoute un intervalle a rowptr d'apres la borne exclus de l'intervalle precedent
        def add_ptr():
            self.rowptr.append(self.rowptr[-1] + nb_on_row)

        self.n = n  # hauteur
        self.m = m  # largeur

        self.nnz = len(fromiter)  # le nombre de valeur non-nulles = le nombre de triplets
        self.rowptr = []  # liste de taille n + 1 des intervalles des colonnes
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        fromiter.sort()  # on sait que les triplets sont en ordre des rangee maintenant

        nb_on_row = 0  # en ce moment, il n'y a rien sur le row
        last_row = fromiter[0][0]  # et le "premier" last_row est le i du premier triplet

        self.rowptr.append(0)  # rowptr commence toujours par 0
        fill_blank(0, last_row)  # on met des intervalles vides jusqu'au premier row non-nul

        for triplet in fromiter:
            # Peu importe ce qui se passe, on sait que chaque triplet n'est pas 0.
            # Donc, on ajoute triplet[1] et triplet[2] a colind et data (respectivement) peu importe la valeur
            # de triplet[0]

            self.colind.append(triplet[1])  # On ajoute l'index de cet element au colind
            self.data.append(triplet[2])  # On ajoute la valeur de l'element a data

            if last_row == triplet[0]:
                # Si on est sur le meme row que le dernier triplet:
                nb_on_row += 1  # On incremente simplement le nombre de valeurs sur le row

            else:
                # Sinon, on doit assumer qu'on change de row
                # On ajoute donc l'intervalle du row precendent (add_ptr)
                # On ajoute des intervalles vides jusqu'au row present
                # On assign le row present a last_row
                # On assigne 1 a last_row puisque le triplet present est lui-meme une valeur non-nulle

                add_ptr()  # On ajoute le rowptr du row precedent

                # On ajoute des intervalles vides pour les row entre last_row et le row precedent
                fill_blank(last_row + 1, triplet[0])

                last_row = triplet[0]  # On prend la valeur du nouveau row
                nb_on_row = 1  # On sait qu'il y a au moins ce triplet comme valaur non-nulle sur ce row

        # On n'ajoute pas l'intervalle du dernier row a rowptr: add_ptr est appele lorsqu'on change de row.
        # Donc, on l'ajoute ici. nb_on_row est ici correct: on l'a calcule dans la boucle
        add_ptr()

        # On met des intervalles vides pour les rows plus grands que le dernier row non-nul
        # last_row est lui aussi valide, pour la meme raison que nb_on_row a l'instruction precedente.
        fill_blank(last_row + 1, n)

    # Retourne l'item aux coordonnees du tuple k
    def __getitem__(self, k):
        try:
            i, j = k
        except Exception:
            # k n'est pas un tuple
            return None

        try:
            return self.data[self.rowptr[i] + j]
        except Exception:
            # Le couple n'est pas dans nos valeurs non-nulles

            if i <= self.n and j <= self.m:     # Si le couple est dans la matrice
                return 0                        # valeur nulle
            else:                               # Sinon
                return None                     # valeur hors-matrice None

    # Retourne une matrice dense tiree de l'encodage de Yale de l'objet
    def todense(self):
        # On cree une matrice de 0 du bon format
        matrix = [[0] * self.m for i in range(self.n)]

        # Pour chaque rangee
        for i in range(self.n):
            pointer = self.rowptr[i]                    # On prend le pointer du row
            nb_non_nul = self.rowptr[i+1] - pointer    # On prend la grosseur de l'interalle

            if nb_non_nul == 0:    # Si l'intervalle est vide, on passe a la prochaine rangee
                continue

            # Si l'interval n'est pas vide, on parcours les points non-nuls (colind, data) du row et on assigne dans
            # la matrice a l'emplacement i (pris de la boucle englobante), j (pris de colind) l'item correspondant
            # (pris de data)
            #
            # pointer+counter: counter s'incremente nb_non_nul fois. En y ajoutant son pointeur, on retrouve l'indice
            # des j et des data correspondant
            for counter in range(nb_non_nul):
                matrix[i][self.colind[pointer+counter]] = self.data[pointer+counter]

        return matrix   # retourne la matrice dense


print("\n")
sparse = SparseMatrix(fromiter=[(1, 0, 1), (1, 1, 30), (1, 3, 40), (2, 2, 50), (2, 3, 60), (2, 4, 70), (3, 5, 80)],
                      shape=(4, 6))
print(sparse.m)
print(sparse.n)
print(sparse.nnz)
print(sparse.rowptr)
print(sparse.colind)
print(sparse.data)
print(sparse.todense())

print("\n")
sparse = SparseMatrix(fromiter=[(0, 1, 1), (1, 0, 2), (2, 1, 4), (2, 2, 3)],
                      shape=(3, 3))
print(sparse.m)
print(sparse.n)
print(sparse.nnz)
print(sparse.rowptr)
print(sparse.colind)
print(sparse.data)
print(sparse.todense())
