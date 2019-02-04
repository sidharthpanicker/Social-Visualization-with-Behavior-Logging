# Social visualization with Behavior Logging

Technologies Used:
1) Django for Backend Server
2) HTML, CSS, JavaScript, Ajax, D3(for visualizing) for Front End technologies

Installation Instructions:
 (Django installation using virtualenv with requirements.txt)

System Requirements:
MacOs/Linux with a good configuration (Min: 2 GB RAM)

Steps:

1) The instructions are written such that we can run the Django project in the virtual environment.

2) pip install virtualenv

3) Create a directory for the project (can give any name you wish)
cd my_project_folder

4) Start the virtual environment by executing the command below
	$ virtualenv my_project

5) Activate the virtual environment by executing
source my_project/bin/activate

6) Let’s install Django and other required libraries, there is a requirements.txt which has the requirement, so once you activate you can just install all required software using 
pip install -r requirements.txt

7) Copy the adaptiveweb folder from the zip inside my_project folder

8) Go inside the adaptiveweb folder using:
cd adaptiveweb

9) Run the Django server by running:
    	python manage.py run server

10) Server would start running at 127.0.0.1:8000 and it will be displayed in the logs.

11) You can navigate through the site.

12) Credentials for the website are:
aaa:1234 bbb:1234 ccc:1234 admin:qwerty1234

13) Once the evaluation of the project is done, execute “deactivate” which will shut down the virtualenv and delete the whole folder.

Behavioral/Persistent Logs Location in the Project:

1)	Mouse Clicks/ Post Question/Read Comments/Post Comments/View Analytics/Open Discussion: adaptiveweb/logs/mouseclicks
2)	Mouse Movements: adaptiveweb/logs/mousemovements
3)	Mouse Scrolls: adaptiveweb/logs/mousescrolls
4)	User Login/Log out: adaptiveweb/logs/userlogin

Note: Mouse Click and User Login/Log out logs are also present in the database used by the project which is sqllite3
