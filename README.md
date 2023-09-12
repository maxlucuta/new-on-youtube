![Python](https://img.shields.io/badge/Python-3.8-blue?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-4.5.4-blue?style=for-the-badge&logo=typescript)
![React](https://img.shields.io/badge/React-17.0.2-blue?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.1.0-green?style=for-the-badge&logo=flask)



# New on YouTube

## Project Brief <img src="img/logoColour.png" alt="Project Logo" width="20" align="left" hspace="0">
The goal of this project is to enhance the video search experience for users by implementing a recommendation engine. This engine allows users to register their interests and receive a curated list of recommended YouTube videos, complete with summaries generated from video transcripts using ChatGPT-3. From a technical standpoint, we aim to create a user-friendly and visually appealing interface while ensuring that generating recommendations is efficient. Each user should receive new curated lists based on their previous activity, continuously improving the recommendation system to align with their interests.

## Project Structure <img src="img/logoColour.png" alt="Project Logo" width="20" align="left" hspace="0">
This project has two major subdirectories:
- **client**: Contains the user-facing frontend code.
- **server**: Contains the code that runs on the Heroku server.

### Client 
The frontend is implemented in JavaScript (TypeScript) and utilizes the React.js framework.

### Server
The backend is implemented in Python using Flask.

### Third-Party Technologies
- User and video data are stored on Apache Cassandra.
- Videos are hosted on YouTube.com.
- Video summaries are generated via OpenAI's ChatGPT-3 API.
- Video transcript retrieval and summarization tasks are stored and retrieved from Google Pub/Sub.

## Development <img src="img/logoColour.png" alt="Project Logo" width="20" align="left" hspace="0">

### Prerequisites
Before getting started, make sure you have the following installed:
- [Node.js](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and npm (Node Package Manager)
- [Python 3](https://www.python.org/downloads/) and pip (Python package manager)

### Starting Up the Frontend
To start the frontend development server, follow these steps:
1. Navigate to the 'client' directory.
2. Run `npm install` to install the required Node.js packages.
3. Run `npm run start` in your terminal.
4. The app should now be accessible at http://localhost:3000.

### Starting Up the Backend
To start the backend server, follow these steps:
1. Navigate to the 'server' directory.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Start the server using `flask run`.

### Running Tests
To run tests, navigate to the 'server' directory and run `pytest`.

### Running Linting
To check code against PEP 8 standards, run `./run_autopep8.sh` located in the root directory.

### Launch in Docker Locally
To run and deploy the app locally using Docker, follow these steps:
1. Build the Docker image with `docker build -t my_image .` in the root directory.
2. Once the image is built, launch the container with `docker run -e PORT=8080 -p 5000:8080 my_image`.
3. The app should now be accessible at http://localhost:5000.

## CI/CD Pipeline and Production <img src="img/logoColour.png" alt="Project Logo" width="20" align="left" hspace="0">

### Deployment Pipeline
The deployment pipeline is automatically triggered on all commits using GitHub Actions and can be found in the '.github' directory. It includes:
- PEP 8 linting checks on all commits.
- Running all tests in the Docker container by including 'run_tests' in the commit message.
- Deployment to the production server can be initiated by including 'run_deploy' in the commit message, provided that:
  - 'run_tests' is also included in the commit message.
  - All tests pass successfully.
  - The commit is made on the 'main' branch.

### Production Application
The production application is deployed on Heroku and is accessible at [New On YouTube App](https://new-on-youtube.herokuapp.com/). You can access production logs on the Heroku CLI by running `heroku logs --app new-on-youtube --tail`.

