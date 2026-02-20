# TRS Monitoring Service

TRS Monitoring Service is a robust solution for monitoring news streams.

## 🛠️ Getting Started

Follow the steps below to set up and run the TRS Monitoring Service using Docker

### ⚙️ Configure Environment Variables

Copy the example environment file and fill in the necessary values:

```bash
cp .env.example .env
```

Edit the `.env` file to set your environment variables. You can use the default values or customize
them as needed.

Also, make sure to configure the `docker-compose.yml` file if necessary.

### 🐳 Build and Run the Docker Container

Start the Docker container with the following command:

```bash
docker compose up --build -d
```

This command will build the Docker image and start the container.
