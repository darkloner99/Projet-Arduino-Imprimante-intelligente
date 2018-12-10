# Projet-Arduino-Imprimante-intelligente

**Ce projet a pour but de créer une imprimante capable d'apprendre l'écriture d'une personne et par la suite d'être capable de transformer un texte écrit en version ordinateur,  en une version manuscrite avec l'ecriture de la personne, sans avoir forcément déjà enregisté ses mots écrits manuscrits**

L'imprimante comportera 4 moteurs pas a pas permettant une écriture sur l'axe x,y mais également de se déplacer sur l'axe z.
L'imprimante aura un écran lcd afin d'afficher les informations importantes comme les tâches en cour et également un systeme 
de protection numérique.

Elle comportera aussi un moyen de communication afin d'échanger des informations avec l'ordinateur *maître*
L' ordinateur sera nécessaire afin de programmer et d'éxecuter le réseau neuronale nécessaire à l'auto-génération 
du texte.
Le réseau neuronale raisonnera en terme de pixel, ainsi pour lui, les mots seront des pixels, la positions sera en pixel, etc...
Les mots seront une multitude de pixel.
