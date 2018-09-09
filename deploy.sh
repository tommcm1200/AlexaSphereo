#!/bin/bash

display_usage() { 
	echo "This script packages and deploys Python 2.7 lambda function." 
	echo -e "\nUsage:\ndeploy.sh [LAMBDA_FUNCTION_NAME] [REGION]\n" 
	} 

# if less than one arguments supplied, display usage 
	if [  $# -eq 0 ] 
	then 
		display_usage
		exit 1
	fi 
 
# check whether user had supplied -h or --help . If yes display usage 
	if [[ ( $# == "--help") ||  $# == "-h" ]] 
	then 
		display_usage
		exit 0
	fi 

lambdaName=$1
regionName=$2


rm $1.zip
cd ./venv/lib/python2.7/site-packages/
zip -r9 ../../../../$1.zip *
cd ../../../../
cd ./Lambda
zip -g ../$1.zip lambda_function.py
cd ..
aws lambda update-function-code --function-name $1 --zip-file fileb://alexaSphero.zip --region $2

