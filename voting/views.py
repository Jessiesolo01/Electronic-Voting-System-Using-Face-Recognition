import re, os
import logging as log
from time import sleep
from turtle import position
from unicodedata import name
import numpy as np
import datetime as dt
import cv2
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentData, Position, Candidate
# from .face_capture import face_capture
from django.conf import settings
from deepface import DeepFace

# Create your views here.

def index(request):
    # student_no = request.GET['matric_no']
    # student = StudentData.objects.get(student_no=student_no)
    # students = StudentData.objects.filter(student =student, voted='yes')

    # matric_no = request.matric_no
    # student = StudentData.objects.all(request.matric_no)
    
    # student = StudentData.objects.all(student_no=student_no)

    
    # # if student is not None:
    # #     student.voted = 'yes'
    
    

    try:
        matric_no = request.session['matric_no']
    except KeyError:
        matric_no = None
    votes = StudentData.objects.filter(voted='yes').count()

    candidates = Candidate.objects.all()
    total_candidates = len(candidates)
    # vote = []
    # students = StudentData.objects.filter(matric_no =matric_no, voted='yes').first()
    # votes = StudentData.objects.filter(matric_no =matric_no, voted='yes').count()

    # x =students.voted('yes')
    # votes = len(x)
    # vote_list = vote.append(students)
    # votes = len(vote_list)

    
    # matric_no = request.session
    return render(request, 'index.html', {'matric_no':matric_no, 'total_candidates': total_candidates, 'votes':votes})

# def signup(request):
#     username = request.POST.get('username')
#     matric_no = request.POST.get('matric_no')
#     email = request.POST.get('email')
#     phone_no = request.POST.get('phone_no')
#     faculty = request.POST.get('faculty')
#     department = request.POST.get('department')
#     lvl = request.POST.get('lvl')
#     student_model = Student.objects.get(email=email)

#     profile = StudentData.objects.create(student=student_model, id_user = matric_no)
#     profile.save()

#     if request.method == 'POST':
#         matric_no = request.POST.get('matric_no')
        
#         if Student.objects.filter(matric_no=matric_no).exists():
#             username = request.get('username')
#             matric_no = request.get('matric_no')
#             email = request.get('email')
#             phone_no = request.get('phone_no')
#             faculty = request.get('faculty')
#             department = request.get('department')
#             lvl = request.get('lvl')

#             profile2 = StudentData.objects.get(username=username, matric_no=matric_no, email=email,
#             phone_no=phone_no, faculty=faculty, department=department, lvl=lvl)

#             profile2.show()
#             if request.method == 'POST':
#                 password = request.POST.get('password')
#                 if Student.objects.filter(matric_no=matric_no, password=password).exists():
#                     return redirect('signin')
#                 else:
#                     messages.info(request, "The password doesn't match")
#                     return redirect('signup')
#             else:
#                 return redirect('signup')


#         else:
#             messages.info(request, "The Matriculation Number does not exist, try again")
#             return redirect('signup')
            
#     else:
#         return redirect('signup')

#     return render(request, 'signup.html', {'profile2': profile2})

# def signup(request):

#     if request.method == 'POST':

#         student_name = request.POST.get('student_name')
#         matric_no = request.POST.get('matric_no')
#         email = request.POST.get('email')
#         phone_no = request.POST.get('phone_no')
#         faculty = request.POST.get('faculty')
#         department = request.POST.get('department')
#         lvl = request.POST.get('lvl')
#         password = request.POST.get('password')
            
#         # student_model = StudentData.objects.get(email=email)

#         student_profile = StudentData.objects.create(email=email, student_name=student_name, matric_no = matric_no, 
#         phone_no=phone_no, faculty=faculty, department=department, lvl=lvl)

