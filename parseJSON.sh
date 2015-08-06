#!/bin/bash
if [ $# == 1 ]
then
	if [ $1 == "location" ]
	then
		cat .raw.userlocation.json | jq ".[]" | sed 's/"//g' > .userlocation.json
	elif [ $1 == "weather" ]
	then
		cat .raw.weather.json | jq ".[]" | sed 's/"//g' > .weather.json
	fi
else
	echo "Sorry!"
fi