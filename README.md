# Gen-AI-Intro(Know-Me-From-My-Resume)

Notes: 
`This uses my resume data but any person or entiry identifiers are replaced with dummy values.`
`For optimal results, provide a detailed, well-structured resume as the input document.`
`The project assumes a resume named "myresume.txt" is located in the project's root directory. Modify ingest_data.py if you need to load resumes differently.`

**Quick Start**

## Step 1: Install Requirements

`pip install -r requirements.txt`

## Step 2: Set OPEN AI Key

```sh
export OPENAI_API_KEY=<your_key>
```

## Step 3: Ingest your data

Run: `python ingest_data.py`

This builds `vectorstore.pkl` using OpenAI Embeddings and FAISS.

## Query data

Custom prompts are used to ground the answers myresume text file.

## Run Application

Run: `python app.py` from the command line to interact with your ChatGPT for your data.
Run: `python cli_app.py` to run application in a terminal window instead of a browser.

# Docker Kubernetes Containerization
High-Level Steps: I won’t go into complete production grade setup (comes with significant local setup efforts or cost at cloud), but this should be sufficient to start, this is highly customizable.

1.	Create a Dockerfile for the application
2.	Build the Docker Image
3.	Push the Image to a Registry
4.	Write Kubernetes Deployment and Service Manifests
5.	Deploy to Kubernetes

**Dockerfile (Dockerfile)**

    ```
    FROM python:3.12.2-slim 
    # Use an appropriate base image

    WORKDIR /app # I typically use /app

    # Install system-level dependencies (if you have any)
    RUN apt-get update && apt-get install -y \
    <dependency1> \
    <dependency2>  # Example:  swig 

    # Copy dependency and code files 
    COPY requirements.txt ./
    COPY ingest_data.py app.py query_data.py cli_app.py ./

    # Install dependencies
    RUN pip install -r requirements.txt 

    # Expose the port used by your Gradio app
    EXPOSE 8000

    # Define the command to start the application
    CMD ["python", "app.py"] 
    ```

**Build the Docker Image**

    ```
    docker build -t resume-qa-app:latest .
    ```
Replace resume-qa-app:latest with any desired image name and tag.

**Push the Image to a Container Registry**

•	Choices: Docker Hub, AWS ECR, Google Container Registry, etc.
    •	Log in to chosen registry.
    •	Example (Docker Hub): 
    ```
    docker tag resume-qa-app:latest your-dockerhub-username/resume-qa-app:latest 
    docker push your-dockerhub-username/resume-qa-app:latest 
    ```

**Kubernetes Manifests**

a. Deployment (deployment.yaml)

    ```
    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: resume-qa-deployment
    spec:
        replicas: 1 # Adjust scaling if needed
        selector:
            matchLabels:
                app: resume-qa
        template:
            metadata:
                labels:
                    app: resume-qa
            spec:
                containers:
                - name: resume-qa
                image: your-dockerhub-username/resume-qa-app:latest
                ports:
                - containerPort: 8000 
                resources:
                    requests:
                        memory: "256Mi"  # Example: Request 256 MB of memory
                        cpu: "500m"      # Example: Request half a CPU core 
                    limits:
                        memory: "512Mi"  # Example:  Limit to 512 MB of memory
                        cpu: "1"         # Example: Limit to one CPU core 
    # Add resource limits if needed
    ```
b. Service (service.yaml)

    ```
    apiVersion: v1
    kind: Service
    metadata:
    name: resume-qa-service
    spec:
    type: LoadBalancer  # Or 'NodePort' for local testing
    selector:
        app: resume-qa
    ports:
    - port: 80 
        targetPort: 8000
    ```

**Deploy to Kubernetes**

    ```
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

# Detailed Walkthrough

**Title: Know-Me-From-My-Resume Question-Answering System**

## Overview
This project implements a system that allows users to ask questions about the contents of a text-based resume. It leverages the following key technologies:
•	LangChain: For modular natural language processing (NLP) pipelines and interaction with language models.
•	OpenAI API: To generate comprehensive and insightful answers.
•	FAISS: For efficient similarity-based search of relevant resume sections.
•	Gradio: To build a user-friendly web interface.

## Project Structure
•	`ingest_data.py`:
    o	Loads a resume file, default is text. (supports PDF, Word, Plain Text).
    o	Splits the resume into manageable chunks for processing.
    o	Generates text embeddings using OpenAI's Embeddings API.
    o	Creates a FAISS vector store for fast similarity search.
•	`app.py`:
    o	Provides a Gradio web interface for user interaction with the system.
    o	Handles the OpenAI API key setup.
    o	Implements the core conversational question-answering logic.
•	`query_data.py`
    o	Defines functions to load the FAISS index.
    o	Provides different question-answering models based on LangChain: 
        	`basic`: Simple question-answering chain.
        	`with_sources`: Retrieves and displays relevant source sections of the resume.
        	`custom_prompt`: Employs a tailored prompt to guide the language model for HR-focused answers.
        	`condense_prompt`: Handles follow-up questions gracefully
•	`cli_app.py`
    o	Offers a simple command-line interface for the user to select a QA model and ask questions.
•	`requirements.txt`
    o	Lists the necessary Python dependencies.

## How to Use

Run the Gradio Application

Run:	`python app.py`

This will launch a web interface in your browser.
•	Paste your OpenAI API key.
•	Start asking questions about the resume.

## Optional: Command-Line Interface

Run:	`python cli_app.py`

Example Questions
•	"What is ROBINSON LUCY's top skills?"
•	"Summarize ROBINSON LUCY's experience in fraud detection."
•	"Did ROBINSON LUCY work at [Company Name]?"

## Future Improvements
•	Add support for uploading resumes directly through the web interface.
•	Explore more advanced question-answering techniques and language models.
•	Enable customization of prompts to target specific job roles and industries.
•	Setting up monitoring tools like Prometheus and Grafana