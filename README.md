# Backend for Smart Room App

## Overview

This repository contains the backend code for Smart Room App. The backend serves as the intermediary layer between the frontend and the perception layer (Openhab), providing a set of APIs implemented in Flask. The application follows the Gitflow methodology, and its deployment is managed through [fly.io](https://fly.io/). The codebase also includes a `.github` folder with a pipeline that automates the deployment process whenever changes are merged into the main branch.

## Table of Contents

- [Architecture](#architecture)
- [Endpoints](#endpoints)
- [Deployment](#deployment)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The backend is structured as a Flask API, facilitating communication between the frontend and the perception layer. The Gitflow methodology was adhered to during development, ensuring a structured approach to branching and merging. The application's architecture can be visualized as follows:

![Architecture Diagram](https://github.com/jhonatansossa/SmartRoomBackend/assets/74026540/c37c8290-4173-43ca-a25c-e38072271358)


## Endpoints

The backend exposes 17 endpoints to cater to various functionalities. 

For detailed information on each endpoint and how to use them, refer to the [API Documentation](https://smart-room.fly.dev/#/).

## Deployment

The backend is deployed on [fly.io](https://fly.io/), providing a scalable and reliable infrastructure. Automatic deployment is handled through the included GitHub Actions pipeline located in the `.github` folder. Whenever changes are merged into the main branch, the pipeline triggers deployment to ensure a seamless update process.

For detailed instructions on deploying the backend manually, refer to the [Deployment Guide](https://fly.io/docs/languages-and-frameworks/python/).

## Development

If you want to contribute or set up the backend for local development, follow these steps:

1. Clone the repository: `git clone https://github.com/jhonatansossa/SmartRoomBackend.git`
2. Install WSL if you are using Windows
3. Install MySQL [MySQL Installation Guide](https://www.geeksforgeeks.org/how-to-install-mysql-on-linux/)
4. Import the database backup (allow the access to the root user without password first) `mysql -u root -p openhab2 < backup/openhab2.sql`
5. Create a new virtual environment using python 3.8 (conda is recommended) `conda create --name <env_name> python=3.8`
6. Activate virtual environment `conda activate <env_name>`
7. Download the .env file from DSD main page documentation and replace it in the project folder
8. Install dependencies: `pip install -r requirements.txt`
9. Run the development server: `flask run --host=0.0.0.0`
10. Access the API at `http://localhost:5000`.