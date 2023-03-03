# New On YouTube App

## Project structure
This project has two major subdirectories
- client - All the user-facing frontend code
- server - Code that runs on the Heroku server

### Client
The frontend of this project is implemented in JavaScript (Typescript) and the React.js framework

### Server
The backend is implemented in Python using Flask

## Developement

### Prerequisites
- Install the latest version of node.js and the node package manager (npm) on your machine: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
- install python3 and the python package manager, pip https://www.python.org/downloads/

### Starting up the frontend 
- Navigate to 'client' 
- Use the command 'npm install' to install required node.js packages
- Use 'npm run start' in your terminal to start the development server
- The app should now be accessible via http://localhost:3000

### Starting up the backend
- Navigate to 'server'
- Install required dependencies using 'pip install -r requirements.txt'
- Start the server using 'flask run'

### Running tests
- Navigate to 'server'
- Run all tests with 'pytest'

### Running linting
- Run './run_autopep8.sh' in the root to run autopep8 and see which parts of the code still do not conform to PEP 8 standards

### Launch in Docker locally
- To run deploy in Docker locally run 'docker build -t my_image .' in the root
- Once the image has been built launch the container with 'docker run -e PORT=8080 -p 5000:8080 my_image'
- The app should now be accessible via http://localhost:5000

## CI/CD pipeline and Production

### Deployment pipeline
- The deployment pipeline is run on all commits using GitHub actions
- PEP 8 linting checks are run on all commits
- All tests can be run in the Docker container by including 'run_tests' in the commit message
- Deployment to production server can be run by including 'run_deploy' in the commit message. Note that deployment requires that:
  - 'run_tests' is also included in the commit message
  - All tests are passed
  - The commit is made on the 'main' branch

### Production application
- The production application is deployed on Heroku and is accessible via https://new-on-youtube.herokuapp.com/
- The produciton logs are accessible on the Heroku CLI by running 'heroku logs --app new-on-youtube --tail'
