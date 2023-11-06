# All-In-One SBRP Portal [G4-T4]

## About All-In-One SBRP Portal

The SBRP Portal serves as a tool for All-In-One staff to apply for open positions within the company.
From the portal, staff members are able to see the skills they have acquired and how relevant their skills are to each role opening.

## Features

In this first release, we have rolled out the following features.

### User Stories

1. **[Core]** As a member of the HR team, I want to view all the role listings, so that I can see the roles listings that have been created.
2. **[Core]** As a member of the HR team, I can add new open roles so that all staff members are aware of new open roles available.
3. **[Core]** As a member of the HR team, I can modify existing open roles so that all open roles contain the latest and most accurate information.
4. **[Core]** As a member of the HR team, I want to view the profile of role applicants, so that I can make informed decisions during recruitment.
5. **[Core]** As a staff member, I can view all open roles, so I can conveniently know the open roles available.
6. **[Core]** As a staff member, I want to be able to filter the role listings so that I can easily view roles according to my desired queries.
7. **[Core]** As a staff member, I can know the compatibility of my skills with that of the role’s requirements, so that I know if I am suitable for the role.
8. **[Core]** As a staff member, I can apply for an open role, so that I have a chance for a role change at my workplace.
9. **[Secondary]** As a staff member, I can view my skills profile, so that I can conveniently get an overview of my current abilities at a glance.
10. **[Secondary]** As a staff member, I can cancel my application for an open role, so that I can withdraw my application in the case that I am no longer interested or I have already gotten another position.

## Required Software On Your Machine

1. VSCode (or text-editor of your choice)
2. Python Version 3.11

## Executing the program

1. Download the zip from this git repository [GitHub Repo](https://github.com/darylmatt/spm_g4t4)
2. Unzip the folder and open the package in VSCode
3. Ensure that Python and Pylance extensions are installed on your VSCode
4. Navigate to the flask_webapp folder and paste the provided .env file
5. Install the corresponding dependencies in the terminal by calling the following commands:

   - `pip install Flask`
   - `pip install flask-cors`
   - `pip install flask_sql_alchemy`
   - `pip install python-decouple`
   - `pip install my-sql-connector-python`

6. Run the app.py code in your terminal and access the webpage via http://localhost:5500. You should be automatically redirected to the login page http://localhost:5500/login.
