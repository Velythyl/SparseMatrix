"""
Auteure: Charlie Gauthier
Matricule: 20105623
Date: septembre 25 2015
"""

import bisect


# Pris de la documentation python officielle https://docs.python.org/2/library/bisect.html
# 20 octobre 2018
import numpy as np


def binary_search(liste, j, lo, hi):     # Fais une recherche pour j dans liste entre lo et hi
    index = bisect.bisect_left(liste, j, lo, hi)     # trouve point d'insertion de j
    if index != len(liste) and liste[index] == j:     # Si j se trouve deja a ce point
        return index                                # On a trouve j!
    raise Exception                                 # On cherche les Exception dans les try except des __getitem__


# Note: j'utilise le duck typing pour verifier le type des arguments et pour verifier si l'appel de fonction est valide
class SparseMatrix:

    # Genere un encodage de Yale pour un iterable de triplets et un tuple de dimensions
    def __init__(self, fromiter, shape):
        try:
            n, m = shape
            temp = iter(fromiter)  # Test si iterable
            if len(fromiter[0]) != 3:
                raise Exception
        except Exception:
            # mauvais types de fromiter ou shape
            return

        # add_ptr ajoute un intervalle a rowptr apres la borne exclus de l'intervalle precedent
        def add_ptr(lower, upper):
            for counter in range(lower, upper):
                self.rowptr.append(self.nnz)

        self.n = n  # hauteur
        self.m = m  # largeur

        self.nnz = 0  # le nombre de valeur non-nulles = le nombre de triplets, mais incremente dans boucle
        self.rowptr = [0]  # liste de taille n + 1 des intervalles des colonnes
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        fromiter.sort()  # on sait que les triplets sont en ordre des rangee maintenant

        last_row = fromiter[0][0]  # le "premier" last_row est le i du premier triplet

        add_ptr(0, last_row)  # on met des intervalles vides jusqu'au premier row non-nul

        for triplet in fromiter:
            # Peu importe ce qui se passe, on sait que chaque triplet n'est pas nul
            # Donc, on ajoute triplet[1] et triplet[2] a colind et data (respectivement) peu importe la valeur
            # de triplet[0]

            self.colind.append(triplet[1])  # On ajoute l'index de cet element a colind
            self.data.append(triplet[2])  # On ajoute la valeur de l'element a data

            if last_row != triplet[0]:
                # Sinon, on change de row
                # On ajoute donc l'intervalle du row precendent (add_ptr)
                # On ajoute des intervalles vides jusqu'au row present
                # On assign le row present a last_row

                add_ptr(last_row, triplet[0])  # On ajoute le rowptr du row precedent et les intervalles vides

                last_row = triplet[0]  # On prend la valeur du nouveau row

            self.nnz += 1  # On a ajoute une valeur non nulle avec succes

        # On n'ajoute pas l'intervalle du dernier row a rowptr: add_ptr est appele lorsqu'on change de row seulement
        # Donc, on l'ajoute ici, ainsi que des intervalles vides jusqu'au total de n si pertinent.
        add_ptr(last_row, self.n)

    # Retourne l'item aux coordonnees du tuple k
    def __getitem__(self, k):
        try:
            i, j = k
        except Exception:
            # k n'est pas un tuple
            return None

        try:
            temp = self._get_pointer_interval(i)
            lo = temp[0]  # On prend le pointer du row
            hi = temp[1]  # On prend la grosseur de l'interalle

            index = binary_search(self.colind, j, lo, hi)   # On trouve le decalage pour le j
            return self.data[index]                      # On retourne la valeur a ce decalage dans data

        except Exception:
            # Le couple n'est pas dans nos valeurs non-nulles
            if i <= self.n and j <= self.m:  # Si le couple est dans la matrice
                return 0  # Retourne valeur nulle
            else:  # Sinon
                return None  # valeur hors-matrice: None

    # Retourne une matrice dense tiree de l'encodage de Yale de l'objet
    def todense(self):
        # On cree une matrice de 0 du bon format
        matrix = [[0] * self.m for i in range(self.n)]

        # Pour chaque rangee
        for i in range(self.n):
            temp = self._get_pointer_interval(i)
            pointer = temp[0]  # On prend le pointer du row
            nb_non_nul = temp[1] - pointer  # On prend la grosseur de l'interalle

            if nb_non_nul == 0:  # Si l'intervalle est vide, on passe a la prochaine rangee
                continue

            # Si l'interval n'est pas vide, on parcours les points non-nuls (colind, data) du row et on assigne dans
            # la matrice a l'emplacement i (pris de la boucle englobante), j (pris de colind) l'item correspondant
            # (pris de data)
            #
            # On connait le nombre de valeurs non-nulles de suite: c'est la grosseur de l'interval, nb_non_nul
            #
            # pointer+counter: counter s'incremente nb_non_nul fois. En y ajoutant son pointeur, on retrouve l'indice
            # des j et des data correspondant
            for counter in range(nb_non_nul):
                matrix[i][self.colind[pointer + counter]] = self.data[pointer + counter]

        return matrix  # retourne la matrice dense

    def _get_pointer_interval(self, i):  # Retourne le pointeur sur colind et data ainsi que le nombre de valeurs
        pointer = self.rowptr[i]  # non-nulles sur le row
        pointer_hi = self.rowptr[i + 1]  # On prend la grosseur de l'interalle
        return [pointer, pointer_hi]


