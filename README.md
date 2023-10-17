
# Project Title: ChatApp using Django and Rest Framework with jwt authentication and webscocket intigration

ChatApp is a secure and feature-rich chat application developed using Django and Rest Framework. With integrated JWT authentication, users can safely add friends and engage in private chat conversations. Experience real-time communication with ease and confidence

How to run this project step by step guide.

step1: Download this project on your machine.  

step2: Create a virtual environment and activate it.

step3: Install all the requirements using reqt.txt file.
        
        pip install -r reqt.txt


step4: now migrate this project by using:

        1. python manage.py makemigrations
        2. python manage.py migrate

step5: Now simply open the terminal and run the app using:

        python manage.py runserver

This app is very inter dependent so for testing first ccreate a super user by using:

        python manage.py createsuperuser

then continue with step5.

If you are testing this app in POSTMAN, then simply get the url form the terminal and ensure the url path from urls.py file and start with sign_up. one user signedup then user can get verified with otp. Its a fully functional project for chat application backend it has functionalities like:
        
1. Signup

        http://127.0.0.1:8000/account/sign_up/

2. Account Verification

        http://127.0.0.1:8000/account/otp_verification/

3. Singin

        http://127.0.0.1:8000/account/Sing_in/

4. Singout

        http://127.0.0.1:8000/account/sign_out/

5. Online users: will list the users who are already ur friend and active at the time.

        http://127.0.0.1:8000/chat/online_users/

6.  Friend Suggestions based on ur interests.

        http://127.0.0.1:8000/account/friend_recommendations/

7. Start Chat to a friend.

        http://127.0.0.1:8000/chat/start/

There are some more functionalitis in this like add user from suggested users, sending requests, accepting requests, deleteing requests, Adding and Updating interests, and many more 

For stating a chat with any friend You have: 


8. chatroom connection:
        
        ws://127.0.0.1:8000/ws/chat/VXy2c8ZJ/?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3Nzc3NjQxLCJpYXQiOjE2OTc1MTg0NDEsImp0aSI6Ijg1MDUyNmU4Y2QzYzQxZjk4YzI5NWJhNTM0MjcxMTkxIiwidXNlcl9pZCI6NX0.yQO_cHohYEyKvQAqFoQcQohxHRaOMgjjtrBbVaDNU6k
    

For conetion in chatroom u have to use:

             ws://127.0.0.1:8000/ws/chat/

and chatroom name u will recive after applying step 7. And in params u have to pass your access_token, S the final urls looks like:

             ws://127.0.0.1:8000/ws/chat/room_name/?access_token


With thses details you are ready to go with this project. 





