"""
Auteure: Charlie Gauthier
Matricule: 20105623
Date: septembre 25 2015
"""

# Note: j'utilise le duck typing pour verifier le type des arguments et pour verifier si l'appel de fonction est valide
# 


class SparseMatrix:
    def __init__(self, fromiter, shape):
        try:
            n, m = shape
            temp = iter(fromiter)
        except Exception:
            # mauvais types de fromiter ou shape
            return None
            
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
                # De plus, on doit sauvegarder les rows nuls. Donc, on ajoute les valeurs de row jusqu'au row depuis le dernier row

                for x in range(last_row, triplet[0]):   # On ajoute des intervalles vides pour les row entre last_row et le row precedent
                    self.rowptr.append(self.rowptr[-1])
                    
                self.rowptr.append(self.rowptr[-1] + nb_on_row)     # On ajoute le rowptr du row precedent

                last_row = triplet[0]   # On prend la valeur du nouveau row
                nb_on_row = 1           # On sait qu'il y a au moins ce triplet comme valaur non-nulle sur ce row

    def __getitem__(self, k):       # TODO donc seulement retourner la diagonale? Devrait pas etre k, i? pour k ieme ele sur ligne i
                                    # TODO ou i, j? ou k = tuple
                                    # TODO ou k, et on trouve le k ieme element sans prendre i, j=k?
        try:
            i, j = k # TODO: retourner la valeur correspondant à l'indice (i, j)
        except Exception:
            # k n'est pas un tuple
            return None
        
        try:
            return data[self.rowptr[i]+j]
        except Exception:
            # j trop grand pour i
            # ou i trop grand pour rowptr
            return None
            
    def todense(self):
        # TODO: encoder la matrice en format dense TODO Numpy array? 2d list? triples et shape?
        pass