class SparseTensor:

    # Note: on assume qu'on recoit les fromiter sous forme (k,i,j,valeur): ceci est plus logique pour la generalisation
    # Donc, on a dim x, dim x-1, ..., dim 3, dim 2, dim 1, valeur
    def __init__(self, fromiter, shape):
        try:
            o, n, m = shape
            temp = iter(fromiter)  # Test si iterable
            if len(fromiter[0]) != 4:
                raise Exception
        except Exception:
            # mauvais types de fromiter ou shape
            return

        # add_ptr ajoute un intervalle a rowptr apres la borne exclus de l'intervalle precedent
        def add_ptr(lower, upper):
            for counter in range(lower, upper):
                self.rowptr.append(self.nnz)

        self.n = n  # hauteur
        self.m = m  # largeur
        self.o = o  # profondeur

        self.nnz = 0  # le nombre de valeur non-nulles = le nombre de quads, incremete dans la boucle principale
        self.rowptr = [0]  # liste de taille n + 1 des intervalles des rangees-profondeurs
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        fromiter.sort()  # on sait que les quads sont en ordre des profondeurs puis rangees maintenant

        # Concept: les ki: ils sont l'agencement profondeur-rangee d'une valeur dans la matrice. On le calcule avec
        # profondeur * nombre de rangees par profondeur + rangee
        last_ki = fromiter[0][0] * self.n + fromiter[0][1]  # le "premier" last_ki est le ki du premier quad

        add_ptr(0, last_ki)  # On ajoute des pointeurs vides jusqu'au premier ki non-nul

        for quad in fromiter:
            # Peu importe ce qui se passe, on sait que chaque quad n'est pas nul
            # Donc, on ajoute quad[2] et quad[3] a colind et data (respectivement) peu importe la valeur
            # de quad[0] et [1]

            self.colind.append(quad[2])  # On ajoute l'index de cet element au colind
            self.data.append(quad[3])  # On ajoute la valeur de l'element a data

            temp_ki = quad[0] * self.n + quad[1]  # Le ki du row present
            if last_ki != temp_ki:
                # Si on change de ki
                # On ajoute donc l'intervalle du row precendent (add_ptr)
                # On ajoute des intervalles vides jusqu'au row present
                # On assigne le row present a last_ki

                add_ptr(last_ki, temp_ki)  # On ajoute le rowptr du row precedent et les intervalles nuls si besoin

                last_ki = temp_ki  # On prend la valeur du nouveau row

            self.nnz += 1  # On a ajoute une valeur avec succes
            print(quad)  # Montrer que le programme travaille encore, commenter au besoin
            quad = None  # Liberer de la memoire

        # On n'ajoute pas l'intervalle du dernier ki a rowptr: add_ptr est appele lorsqu'on change de ki.
        # Donc, on l'ajoute ici.
        add_ptr(last_ki, self.o * self.n + 1)

    def __getitem__(self, triple):
        try:
            i, j, k = triple
        except Exception:
            # triple n'est pas un triple (donc coordonnee pas valide)
            return None

        try:
            temp = self._get_pointer_interval(k, i)
            lo = temp[0]  # On prend le pointer du row
            hi = temp[1]  # On prend la grosseur de l'interalle

            index = binary_search(self.colind, j, lo, hi)  # On trouve le decalage pour le j
            return self.data[index]  # On retourne la valeur a ce decalage dans data

        except Exception:
            # Le couple n'est pas dans nos valeurs non-nulles
            if i <= self.n and j <= self.m and k <= self.o:  # Si le couple est dans la matrice
                return 0  # valeur nulle
            else:  # Sinon
                return None  # valeur hors-matrice: None

    def todense(self):
        # On cree une matrice de 0 du bon format
        matrix3d = [[[0 for j in range(self.m)] for i in range(self.n)] for k in range(self.o)]

        # Pour chaque profondeur
        for k in range(self.o):
            for i in range(self.n):
                temp = self._get_pointer_interval(k, i)
                pointer = temp[0]  # On prend le pointer du row
                nb_non_nul = temp[1] - pointer  # On prend la grosseur de l'interalle

                if nb_non_nul == 0:  # Si l'intervalle est vide, on passe a la prochaine rangee
                    continue

                # Si l'interval n'est pas vide, on parcours les points non-nuls (colind, data) du ki et on assigne dans
                # la matrice a l'emplacement k, i (pris des boucles englobantes) j (pris de colind) l'item correspondant
                # (pris de data)
                #
                # On connait le nombre de valeurs non-nulles de suite: c'est la grosseur de l'interval, nb_non_nul
                #
                # pointer+counter: counter s'incremente nb_non_nul fois. En y ajoutant son pointeur, on retrouve
                # l'indice des j (colind) et des data correspondants
                for counter in range(nb_non_nul):
                    matrix3d[k][i][self.colind[pointer + counter]] = self.data[pointer + counter]

        return matrix3d  # retourne la matrice dense

    def _get_pointer_interval(self, k, i):  # Retourne le pointeur sur colind et data ainsi que le nombre de
        pointer = self.rowptr[k * self.n + i]  # valeurs non-nulles sur ki
        pointer_hi = self.rowptr[k * self.n + i + 1]  # On prend la grosseur de l'interalle
        return [pointer, pointer_hi]

    def get_nb_of_nb(self):
        return len(self.rowptr) + len(self.data) + len(self.colind) + len([self.nnz, self.m, self.o, self.n])


