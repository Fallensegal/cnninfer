# CNN-Infer

## Table of Content

- [Overview](#overview)
- [Pre-requisites](#pre-requisites)
- [Start the Application](#starting-the-application)


## Overview

CNN-Infer is an experimental deployment exploring the use of modern infrastructure technology stack to develop, and deploy machine learning application in an expeditious manner. The objective is to infer a subset of the COCO images using a select number of CNN architecture models.

## Pre-requisites

1. Install `Docker`
    - Windows: https://docs.docker.com/desktop/install/windows-install/
    - Mac: https://docs.docker.com/desktop/install/mac-install/
    - Linux: https://docs.docker.com/engine/install/ubuntu/

2. Install `Kubernetes` (Minikube)
    - Windows/MacOS/Linux: https://minikube.sigs.k8s.io/docs/start/

3. Install `Helm`
    - Windows/MacOS/Linux: https://helm.sh/docs/intro/install/

4. Install `kubectl`
    - Windows: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
    - MacOS: https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/
    - Linux: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/



## Starting the Application:

> **Note**: I will be assuming the user OS is `MacOS` or `Linux`. As a result, the directions will be specific to the respective OS

> **Note**: 

1. Install the pre-requisites
2. Clone this application repo: https://github.com/Fallensegal/cnninfer
3. Install `Helm` dependencies:
    - Make sure you are in the project root directory
    - Add the following `Helm` chart repo as part of the `Helm` tool

    ```bash
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    ```
    - Install `Helm` dependencies

    ```bash
    helm dependency build ./deploy
    ```

4. Start `Minikube`

    ```bash
    minikube start
    ```
    *Expected Output (Similar Output):*
    ```bash
    😄  minikube v1.32.0 on Debian bookworm/sid
    ✨  Using the docker driver based on existing profile
    👍  Starting control plane node minikube in cluster minikube
    🚜  Pulling base image ...
    🔄  Restarting existing docker container for "minikube" ...
    🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
    🔗  Configuring bridge CNI (Container Networking Interface) ...
    🔎  Verifying Kubernetes components...
        ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
    🌟  Enabled addons: storage-provisioner, default-storageclass
    🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

    ```

5. Start the application


## Docs
The official Polylith documentation:
[high-level documentation](https://polylith.gitbook.io/polylith)

A Python implementation of the Polylith tool:
[python-polylith](https://github.com/DavidVujic/python-polylith)
