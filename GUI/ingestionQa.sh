#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

# Variables
# ---------
# The following variables are used in the script. They need to be adjusted to the specific environment.
STAGE=${STAGE:="qa"}
CLIENT_ID=${CLIENT_ID:="qftnh9tr1n2il47k8pvg6v9ro"}
CLIENT_SECRET=${CLIENT_SECRET:="fvl36lb6rjr9t6voqa5v52u97j27v2t2cib6p7vd0sr01sufdrl"}

AUTH_URL="https://auth.${STAGE}.ddfarming.de/oauth2/token"
INGESTION_URL="https://appcontroller.fc.${STAGE}.ddfarming.de/deviceapi/upload"
REFRESH_URL="https://appcontroller.fc.${STAGE}.ddfarming.de/deviceapi/images/refresh-presigned-urls"

# Check if stage is prod and adjust the URLs accordingly
if [ "${STAGE}" == "prod" ]; then
  INGESTION_URL="https://appcontroller.fc.ddfarming.de/deviceapi/upload"
fi

# Login
# -----
# The following code logs in using the client credentials and retrieves an access token, using Cognito.
echo "[x] Login with client credentials to retrieve access token"
login_response=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  "${AUTH_URL}")
access_token=$(echo "${login_response}" | jq -r '.access_token')

if [ "${access_token}" == "null" ]; then
  echo "[-] Error: Could not retrieve access token"
  echo "[-] Retrieved login response: ${login_response}"
  exit 1
fi

echo "[-] Login Response: ${login_response}"
echo "[-] Access token: ${access_token}"

# Ingestion
# ---------
# The following code uploads an image to the FieldCatcher API.
echo "[x] Ingesting image, by uploading image metadata"
ingestion_response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: ${access_token}" \
  -H "x-device-id: test" \
  -d @"${BASEDIR}/$1.json" \
  "${INGESTION_URL}")
request_id=$(echo "${ingestion_response}" | jq -r '.request_id')
image_id=$(echo "${ingestion_response}" | jq -r '.images[0].image_id')
presigned_url=$(echo "${ingestion_response}" | jq -r '.images[0].presigned_url')
ingestion_access_token=$(echo "${ingestion_response}" | jq -r '.access_token')

if [ "${request_id}" == "null" ]; then
  echo "[-] Error: Could not upload image metadata"
  echo "[x] Retrieved Ingestion response: ${ingestion_response}"
  exit 1
fi

echo "[-] Request ID: ${request_id}"
echo "[-] Image ID: ${image_id}"
echo "[-] Presigned URL: ${presigned_url}"
echo "[-] Ingestion access token: ${ingestion_access_token}"

# Upload image
# ------------
# The following code uploads the image using the presigned URL.
echo "[x] Uploading image"
curl -s -f -X PUT \
  -H "Content-Type: image/jpeg" \
  -T "${BASEDIR}/$1.jpg" \
  -v "${presigned_url}"

if [ $? -ne 0 ]; then
  echo "[-] Error: Could not upload image"
  exit 1
fi

echo "[-] Image uploaded successfully"

# Refresh presigned URLs
# ----------------------
# The following code refreshes the presigned URLs for the images, in case the upload URL has expired.
echo "[x] Refreshing presigned URL"
presigned_url_response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: ${access_token}" \
  -d "[{\"access_token\":\"${ingestion_access_token}\",\"image_ids\":[\"${image_id}\"]}]" \
  "${REFRESH_URL}")
image_id=$(echo "${presigned_url_response}" | jq -r '.results[0].image_id')
presigned_url=$(echo "${presigned_url_response}" | jq -r '.results[0].presigned_url')

if [ "${image_id}" == "null" ]; then
  echo "[-] Error: Could not refresh presigned URL"
  echo "[x] Retrieved presigned URL response: ${presigned_url_response}"
  exit 1
fi

echo "[-] Image ID: ${image_id}"
echo "[-] Presigned URL: ${presigned_url}"