#         student_profile.save()
#         # student = StudentData.objects.filter(matric_no=matric_no)

        
#     return render(request, 'signup.html')
def face_capture(request):
    matric_no = request.session['matric_no']
    if (os.path.exists('face_recognition_data/{}/{}'.format(matric_no, 'register')) == False):
        os.makedirs('face_recognition_data/{}/{}'.format(matric_no, 'register'))
    
    directory = 'face_recognition_data/{}/{}'.format(matric_no, 'register')
    cascPath = "face_recognition_data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    log.basicConfig(filename='webcam.log', level=log.INFO)
    video_capture = cv2.VideoCapture(0)
    anterior = 0

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        # Display the resulting frame
        cv2.imshow('Face Capturing', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            check, frame = video_capture.read()
            cv2.imshow("Capturing", frame)
            cv2.imwrite(filename=f'{directory}/{matric_no}.jpg', img=frame)
            video_capture.release()
            cv2.destroyAllWindows()
            break
        # cv2.imshow('Image Capture', frame)
    video_capture.release()
    cv2.destroyAllWindows()

    matric_no

    return redirect('/logout')
    
    # return render(request, 'capture.html')



def recognize(request):
    # detail = {'email': serializer.validated_data['email']}
    basedir = settings.BASE_DIR
    matric_no = request.session['matric_no']

    if (os.path.exists('face_recognition_data/{}/{}'.format(matric_no, 'login')) == False):
        os.makedirs('face_recognition_data/{}/{}'.format(matric_no, 'login'))
    
    directory = 'face_recognition_data/{}/{}'.format(matric_no, 'login')
    cascPath = "face_recognition_data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    log.basicConfig(filename='webcam.log', level=log.INFO)
    video_capture = cv2.VideoCapture(0)
    anterior = 0

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        # Display the resulting frame
        cv2.imshow('Face Capturing', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            check, frame = video_capture.read()
            cv2.imshow("Capturing", frame)
            cv2.imwrite(filename=f'{directory}/{matric_no}.jpg', img=frame)
            video_capture.release()
            cv2.destroyAllWindows()
            break
        # cv2.imshow('Image Capture', frame)
    video_capture.release()
    cv2.destroyAllWindows()
    
    known_img = os.path.join(basedir, f"face_recognition_data\{matric_no}\{'register'}\{matric_no}.jpg")
    unknown_img = os.path.join(basedir, f"face_recognition_data\{matric_no}\{'login'}\{matric_no}.jpg")
    
    if known_img and unknown_img:
        try:
            match = DeepFace.verify(known_img, unknown_img, model_name='Ensemble')

            # if match['verified'] == True and match['distance'] < 0.5:
            if match['verified'] == True:

                request.session['recognized'] = True
                return redirect('voting')
            else:
                messages.info(request, 'Face does not match, try again')
                return redirect('signin')
        except ValueError:
            messages.info(request, "Face could not be detected. Try again")
            return redirect('signin')
    
    # return match['verified']

def profile(request):

    if request.session['matric_no']:
        matric_no = request.session['matric_no']
        student_profile = StudentData.objects.get(matric_no=matric_no)
        profileimg = student_profile.profileimg
        student_name = student_profile.student_name
        matric_no = student_profile.matric_no
        email = student_profile.email
        faculty = student_profile.faculty
        department = student_profile.department
        lvl = student_profile.lvl
        phone_no = student_profile.phone_no


        # profileimg = request.FILES.get('profileimg')
        # student_name = request.get('student_name')
        # matric_no = request.get('matric_no')
        # email = request.get('email')
        # faculty = request.get('faculty')
        # department = request.get('department')
        # lvl = request.get('lvl')
        # phone_no = request.get('phone_no')

        return render(request, 'profile.html', {'student_profile':student_profile})
    else:
        return redirect('logout')

    
def signup(request):
    if request.method == 'POST':
        matric_no = request.POST['matric_no']
        password = request.POST['password']
        student_profile = StudentData.objects.filter(matric_no = matric_no).first()
        # pk = request.matric_no
        # print(matric_no, password)

        # students = StudentData.objects.get(student_name='Jessica Solomon')
        # print(students)
        # student = auth.authenticate(matric_no=matric_no, password=password)

        if student_profile:
            # auth.login(request, student)
            request.session['matric_no'] = matric_no
            return redirect('profile')
        else:
            messages.info(request, 'Invalid Details')
            messages.info(request, 'Enter your Student Portal Login Details')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        matric_no = request.POST['matric_no']
        password = request.POST['password']
        # print(matric_no, password)

        # students = StudentData.objects.get(student_name='Jessica Solomon')
        # print(students)

        # student = auth.authenticate(matric_no=matric_no, password=password)
        student_profile = StudentData.objects.filter(matric_no = matric_no).first()

        # if student_profile is not None:
        if student_profile:
        
            request.session['matric_no'] = matric_no
            # return redirect('voting')
            return redirect('recognize')
        else:
            messages.info(request, 'Credentials Invalid')
            messages.info(request, 'Enter Student Portal Login Details')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


# @login_required(login_url='signin')
def voting(request):
    try:
        recognized = request.session['recognized']
    except KeyError:
        return redirect('recognize')
    matric_no = request.session['matric_no']
    std_details = StudentData.objects.get(matric_no=matric_no)

    if std_details and std_details.voted == 'no':
    # if std_details:
    # voted = Voted.objects.get(matric_no=matric_no)
    # voted = get_object_or_404(Voted, matric_no = matric_no)
    # if voted is None:
        positions = Position.objects.all()
        candidates = Candidate.objects.all()

        if request.method == 'POST':
            for position in positions:
                xid = "position"+str(position.id)+"a"
                pos_id = request.POST[xid]
                
                user = Candidate.objects.get(id=pos_id)
                # for candidate in user
                if user is not None:
                    user.total_vote = int(user.total_vote)+1
                    user.save()

                    student = StudentData.objects.get(matric_no=matric_no)
                    if student is not None:
                        student.voted = 'yes'
                        student.save()
                        
                    else:
                        messages.info(request, 'Student not found')
            return redirect('result')
        else:
            messages.info(request, 'Unable to cast vote')

        return render(request, 'voting.html', {'positions':positions, 'candidates': candidates, 'student_profile':std_details})
    else:
        return redirect('result')
    
# @login_required
# def dashboardView(request):
#     return render(request, "poll/dashboard.html")
''

def result(request):
    try:
        recognized = request.session['recognized']
    except KeyError:
        return redirect('recognize')
        
    matric_no = request.session['matric_no']
    # cand_name = request.GET.get('name')
    # total_vote = request.GET.get('total_vote')
    # cand_pos = request.GET.get('title')



    positions = Position.objects.all()
    # candidates = Candidate.objects.filter(cand_name=cand_name, cand_pos=cand_pos, total_vote=total_vote).first()
    candidates = Candidate.objects.all()

    
    # cand_name=cand_name
    # cand_pos=cand_pos
    # total_vote=total_vote
    context = {
        'positions':positions,
        'candidates':candidates
    }

    # vote = []
    # students = StudentData.objects.filter(matric_no =matric_no, voted='yes').first()
    # vote_list = vote.append(students)
    # votes = len(vote_list)

    # candidates = Candidate.objects.all()
    # total_candidates = len(candidates)

    return render(request, 'result.html', context)

def logout(request):
    request.session['matric_no'] = None
    auth.logout(request)
    return redirect('signin')