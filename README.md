# publicsuffixlist-api
fastAPI endpoint for public suffix list - mozilla PSL.

This container downloads https://publicsuffix.org/list/public_suffix_list.dat on build. Once running, you can query the API to understand if a domain is  TLD, Organisation Level Domain or Subdomain.

You can add your own custom suffix to the list using the `MANUAL_ADD` environment variable.

# Run the container

````
docker run -it -p 8000:8000 -e MANUAL_ADD="mylocaldomain.local" smck83/publicsuffixlist-api
````
# Hit the API

## Example 1

### The request
`https://localhost:8000/getPsl?domain=calendar.google`


### The response

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
## Example 2

### The request
`https://localhost:8000/getPsl?domain=github.mylocaldomain.local`


### The response

````
{
  "sourceDomain": "github.mylocaldomain.local",
  "parentDomain": "mylocaldomain.local",
  "isTld": false,
  "tldDomain": "mylocaldomain.local",
  "manuallyAdded": true,
  "orgLevelDomain": "github.mylocaldomain.local",
  "isOrgLevel": true,
  "comment": [
    "Manually added"
  ]
}

````
