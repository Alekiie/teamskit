Teamskit is a Web application project aimed at managing users and tasks for an organisation.Think of it as a system where:
## Admins
- They have full access to users and tasks.  
- They have full control,can create,read,update and delete users and tasks from the dashboard.  
- They can assign and reassign tasks to different users.
- They can view the recent activity on tasks from the dashboard

## Managers
- They can only view users.
- They can create and update tasks to different users.
- They can reassign tasks. 
- They can view the recent activity on tasks from the dashboard.

## Members
- They can see the tasks they have been assigned to undertake.
- They can update the status of the tasks they are doing.
- They can see the recent activity on tasks from the dashbord.

## Tech stacks
This project has been developed using:
1. Frontend - ReactJS ,TailwindCss,Framer motion,Lucid Icons and Vite.
1. Backend - Django,MySQL and JWT.

## Running the project
For the backend:
> Requirements:  
> 1. Python3
> 2. MySQL or Mariadb
1. Clone this repo:
``` bash
git clone https://github.com/alekiie/teamskit
```
2. Navigate to the project directory:
```bash
cd teamskit
```
3. Create a virtual environment:
```bash
python -m venv .venv
```
4. Activate the virtual environment:
```
source .venv/bin/activate
```
5. Install the required modules:
```bash
pip install -r requirements.txt
```
6. Create a database:
On your terminal run:
```bash
mysql -u root -p
```
Enter your MYSQL password then run:
```mysql
create database teamskit;
```
7. Run the project:
```bash
python manage.py runserver
```

The project runs on port 3000.

## Endpoints to expect
| Endpoint | Methods allowed |
|--------- | ----------------|
| `/api/users/` | GET,POST,PUT,DELETE (Based on user permissions) |
| `/api/tasks/` | GET,POST,PUT,DELETE (Based on your permissions) |
| `/api/auth/login/` | POST |
| `/api/tasks/recent/` | GET |
| `/api/tasks/:id/assign_task ` | POST (Based on user permisssion) |
|




The project API documentation is available on: `/api/schema/swagger-ui`


## Environmental Variables
On the `.env` file, enter the values for the following variables":

```
DB_NAME=teamskit
DB_USER=yourdatabaseusername
DB_PASSWORD=yourdatabasepassword
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=yoursecretkey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, localhost, teamskit.local

```

