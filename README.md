
# Deploying a Flask App with MongoDB using Docker Compose

This guide will walk you through deploying a Flask application with a MongoDB database using Docker Compose.This setup includes a public network for the Flask app and a private network for MongoDB, ensuring a secure and isolated environment.

## Project Structure

```
web_app
  │
  ├────── app
  │       ├── app.py
  │       ├── Dockerfile
  │       └── requirements.txt
  └────── docker-compose.yml 
```

### Step 1: Create the Flask Application

in the directory named [`app`](/web_app/app/app.py) create the web_app/app/`app.py` file that hosting your app.
 > Using the python application provided by instructor  



### Step 2: Create the `requirements.txt` File

Inside the `app` directory, create a [`requirements.txt`](/web_app/app/requirements.txt) file to specify the dependencies needed for deploying the python app.


### Step 3: Create the `Dockerfile`

Inside the `app` directory, create a `Dockerfile` to define the Docker image for the Flask app:

```Dockerfile
  # Use the official Python image from the Docker Hub
  FROM python:3.9-slim

  # make the app directory
  RUN mkdir -p /app

  # Set the working directory in the container
  WORKDIR /app

  # Copy the current directory contents into the container at /app
  COPY .  /app

  # Install the dependencies specified in requirements.txt
  RUN pip install  -r requirements.txt

  # Make port 5000 available to the world outside this container
  EXPOSE 5000

  # Run app.py when the container launches
  CMD ["python", "app.py"]
```

### Step 4: Create the Docker Compose File

In the root of your project directory, create a `docker-compose.yml` file to define the services (Flask app and MongoDB) and their configurations:

```yaml
  version: '3.8'

  services:
    flask-app:
      build:
        context: ./app  # Path to the directory containing Dockerfile
      container_name: flask-app
      ports:
        - "5000:5000"
      depends_on:
        - mongo
      networks:
        - public
        - private
      environment:  # this variable that mentioned in the python app as"MONGO_URI"
        - MONGO_URI=mongodb://mongo:27017/database
        

    mongo:
      image: mongo:latest
      container_name: mongo
      volumes:
        - mongo-data:/data/db
      networks:
        - private

  volumes:
    mongo-data:


  networks:
    public:
      driver: bridge
    private:
      driver: bridge
      internal: yes
```
<details>
    <summary>Explanation of Docker Compose File</summary>


  - `version:` `'3.8'`: Specifies the version of Docker Compose syntax to use.
    
  - `services`: Defines the services that will be part of this application.
    
    - `flask-app`: The Flask application service.
      - `build`: Specifies the build configuration for the Flask app.
        - `context:` ` ./app`: Path to the directory containing the `Dockerfile`.
      - `container_name:` `flask-app`: Names the container `flask-app`.
      - `ports: ` `- "5000:5000"`: Maps port 5000 of the container to port 5000 on the host machine.
      - `networks`: Connects the Flask app to both the `public` and `private` networks.
      - `depends_on:` `- mongodb`: Ensures the MongoDB service starts before the Flask app.
      - `environment:` This key is used to define environment variables for a service in the docker-compose file.

    
    - `mongodb`: The MongoDB service.
      - `image:` `mongo:latest`: Uses the latest MongoDB image from Docker Hub.
      - `container_name:` `mongo`: Names the container `mongo`.
      - `networks`: Connects the MongoDB service to the `private` network.
      - `volumes:` `- mongo-data:/data/db`: Mounts the `mongo-data` volume at `/data/db` to persist MongoDB data.
    
  - `volumes`: Defines named volumes for persistent storage.
    - `mongo-data`: A volume for storing MongoDB data.

  - `networks`: Defines custom networks for the services.
    - `public`: A bridge network allowing external access.
    - `private`: A bridge network isolating the MongoDB container.
</details>


### Step 5: Build and Run the Application

- **Build the Docker Images**:
   ```bash
   docker-compose up --build
   ```

- **Run the Docker Containers**:
   ```bash
   docker compose-up
   ```

### Step 6: Access the Application

- Open your browser and go to [`http://localhost:5000`](http://localhost:5000) to see your Flask application.
- You can also check the [`http://localhost:5000/data`](http://localhost:5000/data) route to see if it retrieves data from MongoDB.



