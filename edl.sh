#!/bin/bash

help()
{
   echo "Perform basic Earthdata Login user token operations. Works with PROD."
   echo
   echo "Syntax: edl.sh [-u|c|r|d|h]"
   echo "options:"
   echo "  u EDL Userid"
   echo "  c Create user token"
   echo "  r Read user tokens"
   echo "  d Delete user token"
   echo "  h Print this help"
   echo
}

operation="None"

while getopts ":crd:u:h" option; do
   case $option in
      c)
         operation="create"
         ;;
      r)
         operation="read"
         ;;
      d)
         operation="delete"
         token=$OPTARG
         ;;
      u)
         userid=$OPTARG
         ;;
      h)
         help
         exit;;
     \?)
         echo "Error: Invalid option"
         exit;;
   esac
done

if [ -z "$userid" ];
then
  read -p "EDL Username: " userid
fi
read -sp "EDL Password for '$userid': " pwd; echo

s=$(echo -n "$userid:$pwd"|base64)
auth_hdr="Authorization: Basic $s"

base_url="https://urs.earthdata.nasa.gov"

JQ=$(command -v jq)
if [ -z "$JQ" ]; then
  JQ=cat
fi

if [ "$operation" = "create" ]; then
  curl -s -X POST -H "$auth_hdr" "$base_url/api/users/token" | $JQ
elif [ "$operation" = "read" ]; then
  curl -s -H "$auth_hdr" "$base_url/api/users/tokens" | $JQ
elif [ "$operation" = "delete" ]; then
  curl -s -X POST -H "$auth_hdr" "$base_url/api/users/revoke_token?token=$token" | $JQ
else
  echo "Error: No operation specified"
fi
