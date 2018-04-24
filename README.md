## IAAS solution for PI 
Code to containerize a flask app that generates the value of PI upto a given number of digits. 

## DOCKER

Docker has been used to provide containerization and infrastructure-as-a-code service.

Docker compose file is provided to execute the flask app in a container. It is configured to expose the API port from the container to that of the hostip/localhost:5000.

Installation steps:

1. Clone this repo by running:

   ```bash
   git clone --recursive https://github.com/plokhande/pi_iaas
   ```

2. Install Docker on the host system as described in [Installing Docker] (https://docs.docker.com/install/).

3. Execute the below command to setup the flask-app container using docker-compose

   ```bash
   docker-compose up 
   ```

4. Access the application on (hostip:5000/)

## FLASK

Flask is used for the API code. Complete code resides in pi_flaskapp.py under the pi_app folder. 

Consists of mainly three methods for API endpoints

- **POST /pi_job**

This takes one argument, the number of digits upto which the value of PI has to be calculated. It returns a uniquely generated job_id, which can be used for further references to fetch the status of the job. 

    a. The below json is returned on succesful trigger of the job.

        {
            "success": true,
            "job_id": 0
        }

    b. On failure, you get the response as 

        {
            "success": false,
            "error": 'Error message'
        }

- **GET /pi_job/{job_id}**

This method takes the job_id generated by the post method as input and returns 

    a. if the job is 'in-progress' : below json is returned

        ```
        {
            success: true,
            job_id: "0",
            digits: 435,
            status: "In-progress",
            time_elapsed: "4 seconds"
        }
        ```
    b. if the job is in 'completed' state: below json is returned

        ```
        {
            success: true,
            job_id: "0",
            digits: 435,
            status: "complete"
        }
        ```

    c. In case of invalid job_id being passed as input, below response is returned

        ```
        {
            success: false,
            job_id: "4",
            error: "Job does not exist"
        }
        ```

- **GET /download_pi_job/{job_id}**

This method takes the job_id generated by the post method as input and downloads a text file to the system containing the results of the corresponding PI value.

## FLASK RESTPLUS

Flask restplus which is an adaption of swagger is used for providing documentation for this application. This gives the ease of documentation with added benefit of testing the API.

Complete documentation for the API usage can be found at (hostip:5000/) - where the flask app is running. This page also provides with options to test the API with the click of a button. Example screenshots can be found below

**API home screen**

![usage](screenshots/API_home_screen.png)

**POST /pi_job**

![usage](screenshots/post_pi_job.png)

**GET /pi_job/{job_id}**

![usage](screenshots/get_pi_job.png)

**GET /download_pi_job/{job_id}**

![usage](screenshots/get_download_pi_job.png)

## MONITORING

Service and container monitoring has not been addressed in the code yet. This can be achieved as below.

    a. configuring docker swarm or kubernetes to reduce the down-time of the container services.

    b. installing zookeeper to monitor the background service of docker containers

## CLOUD ALTERNATIVE

AWS provides a series of services to achieve similar architecture to provide a much better and optimum solution.
- ECS for docker containerization.
- Lambda for serverless and faster computation alongwith scalability solution.
- Cloudwatch for monitoring and alerting.