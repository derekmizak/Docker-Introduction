## **Session1_Exercise1.md**

# Exercise 1: Installing Docker

**Objective:**  
Install Docker on your local machine and verify the installation.

---

## **Instructions**

### 1. Choose Your Operating System

- **Windows 11** (64-bit: Home, Pro, Enterprise, or Education version 22H2 or higher)
- **Windows 10** (64-bit: Home or Pro with build 19043 or later)
- **macOS** (latest version and previous two releases supported)
- **Linux** distribution (Ubuntu, CentOS, etc. with at least 4GB RAM)

### 2. Download Docker

- **Windows/macOS:**
  - Visit the [Docker Desktop Download Page](https://www.docker.com/products/docker-desktop).
  - Download the installer for your operating system.
- **Linux:**
  - Follow the official installation guide for your distribution:
    - [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
    - [CentOS](https://docs.docker.com/engine/install/centos/)
    - [Other distributions](https://docs.docker.com/engine/install/)

### 3. Install Docker

- Run the installer and follow the on-screen prompts.
- Accept the license agreement when prompted.
- **Windows Users:**
  - **WSL 2 Backend (Recommended):** Docker Desktop now uses WSL 2 by default. Ensure WSL version **2.1.5 or later** is installed.
    - To check your WSL version: `wsl --version`
    - To update WSL: `wsl --update`
  - **Hyper-V Backend:** Available as an alternative, but WSL 2 offers better performance.
  - Enable virtualization in your BIOS/UEFI settings if not already enabled.
- **macOS Users:**
  - You may need to enter your system password to authorize the installation.
  - On Apple Silicon (M1/M2/M3), Docker Desktop runs natively.

### 4. Post-Installation Steps

- **Linux Users:**
  - **Manage Docker as a Non-Root User:**
    - Run the following command to add your user to the `docker` group:
      ```bash
      sudo usermod -aG docker $USER
      ```
    - Log out and log back in for the changes to take effect.

### 5. Verify Installation

- Open a **terminal** or **command prompt**.
- Run the following commands to check your Docker installation:
  ```bash
  docker version
  docker info
  ```
- **Expected Output:**
  - `docker version` displays the Docker client and server version numbers.
  - `docker info` provides system-wide information about the Docker installation.

### 6. Troubleshooting

- If you encounter issues:
  - Refer to the [Docker Troubleshooting Guide](https://docs.docker.com/config/daemon/).
  - Ensure that virtualization is enabled in your system BIOS/UEFI settings.
  - Check that your user has the necessary permissions.

---

## **Expected Result**

- Docker is successfully installed and running on your machine.
- You can execute Docker commands without encountering errors.

---

## **Notes**

- **Stay Updated:** It's recommended to keep Docker updated to the latest version for security patches and new features.
- **Docker Desktop vs. Docker Engine:**
  - **Docker Desktop** is used for Windows and macOS.
  - **Docker Engine** is installed directly on Linux systems.
- **Commercial Licensing (2025):**
  - Docker Desktop remains **free for personal use, education, and small businesses**.
  - Organizations with **more than 250 employees OR more than $10 million in annual revenue** require a paid Docker subscription for commercial use.
  - Docker Engine (Linux) remains free and open source.
- **WSL 2 Requirements:**
  - Windows users must have WSL version **2.1.5 or later** for optimal Docker Desktop performance.
  - WSL 2 provides better performance and resource management compared to Hyper-V.

---



