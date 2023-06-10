import dlib
import cv2
import numpy as np
import time
import shutil
import os
import face_recognition
import zipfile


def  findcomapre(abc):
    
    path = os.getcwd()+abc

    #print the main dir for user
    print(path)    
    folder_path = os.path.join(path, 'group')

    #printing the group folder to check th upload
    print(folder_path)
    def get_file_names(folder_path):
       files = []
       for file_name in os.listdir(folder_path):
           if os.path.isfile(os.path.join(folder_path, file_name)):
               files.append(file_name)
       return files[0]
    zip_name = get_file_names(folder_path)

    #print the zip file name 
    print(zip_name)

    def extract_to_drive(zip_path, output_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

    zip_file_path = os.path.join(path, 'group',zip_name)
    output_directory = os.path.join(path, 'extracted')

    extract_to_drive(zip_file_path, output_directory)

    zip_file_name = os.listdir(output_directory)
    #printing the name name of the extracted file name
    print(zip_file_name[0])


    folder_path_folder = os.path.join(path, 'extracted', zip_file_name[0])

    # Get the file names in the folder
    file_names = os.listdir(folder_path_folder)

    # Rename the files numerically
    for index, file_name in enumerate(file_names):
        # Get the file extension
        #file_ext = os.path.splitext(file_name)[1]
        file_start = os.path.splitext(file_name)[0]
        print(file_start)
    
        # Construct the new file name
        new_file_name = f'{index + 1}'+'.jpg'

        # Get the full paths of the old and new file names
        old_file_path = os.path.join(folder_path_folder, file_name)
        new_file_path = os.path.join(folder_path_folder, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
    
    sample_folder_path= os.path.join(path,'sample')

    detector = dlib.get_frontal_face_detector()

    print(os.path.join(path, 'sample' , os.listdir(sample_folder_path)[0]))

    # Load the image    
    image = cv2.imread(os.path.join(path, 'sample' , os.listdir(sample_folder_path)[0]))

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect the faces in the image
    faces = detector(gray)

    # Extract the faces and save them to files
    for i, face in enumerate(faces):
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        # Extract the face from the image
        face_image = image[y1:y2, x1:x2]

        # Resize the face image to a standard size
        face_image = cv2.resize(face_image, (256, 256))

        # Save the face image to a file
        cv2.imwrite(os.path.join(path, 'compare', 'compare.jpg'), face_image)

        # Show the image with rectangles around the detected faces
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Load the face images
    image = face_recognition.load_image_file(os.path.join(path, 'compare', 'compare.jpg'))

    #embed
    embedding_sample = face_recognition.face_encodings(image,num_jitters=10, model='small')[0]
    print(embedding_sample)
    

    folder_path_folder1 = os.path.join(path, 'extracted', zip_file_name[0])
    file_names1 = os.listdir(folder_path_folder1)
    print(file_names1)

    file_path=[]
    folder_name = os.listdir(os.path.join(path,'extracted'))[0]
    print(folder_name)
    for file_name in file_names1:
        print(file_name)
        file_path.append(os.path.join(path,'extracted',folder_name, file_name))
        print(file_path)

    #operation for group photos

    for a,file_names1 in enumerate(file_path):
        print(a)
        print(file_names1)
        print(type(file_names1))
        # Load the image
        image = cv2.imread(file_names1)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        os.mkdir(os.path.join(path,'facial_folder',f'facial_photo_compare_{a}'))
        # Detect the faces in the image
        faces = detector(gray)
        time.sleep(1)

        embedding_list = []
        # Extract the faces and save them to files
        for i, face in enumerate(faces):
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            # Extract the face from the image
            face_image = image[y1:y2, x1:x2]

            # Resize the face image to a standard size
            face_image = cv2.resize(face_image, (256, 256))

            # Save the face image to a file
            cv2.imwrite(os.path.join(path,'facial_folder',f'facial_photo_compare_{a}','face_{i}.jpg'), face_image)

            try:
            #embeding the images / read the image
                embedding = face_recognition.face_encodings(face_recognition.load_image_file(os.path.join(path,'facial_folder',f'facial_photo_compare_{a}','face_{i}.jpg')), num_jitters=5,model='small')[0]
                embedding_list.append(embedding)
        #compare the embeding
                is_match = face_recognition.compare_faces(embedding_list, embedding_sample,tolerance=0.55)
            except IndexError:
             continue


        if any(is_match):
            shutil.copy2(file_names1, os.path.join(path,'result'))

        print(is_match)

  # Show the image with rectangles around the detected faces
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    
    
    return os.path.join(path,'result')