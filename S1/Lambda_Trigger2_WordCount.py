import json, boto3

def lambda_handler(event, context):
    
    
    s3_1=boto3.resource('s3')  #Connection à l'interface client de haut niveau de S3
    
    s3_2=boto3.client('s3')  
    if event:
        print("Event : ", event)
        file_Obj = event["Records"][0]
        file_name = str(file_Obj['s3']['object']['key'])
        print ("File name :",file_name)
        fileObject = s3_1.Object('compartiment-avant-count1', file_name) #Crée un Objet Ressource S3
        count={} #Dictionnaire qui contiendra l'ensemble des mots du sous-fichier et leur occurrence
        string=""
        
        for line in fileObject.get()["Body"]._raw_stream: #Récupère le stream
            if line.strip().decode('utf-8') in count: #strip : enlève les espaces, decode : Conversion en string
                count[line.strip().decode('utf-8')] += 1
            else:
                count[line.strip().decode('utf-8')] = 1
        
        for key in count:
            string += str(key).lower() + ";" + str(count[key]) + "\n" #met le résultat dans un string, avec comme séparation ";"
        
        string_encoded = string.encode('utf-8') #on encode à nouveau
        s3_2.put_object(Body=string_encoded, Bucket="compartiment-apres-count1", Key=file_name.replace(".txt","") + "-resized.csv") #Ajoute le sous fichier résultat dans le bucket
