# YouTube Recommendations App

## Project Structure
This project has two major subdirectories
- client - All the user-facing frontend code
- server - Code that is expected to run on the AWS server

### client
The frontend of this project is implemented in JavaScript (Typescript) and the React.js framework

### server
The backend is implemented in Python using Flask

## Developement

### Prerequisites
- Install the latest version of node.js and the node package manager (npm) on your machine: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
- install python3 and the python package manager, pip https://www.python.org/downloads/
- I recommmend editing using VS-Code and its integrated terminal
- create your own branch of this repository and clone it to your machine

### starting up the frontend 
- Navigate to 'client' 
- Use the command 'npm install' to install required node.js packages
- Use 'npm run start' in your terminal to start the development server
- The app should now be accessible via http://localhost:3000;
- The server test should not yet be working!

### starting up the backend
- Navigate to 'server'
- Create a python virtual environment: 'python3 -m venv venv' (this uses the python utility 'venv' to create a virutal environment named 'venv')
- N.B. using a virtual environment enables all our python packages to be installed in the context of *this project* as opposed to your entire machine.
- Activate your virtual environment using 'source venv/bin/activate'
- The command prompt should now be prepended with '(venv)'
- Install required dependencies using 'pip install flask flask-cors python-dotenv'
- Start the server using 'flask run'
- The server test from the frontend should be successful!