class VerySparseTensor:

    # Note: on assume qu'on recoit les fromiter sous forme (k,i,j,valeur): ceci est plus logique pour la generalisation
    # Donc, on a dim x, dim x-1, ..., dim 3, dim 2, dim 1, valeur
    def __init__(self, fromiter, shape):
        try:
            o, n, m = shape
            temp = iter(fromiter)  # Test si iterable
            if len(fromiter[0]) != 4:
                raise Exception
        except Exception:
            # mauvais types de fromiter ou shape
            return

        nb_null_prof = 0  # Compte le nombre de profondeurs vides (decommenter dans fill_blank_prof et a la fin de

        # init

        # fill_blank ajoute des intervalles vides pour les rows de lower a upper, inclus-exclus
        def fill_blank(lower, upper):
            for counter in range(lower, upper):
                self.rowptr.append(self.rowptr[-1])

        # fill_blank_prof ajoute des intervalles vides pour les profondeurs de lower a upper, inclus-exclus
        def fill_blank_prof(lower, upper):
            for counter in range(lower, upper):
                self.profptr.append(self.profptr[-1])

                global nb_null_prof  # A decommenter pour voir le nombre de prof nulles
                nb_null_prof += 1

        # add_ptr ajoute un intervalle a rowptr d'apres la borne exclus de l'intervalle precedent
        def add_ptr():
            self.rowptr.append(self.rowptr[-1] + nb_on_row)

        # Un pointeur de profondeur est toujours de n elements (on pointe sur tous les intervalles de la prof.)
        def add_ptr_prof():
            self.profptr.append(self.profptr[-1] + self.n)

        self.n = n  # hauteur
        self.m = m  # largeur
        self.o = o  # profondeur

        self.nnz = len(fromiter)  # le nombre de valeur non-nulles = le nombre de triplets
        self.profptr = []  # liste de taille o + 1 des intervalles des rangees (donc prof)
        self.rowptr = []  # liste de taille n + 1 des intervalles des colonnes
        self.colind = []  # liste de taille nnz des indices des valeurs non-nulles
        self.data = []  # liste de taille nnz des valeurs non-nulles

        fromiter.sort()  # on sait que les quads sont en ordre des profondeurs maintenant

        nb_on_row = 0  # en ce moment, il n'y a rien sur le row
        last_prof = fromiter[0][0]  # et le "premier" last_prof est le k du premier quad
        last_row = fromiter[0][1]  # et le "premier" last_row est le i du premier quad

        self.rowptr.append(0)  # rowptr commence toujours par 0
        self.profptr.append(0)  # de meme pour profptr
        fill_blank_prof(0, last_prof)  # on met des intervalles vides jusqu'a la premiere profondeur non-vides
        fill_blank(0, last_row)  # on met des intervalles vides jusqu'au premier row non-nul

        for quad in fromiter:
            # Peu importe ce qui se passe, on sait que chaque quad n'est pas nul
            # Donc, on ajoute quad[2] et quad[3] a colind et data (respectivement) peu importe la valeur
            # de quad[0] et [1]

            self.colind.append(quad[2])  # On ajoute l'index de cet element au colind
            self.data.append(quad[3])  # On ajoute la valeur de l'element a data

            if last_prof == quad[0]:
                # Si on est sur la meme profondeur

                if last_row == quad[1]:
                    # Et le meme row: on a une valeur de plus sur le row
                    nb_on_row += 1

                else:
                    # Sinon, on doit assumer qu'on change de row
                    # On ajoute donc l'intervalle du row precendent (add_ptr)
                    # On ajoute des intervalles vides jusqu'au row present
                    # On assign le row present a last_row
                    # On assigne 1 a nb_on_row puisque le quad present est lui-meme une valeur non-nulle

                    # Si on est sur la meme prof que le dernier quad:

                    add_ptr()  # On ajoute le rowptr du row precedent

                    # On ajoute des intervalles vides pour les row entre last_row et le row precedent
                    fill_blank(last_row + 1, quad[1])

                    last_row = quad[1]  # On prend la valeur du nouveau row
                    nb_on_row = 1  # On sait qu'il y a au moins ce quad comme valaur non-nulle sur ce row

            else:
                # Sinon, on change de profondeur
                # On doit finaliser le row, puis changer de profondeur

                add_ptr()  # Ajout pointeur row (qui vient de l'ancienne profondeur) precedent

                fill_blank(last_row + 1, self.n)  # Remplir le reste du row

                last_prof = quad[0]  # Changer de profondeur
                last_row = quad[1]  # Change de row

                fill_blank(0, last_row)  # Remplir le debut (si vide) du row sur la nouvelle prof.

                add_ptr_prof()  # Ajouter le pointeur pour cette profondeur non-nulle precendente
                fill_blank_prof(last_prof + 1, quad[0])  # Remplir les intervalles vides entre l'ancienne et la
                # nouvelle profondeur

                nb_on_row = 1  # Ce quad est une valeur non-nulle

            quad = None  # Liberer de la memoire

        # On n'ajoute pas l'intervalle du dernier row a rowptr: add_ptr est appele lorsqu'on change de row.
        # Donc, on l'ajoute ici. nb_on_row est ici correct: on l'a calcule dans la boucle
        add_ptr()
        add_ptr_prof()

        # On met des intervalles vides pour les rows plus grands que le dernier row non-nul
        # last_row et last_prof sont eux aussi valides: on les a calcules dans la boucle
        fill_blank(last_row + 1, self.n)
        fill_blank_prof(last_prof + 1, self.o)

    def __getitem__(self, triple):
        try:
            i, j, k = triple
        except Exception:
            # triple n'est pas un triple (donc coordonnee pas valide)
            return None

        def _error():
            # Le couple n'est pas dans nos valeurs non-nulles
            if i <= self.n and j <= self.m and k <= self.o:  # Si le couple est dans la matrice
                return 0  # valeur nulle
            else:  # Sinon
                return None  # valeur hors-matrice: None

        try:
            temp = self._get_pointer_interval(k, i)
            lo = temp[0]  # On prend le pointer du row
            hi = temp[1]  # On prend la grosseur de l'interalle

            index = binary_search(self.colind, j, lo, hi)  # On trouve le decalage pour le j
            return self.data[index]  # On retourne la valeur a ce decalage dans data

        except Exception:
            # Le couple n'est pas dans nos valeurs non-nulles
            if i <= self.n and j <= self.m and k <= self.o:  # Si le couple est dans la matrice
                return 0  # valeur nulle
            else:  # Sinon
                return None  # valeur hors-matrice: None

    def todense(self):
        # On cree une matrice de 0 du bon format
        matrix3d = [[[0 for j in range(self.m)] for i in range(self.n)] for k in range(self.o)]

        # Pour chaque profondeur
        for k in range(self.o):
            if self.profptr[k] == self.profptr[k] + 1:  # si profondeur vide, on passe a la prochaine
                continue

            # Profondeur pas vide
            # Pour chaque rangee
            for i in range(self.n):
                temp = self._get_pointer_interval(k, i)
                pointer = temp[0]  # On prend le pointer du ki
                nb_non_nul = temp[1] - pointer  # On prend la grosseur de l'interalle

                if nb_non_nul == 0:  # Si l'intervalle est vide, on passe a la prochaine rangee
                    continue

                # Si l'interval n'est pas vide, on parcours les points non-nuls (colind, data) du row et on assigne dans
                # la matrice a l'emplacement k,i (pris de la boucle englobante), j (pris de colind) l'item correspondant
                # (pris de data)
                #
                # On connait le nombre de valeurs non-nulles de suite: c'est la grosseur de l'intervalle, nb_non_nul
                #
                # pointer+counter: counter s'incremente nb_non_nul fois. En y ajoutant son pointeur, on retrouve
                # l'indice des j et des data correspondant
                for counter in range(nb_non_nul):
                    matrix3d[k][i][self.colind[pointer + counter]] = self.data[pointer + counter]

        return matrix3d  # retourne la matrice dense

    def _get_pointer_interval(self, k, i):  # Retourne le pointeur sur colind et data ainsi que le nombre de
        pointer = self.rowptr[i + self.profptr[k]]  # valeurs non-nulles sur ki
        pointer_hi = self.rowptr[i + self.profptr[k] + 1]
        return [pointer, pointer_hi]

    def get_nb_of_nb(self):
        return len(self.rowptr) + len(self.profptr) + len(self.data) + len(self.colind) + \
               len([self.nnz, self.m, self.o, self.n])

