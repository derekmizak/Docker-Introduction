## **Session1_Exercise1.md**

# Exercise 1: Installing Docker

**Objective:**  
Install Docker on your local machine and verify the installation.

---

## **Instructions**

### 1. Choose Your Operating System

- **Windows 10** (Pro or Enterprise)
- **macOS**
- **Linux** distribution (Ubuntu, CentOS, etc.)

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
  - Enable Hyper-V during installation if prompted.
- **macOS Users:**
  - You may need to enter your system password to authorize the installation.

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

---



