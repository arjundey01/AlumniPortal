# Alumni Portal (IITG SWC)

**A platform for IITG Alumni and Students to interact!**

## Installation 

#### Cloning the repository:
- Clone the repository using `git clone https://github.com/arjundey01/AlumniPortal.git`.

#### Creating a virtual environment:
- Create a python virtual environment inside the project directory using the command `python3 -m venv env`.
- To activate the environment, run `source env/bin/activate` in **Linux** and `env\Scripts\activate.bat` in **Windows**.
- To exit the virtual environment, run `deactivate`.

#### Installing dependencies:
- Activate the virtual environment
- Run `pip install -r req.txt`

#### Installing Docker:
_Note: This step is optional. Required only for the chat app for running a redis server._
- Linux:
    `sudo apt-get update`
    `sudo apt-get install docker-ce docker-ce-cli containerd.io`
- Windows:
    Follow the steps given [here](https://docs.docker.com/docker-for-windows/install/#install-docker-desktop-on-windows).
- Install Redis:
    `docker pull redis`


#### Migrating:
- Run `python3 manage.py makemigrations`
- Run `python3 manage.py migrate --run-syncdb`. _Note: Use the argument `--run-syncdb` only for installation_.


## Starting the server:
- (_Only if redis is installed_) Run `docker run -p 6379:6379 -d redis:5`. (_Use `sudo` in linux._)
- Activate the virtual environment.
- Run `python3 manage.py runserver 0.0.0.0:8000`.
- The site will be available at http://localhost:8000/.

__NOTE:__ Use `python` instead of `python3` on windows.

## UI Design:
- [Figma - SWC Alumni Portal](https://www.figma.com/file/YvVwese9d4ACystZHHYa0E/SWC-alumni-portal?node-id=68%3A301)