class SparseDict:
    # Note: on assume qu'on recoit les fromiter sous forme (k,i,j,valeur): ceci est plus logique pour la generalisation
    # Donc, on a dim x, dim x-1, ..., dim 3, dim 2, dim 1, valeur
    def __init__(self, fromiter, shape):
        self.shape = shape
        self.dict = {}

        for iter in fromiter:
            print(iter) # voir travail
            sub_dict = self.dict
            for dim in range(len(shape)):
                key = iter[dim]

                if dim < len(shape)-1:
                    try:
                        sub_dict = sub_dict[key]
                    except Exception:
                        sub_dict[key] = {}
                        sub_dict = sub_dict[key]
                else:
                    sub_dict[key] = iter[dim+1]
                    break

    def __getitem__(self, arg_list):
        for counter in range(len(self.shape)):
            if arg_list[counter] >= self.shape[counter]:
                return None

        try:
            val = eval("self.dict"+self._get_bracketer(arg_list))
            return val

        except Exception:
            return 0

    def todense(self):
        # On cree une matrice de 0 du bon format
        matrix = np.zeros(self.shape, int).tolist()

        self._walk_and_add(matrix, [], self.dict)

        return matrix


    def _walk_and_add(self, matrix, arg_list, sub_dict):
        try:  # plante si next_dict est en fait la val
            for clef in sub_dict:
                break
        except Exception:  # On a donc la val dans next_dict
            executable = "matrix"+self._get_bracketer(arg_list)
            executable += "=" + str(sub_dict)

            exec(executable)
            return

        for key in sub_dict:
            next_dict = sub_dict[key]  # prend le prochain dict
            next_list = arg_list.copy()
            next_list.append(key)

            print(*next_list)

            self._walk_and_add(matrix, next_list, next_dict)

    def _get_bracketer(self, arg_list):
        executable = ""
        for arg in arg_list:
            executable += "[" + str(arg) + "]"
        return executable

    def get_nb_of_nb(self):
        return len(self.rowptr) + len(self.data) + len(self.colind) + len([self.nnz, self.m, self.o, self.n])