# 2015TP1

Bonjour, 

J'ai terminé de coder le tensor. 

Cependant, je ne peux le tester: mon portable a 4gb de ram, et je reçois une MemoryError avant de pouvoir terminer le test. 

Serait-il possible de changer le set d'images pour quelque chose de plus petit? Un stack de 60 000 bitmap semble être une grandeur arbitraire qui ne peut que nuire aux ordinateurs à plus faible budget. 

Même avant d'utiliser SparseTensor, générer les quads de coordonnées-valeurs prend beaucoup de temps et de mémoire. J'en arrive à 51.4% de ma mémoire de 4gb, seulement sur des méthodes sur lesquelles je n'ai peu ou pas de contrôle.

Pourquoi ne pas générer un stack pour tout le monde de, par exemple, 1000 images avec 50% des coordonnées à 0 et 50% non-nulles, à des emplacements choisis aléatoirement? Avec, probablement, des tranches vides et d'autres formations intéressantes?

Comme ça l'esprit du problème reste le même et on peut faire l'exercice sans avoir à traiter avec un nombre d'images très imposant. Avec ce set de 1000 images la difficulté reste la même, et le bitmap/matplotlib fonctionne toujours.

Oui, je pourrais travailler seulement sur ma tour à plus grand budget, mais j'aimerais pouvoir travailler sur le TP à l'école, sur mon portable. Et oui, peut-être que j'ai mal codé SparseTensor et qu'il ne devrait pas prendre autant d'espace, mais je ne peux le savoir tant que je ne réussis pas à en construire un. 

De plus, je suis certaine que plusieurs n'ont pas une tour de gamer à la maison et qu'ils ne pourront pas du tout faire le TP à moins d'être bien "timés" avec les salles d'ordinateurs de l'UdeM. 

Charlie
