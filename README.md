# publicsuffixlist-api
fastAPI endpoint for public suffix list - mozilla PSL


# Run the container

````
docker run -it -p 8000:8000 -e MANUAL_ADD="mylocaldomain.local" smck83/publicsuffixlist-api
````
# Hit the API

`https://localhost:8000/getPsl?domain=calendar.google`


# Get the response

````
{
  "sourceDomain": "calendar.google",
  "parentDomain": "google",
  "isTld": false,
  "tldDomain": "google",
  "isOrgLevel": true,
  "comment": [
    "google : Charleston Road Registry Inc.",
    "https://www.iana.org/domains/root/db/google.html"
  ],
  "orgLevelDomain": "calendar.google"
}

````
