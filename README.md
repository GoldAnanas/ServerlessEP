# **Informatique Serverless**

Bienvenue sur le Git dédié à notre projet d'étude pratique sur l'informatique sans serveur. Nous expliquerons ici comment mettre en place les différentes applications
de l'informatique serverless que nous avons pu réaliser au cours de l'année. Etant donné que nous avons travaillé sur Amazon Web Services (AWS), il est nécessaire de posséder un
compte sur la plateforme afin de reproduire les différentes étapes présentées.

## **Clone Git**

Tout d'abord, afin de récupère le code de nos fonctions, nous vous conseillons soit de télécharger directement les fichiers via le site Gitlab ou bien de cloner le git.

``` bash
git clone https://gitlab.insa-rennes.fr/EPIS2019/main-project.git
```

## **Word Count parallélisé** (travail du semestre 1)
 - Connectez-vous sur le site d'[AWS](https://aws.amazon.com/marketplace/management/signin)
 - Allez sur le service **S3**
 - Créez les compartiments suivants avec à chaque fois l'accès public autorisé :
   - compartiment-entree
   - compartiment-avant-count1
   - compartiment-apres-count1
   - compartiment-sortie-resultat1
 - Allez sur le service **IAM**
 - Créez un nouveau rôle avec les permissions : *AWSLambdaFullAccess* et  *AmazonS3FullAccess*
 - Ensuite, allez sur le service **Lambda**
 - Créez une nouvelle fonction (le nom n'a pas d'importance)
 - Choisissez *Python 3.7* comme environnement d'éxecution
 - Assignez lui le rôle précédement créé
 - Copiez-collez dans l'IDE intégré le code de la fonction *Lambda_Trigger1_separationFichiers* présente sur le Git dans le dossier *S1* (et de même pour les fonctions 2 et 3)
 - Cliquez sur *Ajoutez un déclencheur* pour chaque fonction :
   - **Fonction 1** : type S3, *compartiment-entree*
   - **Fonction 2** : type S3, *compartiment-avant-count1*
   - **Fonction 3** : type S3, *compartiment-apres-count1*
 ```diff
 - Editez les paramètres de base de la Fonction 3 afin d'augmenter l'expiration à 1 minute
 ```
 
 Une fois toutes ces étapes réalisées, il suffit d'ajouter *cid.txt* (présent sur le Git dossier *S1*) dans le compartiment entrée **(sans oublier d'octroyer les autorisations publiques)**  
 Après quelques secondes, vous pouvez voir le *fichierRes.csv* dans le compartiment sortie.  
 
 ## **Algorithme de Planification d'agenda avec *pyLambdaFlows*** (travail du semestre 2)
 
 En ce qui concerne l'installation de *pyLambdaFlows*, nous avons repris la étapes décrites par les élèves de l'INSA sur leur [Git](https://github.com/Enderdead/pyLambdaFlows).
 L'installation requiert d'avoir Python 3 sur votre machine ainsi qu'un compte AWS.

- Après avoir cloné le Git, installez les dépendences en ouvrant un terminal dans *S2\pyLambdaFlow* :
``` bash
pip3 install -r requirements.txt
```
- Ensuite, lancez l'installateur :
``` bash
python3 setup.py install --user
```
- Sur le site d'AWS, créer un rôle nommé *LambdaBasicExecution* (plus d'information [ici](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)).
- Créez un compte IAM et exportez le fichier *accessKeys.csv* contenant les informations de connexion (plus d'information [ici](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)).
- Copiez le fichier *accessKeys.csv* dans le dossier *S2\Scheduling_with_PyLambdaFlow\Scheduling*.
- Pour lancer l'application de planification d'emploi du temps parallélisée sur les serveurs d'AWS : 
``` bash
python3 main_parallel_aws.py
```
- Pour comparer, il est possible de lancer l'application en séquentiel sur les serveurs d'AWS :
``` bash
python3 main_sequentiel_aws.py
```
- Ou bien, de lancer l'application en séquentiel sur votre machine :
``` bash
python3 main_sequentiel_local.py
```
