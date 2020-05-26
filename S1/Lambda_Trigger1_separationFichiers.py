import json,boto3
import re, os
from io import BytesIO
import lzma
import zipfile

def lambda_handler(event, context):
    
    s3=boto3.client("s3")  #Connection à l'interface client de bas niveau du service S3
    
    if event:
        print("Event : ", event)
        file_Obj = event["Records"][0]
        file_name = str(file_Obj['s3']['object']['key'])  #Stocke le nom du fichier
        print ("File name :",file_name)
        fileObject= s3.get_object(Bucket="compartiment-entree1",Key=file_name)  #Récupère le fichier depuis le bucket de S3
        filePath = os.environ['LAMBDA_TASK_ROOT'] + "/"+file_name
        file_format= file_name.split('.')[1]
        print(file_format)
        
        if (file_format=="7z"):
            bytestream = BytesIO(fileObject['Body'].read())
            print(bytestream)
            data = lzma.open(bytestream, 'rt',encoding='utf-8',errors='ignore')
            #Le mode rb = read bytes aucun décodage n'est effectué et les caractères sont ainsi préservés, quel que soit leur encodage
            #Le mode rt = read text permet le gestion automatique du TextIOWrapper afin de directement lire le texte
            #data = TextIOWrapper(zipped)
            print(data)
        
        else:
            data = fileObject["Body"].read().decode('utf-8',errors="ignore")
            #print("File Obj", fileObject)
        
        file_content=""
        for line in data:
            file_content+= line
               
        #nbFichier = int(os.environ['SplitNumber'])
        nbFichier = 10
        
        words=[]
        #words=file_content.split("\r")
        
        words=re.findall(r"[\w']+", file_content) #permet le split en prennant tous les char (;:\n\r )
        print(words)
        cut1=len(words)/nbFichier
        string=""
        for i in range(0,int(cut1),1):  
            string += str(words[i]+"\n")
        string_encoded = string.encode('utf-8')
        s3.put_object(Body=string_encoded, Bucket="compartiment-avant-count1", Key="fichier1.txt")
        
        
        incre=2
        while(incre<=nbFichier):  #Boucle division le fichier en le nombre de sous-fichiers voulu
            endCut=int(incre*(len(words)/nbFichier))
            startCut=int((incre-1)*(len(words)/nbFichier))
            print(startCut)
            print(endCut)
            string=""
            for i in range(startCut,endCut,1): 
                string += str(words[i]+"\n")
            string_encoded = string.encode('utf-8')
            s3.put_object(Body=string_encoded, Bucket="compartiment-avant-count1", Key="fichier"+str(incre)+".txt")  #Exporte le sous-fichier dans le bucket
            incre=incre+1
        
        
      #  string=""
       # with open("/tmp/fichier2.txt","w+",encoding='utf-8') as o:
        #    for a in range(int(half),len(words),1):
         #       string += str(words[a]+"\n")
          #      
           # string_encoded = string.encode('utf-8')
        #    s3.put_object(Body=string_encoded, Bucket="conteneur-cible", Key="fichier2.txt")
             
        
