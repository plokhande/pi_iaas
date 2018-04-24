# pi_iaas
Code to generate value of PI compliant with the IaaS best practices

## FLASK
Flask is used for the API code. Complete code resides in pi_flaskapp.py under the pi_app folder. 

Consists of mainly two methods of API endpoints
POST /pi_job 
This takes one argument, the number of digits upto which the value of PI has to be calculated.

GET /pi_job/{job_id}

## FLASK RESTPLUS
Flask restplus which is an adaption of swagger is used for providing documentation for this application.

## DOCKER
Docker has been used to provide containerization and infrastructure-as-a-code servie.