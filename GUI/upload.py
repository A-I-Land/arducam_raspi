import os
import requests
from database import *

Image_Path = '/home/ailand/GUI_Data/'


def imageUpload(stage, imageName):
    """
    Upload des ubergebenen Bildes

    stage - Upload Server
    imageName - Bild Name
    """

    STAGE = stage

    if STAGE == "qa":
        CLIENT_ID="qftnh9tr1n2il47k8pvg6v9ro"
        CLIENT_SECRET="fvl36lb6rjr9t6voqa5v52u97j27v2t2cib6p7vd0sr01sufdrl"
        INGESTION_URL="https://appcontroller.fc." + STAGE + ".ddfarming.de/deviceapi/upload"

    if STAGE == "prod":
        INGESTION_URL = "https://appcontroller.fc.ddfarming.de/deviceapi/upload"
        CLIENT_ID = "411d8g5q20dnrahlvhkobcl63v"
        CLIENT_SECRET = "1oe1td2vpcpsbiufvdosm70rphqdapd6m1vdor5489bgcu1j5ssg"

    AUTH_URL="https://auth." + STAGE + ".ddfarming.de/oauth2/token"
    REFRESH_URL="https://appcontroller.fc." + STAGE + ".ddfarming.de/deviceapi/images/refresh-presigned-urls"

    #print(AUTH_URL)
    #print(INGESTION_URL)

    got_access_token = False
    uploaded_image_data = False
    uploaded_image = False

    #Upload Prozess Status
    status = "Started Upload"
    changeDatabaseImageValue("State", imageName, status)


    #Access Token empfangen
    try:

        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }


        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }


        login_response = requests.post(AUTH_URL, headers=headers, data=data)

        #print(login_response)

        #Response Code ueberprüfung
        if login_response.status_code == 200:
            access_token = login_response.json()["access_token"]
            #print(access_token)
            if access_token != None:
                got_access_token = True
                status = "Successfully retrieve access token"
            else:
                status = "Failed to retrieve access token"

    except Exception as e:
        eMessage = "Error: Could not retrieve access token \n" + str(e)
        print(eMessage)
        got_access_token = False
        status = "Failed to retrieve access token"

    changeDatabaseImageValue("State", imageName, status)
    #print(status)

    #Bilddaten wurden nur gesendet wenn Access Token erfolgreich empfangen wurde
    if got_access_token:
        #Hochladen von Bilddaten (json)
        try:

            ingestion_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token,
            'x-device-id': 'test',
            }


            with open(Image_Path + imageName + '.json') as f:
                ingestion_data = f.read().replace('\n', '')


            ingestion_response = requests.post(INGESTION_URL, headers=ingestion_headers, data=ingestion_data)

            #Response Code ueberprüfung
            if ingestion_response.status_code == 200:

                #print(ingestion_response)
                #print(ingestion_response.json())

                request_id = ingestion_response.json()["request_id"]
                if request_id != None:
                    uploaded_image_data = True
                    status = "Successfully uploaded image data"
                else:
                    status = "Failed to uploaded image data"
                image_info = ingestion_response.json()["images"]
                image_id = image_info[0]['image_id']
                presigned_url = image_info[0]['presigned_url']
                ingestion_access_token = ingestion_response.json()["access_token"]


                #print(request_id)
                #print(image_id)
                #print(presigned_url)
                #print(ingestion_access_token)

        except:
            eMessage = "Error culd not upload image Data \n" + str(e)
            print(eMessage)
            uploaded_image_data = False
            status = "Failed to upload image data"

        changeDatabaseImageValue("State", imageName, status)
        #print(status)

    #Bild wird nur hochgeladen wenn Bilddaten erfolgreich hochgeladen wurden
    if uploaded_image_data:
        #Bild hochladen
        try:

            image_headers = {
                'Content-Type': 'image/jpeg',
            }

            with open(Image_Path + imageName + '.jpg', 'rb') as f:
                image_data = f.read()

            image_response = requests.put(presigned_url, headers=image_headers, data=image_data)

            #Response Code ueberprüfung
            if image_response.status_code == 200:
                #Speichern in der Datenbank dass das Bild erfolgreich hochgladen wurde
                changeDatabaseImageValue("Status", imageName, "Uploaded")
                uploaded_image = True
                status = "Successfully uploaded image"
            else:
                status = "Failed to uploaded image"

            #print(image_response)
        except:
            print("Error: Could not upload image")
            uploaded_image = False
            status = "Failed to uploaded image"

        changeDatabaseImageValue("State", imageName, status)
        #print(status)

    return uploaded_image

