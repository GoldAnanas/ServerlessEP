import json, boto3
import codecs
import re
import time



def lambda_handler(event, context):
    
    time.sleep(2)
    
    s3=boto3.client("s3")
    s_3=boto3.resource("s3")
    if event:
        
        print("Event : ", event)
        file_Obj = event["Records"][0]
        file_name = str(file_Obj['s3']['object']['key'])
        print ("File name added:",file_name)
        
        
        filepath = event['Records'][0]['s3']['object']['key']
        
        nbFichiersAttendus=10
        count={} #Dictionnaire qui contiendra l'ensemble des mots de tous les fichiers et leur occurence
        listOfiles=[] #Tableau qui contiendra les clés des sous-fichiers
        nbFichiersPresent=0
        string=""
        #Construit la liste contenant les noms de fichier présents dans le bucket
        
        my_bucket = s_3.Bucket('compartiment-apres-count1') #Crée un nouveau Bucket

        for file in my_bucket.objects.all():
            listOfiles.append(file.key)
            nbFichiersPresent=nbFichiersPresent+1
        
        if nbFichiersPresent==nbFichiersAttendus:
            print("Nombre de fichiers Atteint, création du fichierRes dans compartiment-res")
            file_content=""
            for inc in range(0,nbFichiersAttendus,1):
                print("noms des fichiers pris en compte:\n",listOfiles[inc])
                time.sleep(2)
                fileObject= s3.get_object(Bucket="compartiment-apres-count1",Key=listOfiles[inc]) #Stocke les résultats des sous-fichiers
                
                for line in fileObject["Body"]._raw_stream:
                    array = line.strip().decode('utf-8').split(';') #Créer un tableau avec les résultats du comptage du sous-fichier
                    if array[0] in count: #regarde si le mot existe déjà dans le dictionnaire
                        tmp = count[array[0]]
                        count[array[0]] = int(tmp) + int(array[1]) #incremente l'occurrence du mot dans le dictionnaire
                    else:
                        count[array[0]] = int(array[1]) #sinon ajoute le mot au dictionnaire
                obj = s_3.Object("compartiment-apres-count1",listOfiles[inc])
                obj.delete() #supprime le fichier du bucket appellant, avec la boucle vide le bucket
        
        for key in count:
            string += str(key) + ";" + str(count[key]) + "\n" #on met le résultat dans un string, avec comme séparation ";"
            
            s3.put_object(Body=string.encode('utf-8'), Bucket="compartiment-sortie-resultat1", Key="fichierRes.csv") #Ajoute le fichier résultat dans le bucket