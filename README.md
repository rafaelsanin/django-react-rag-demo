# Project Documentation
Django with React RAG demo

![alt text](demo_gif.gif)

## Overview
This project is a Docker-based setup designed to facilitate the development and deployment of a web application using Django, Django Rest Framework (DRF) and a React app served using Django, leveraging AI models, specifically focusing on the integration of Ollama for AI functionalities. The setup includes a Django-based web application (`project` service) and an Ollama service for AI model management and inference.
## Prerequisites
- Docker and Docker Compose installed on your machine.
- Basic understanding of Docker, Docker Compose, and containerization concepts.
- Familiarity with Django for managing the web application.
- Add the [Tavily](https://tavily.com/) api key (`TAVILY_API_KEY`) in the `.env` file to enhance the AI agent with web search.
## Services
The `docker-compose.yml` file defines the following services:
### Project
The main web application built with Django. It is containerized for development with live reload capabilities.
- **Build Context**: The Docker context is set to the current directory (`.`), with an argument `DEV=true` to indicate a development build.
- **Ports**: The service is exposed on port 8000 of the host.
- **Volumes**:
    - The project's root directory is mounted inside the container for live code changes.
    - Two named volumes (`dev-static-data` and `dev-nomic-data`) are used for static data and caching purposes.
- **Commands**: Executes Django management commands to wait for the database, apply migrations, and start the development server.
- **Environment Variables**: Configuration for database connection and paths for AI model caching.
- **Dependencies**: Relies on the `db` and `ollama` services to be operational.
### Ollama
A service for managing and serving AI models, using the Ollama image.
- **Image**: Uses the `ollama/ollama` Docker image.
- **Ports**: Exposes port 11435 on the host, mapping to 11434 inside the container.
- **Volumes**: A named volume (`dev-llama-data`) for caching AI model data.
- **Healthcheck**: Configured to ensure the Ollama service is healthy before other services depend on it.
- **Deploy**: Specifies resource reservations for a GPU, indicating that this service requires an NVIDIA GPU.
### DB
A service for managing the database used by the project.
- **Image**: Uses a Docker image for the database.
- **Ports**: The database service is not exposed on the host.
- **Volumes**: A named volume (`dev-db-data`) for persisting the database data.
- **Environment Variables**: Configuration for the database connection.
- **Healthcheck**: Configured to ensure the database service is healthy before other services depend on it.
## Volumes
The compose file defines named volumes for persisting data across container restarts:
- `dev-static-data`: For static assets of the web application.
- `dev-nomic-data`: For caching GPT-4 model data used by the project service.
- `dev-llama-data`: For caching AI model data used by the Ollama service.
- `dev-db-data`: For persisting the database data.
## Build and start
To run this project locally:
1. Ensure Docker and Docker Compose are installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the project directory where the `docker-compose.yml` file is located.
4. Run `docker-compose up --build` to build and start the services.
5. Use docker vscode plug-in, right click the ollama service, click `attach shell` and run the command
`ollama pull llama3` to download and cache the llm model used by the service project (Django project). 
6. Access the web application at `http://localhost:8000/admin/`.
7. At the `project_root_directory` directory run  `sudo docker compose run --rm project sh -c "python manage.py createsuperuser"` to create the admin superuser.
8. Create a user using the admin dashboard.
9. Acces the api docs at `http://localhost:8000/api/docs`, get a token using the `/api/user/token` endpoint, click on Authorize and add the token as `Token <generated token>`,
then post a url (e.g `https://react.dev/blog/2024/05/22/react-conf-2024-recap`) using the endpoint `/api/embeddings/embeddings/` to ingest the data fron the url to the db table so the agent has context to generate responses.
10. Access the web application at `http://localhost:8000/ui-chatbot/`.
## Contributing
Contributions to this project are welcome. Please follow the standard fork and pull request workflow. Ensure you test your changes before submitting a pull request.

## Contact
For questions or support, please contact the project maintainers through issue creation.