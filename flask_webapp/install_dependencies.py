import os
import platform
import subprocess

def install_dependencies():
    project_directory = './'
    os.chdir(project_directory)

    packages = [
        'Flask',
        'flask-cors',
        'Flask-SQLAlchemy',
        'python-decouple',
        'mysql-connector-python'
    ]

    for package in packages:
        subprocess.call(['pip', 'install', package])

if __name__ == '__main__':
    install_dependencies()
