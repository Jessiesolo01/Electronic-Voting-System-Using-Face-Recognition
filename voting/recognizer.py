from django.conf import settings
from deepface import DeepFace
import face_recognition
import numpy as np
import cv2
import os


"""
def Recognizer(details):
	video = cv2.VideoCapture(0)
	known_face_encodings = []
	known_face_names = []
	base_dir = os.path.dirname(os.path.abspath(__file__))
	base_dir = os.getcwd()
	image_dir = os.path.join(base_dir,"{}\{}".format('face_recognition_data', details['email']))
	win_name = "Verifying Login"
	print(image_dir)
	names = []
	for root, dirs, files in os.walk(image_dir):
		for file in files:
			if file.endswith('jpg') or file.endswith('png'):
				path = os.path.join(root, file)
				img = face_recognition.load_image_file(path)
				label = file[:len(file)-4]
				img_encoding = face_recognition.face_encodings(img)
				if len(img_encoding) > 0:
					known_face_names.append(label)
					known_face_encodings.append(img_encoding[0])
				else:
					print("No faces found in the image!")
					serializers.ValidationError("No faces found in image")
	face_locations = []
	face_encodings = []

	while True:
		check, frame = video.read()
		small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)
		rgb_small_frame = small_frame[:,:,::-1]
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
		face_names = []
		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)
			face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
			try:
				matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)
				face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
				best_match_index = np.argmin(face_distances)

				if matches[best_match_index]:
					name = known_face_names[best_match_index]
					face_names.append(name)
					if name not in names:
						names.append(name)
			except:
				pass

		if len(face_names) == 0:
			for (top,right,bottom,left) in face_locations:
				top*=2
				right*=2
				bottom*=2
				left*=2

				cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)
				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
				cv2.waitKey(2000)
				cv2.destroyWindow(win_name)
				break
		else:
			for (top,right,bottom,left), name in zip(face_locations, face_names):
				top*=2
				right*=2
				bottom*=2
				left*=2
				cv2.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)
				# cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255), 1)
				break

		cv2.imshow(win_name, frame)

		if cv2.waitKey(1) == ord('s'):
			break

	video.release()
	cv2.destroyAllWindows()
	return names

"""

"""
def Recognizer(details):	

	known_img = os.path.join(basedir, f"face_recognition_data\{details['email']}\{'register'}\{details['email']}.jpg")
	unknown_img = os.path.join(basedir, f"face_recognition_data\{details['email']}\{'login'}\{details['email']}.jpg")

	known_image = face_recognition.load_image_file(known_img)
	unknown_image = face_recognition.load_image_file(unknown_img)

	known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
	unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)	

	face_known_img = face_recognition.face_locations(known_image)[0]
	face_unknown_img = face_recognition.face_locations(unknown_image)[0]

	known_encoding = face_recognition.face_encodings(known_image)[0]
	unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

	match = False
	results = face_recognition.compare_faces([known_encoding], unknown_encoding)
	print("Result********", results[0])
	if results[0]:
		match = True

	return match
"""

basedir = settings.BASE_DIR

def Recognizer(details):
	known_img = os.path.join(basedir, f"face_recognition_data\{details['email']}\{'register'}\{details['email']}.jpg")
	unknown_img = os.path.join(basedir, f"face_recognition_data\{details['email']}\{'login'}\{details['email']}.jpg")
	
	if known_img and unknown_img:
		match = DeepFace.verify(known_img, unknown_img, model_name='ArcFace')

	return match['verified']