# Lab Environment Setup

This workshop uses a **container-based lab environment** managed by Docker.  
All labs are controlled through a single **Lab Hub** web interface.

You only need to complete this setup **once**.

---

## Requirements

Before starting, ensure you have:

- **Git**
- **Docker Desktop**
  - Windows: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
  - macOS: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
  - Linux: Docker Engine + Docker Compose plugin

Verify Docker is installed and running:

```bash
docker version
docker compose version
```

## Step 1 — Clone the Lab Repository

Clone the wwc2025-labs repository and enter the directory:

```bash
git clone https://github.com/profzeller/wwc2025-labs.git
cd wwc2025-labs
```

This repository contains:

- The WWC 2025 Lab Hub
- All lab container images
- A single Docker Compose configuration


## Step 2 — Build the Lab Images

Build the hub and all lab images:

```bash
docker compose --profile labs build
```

Notes:

- This may take several minutes the first time
- You only need to rebuild if the labs change


## Step 3 — Start the Lab Hub

Start the hub container:

```bash
docker compose up -d hub
```

Once started, open your browser and go to:

[http://localhost:8080](http://localhost:8080)

You should see the **WWC 2025 Lab Hub interface**.

## Step 4 — Launch Lab 1

From the Lab Hub interface:

1. Locate **Lab 1 — CIA Triad Scenario Matcher**
2. Click **Start & Launch**

What happens automatically:

- Any other running labs are stopped
- Lab 1 is started in the background
- The lab opens in a new browser tab when ready


## Stopping Labs
You can stop all labs in either of the following ways:

### Option 1 — From the Hub

Click **Stop All Labs** in the Lab Hub interface.

### Option 2 — From the Terminal

Stop everything:

```bash
docker compose down
```

## Important Notes

- Only **one lab runs at a time**
- Do **not** start labs manually with ```docker run```
- Always use the **Lab Hub** to start and stop labs
- No environment variables or configuration files are required

## Troubleshooting

### Hub does not load

- Confirm Docker is running
- Ensure port **8080** is not already in use

### Lab does not start

Verify images exist:

```bash
docker images | grep wwc2025
```

Rebuild if needed:

```bash
docker compose --profile labs build
```

### Reset everything

If something feels broken:

```bash
docker compose down
docker compose up -d hub
```