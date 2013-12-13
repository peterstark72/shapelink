Shapelink
=========

This Python module lets you access the Shapelink.com API.

First you need an API-key and Secret as described at http://developer.shapelink.com/index.php/Get_an_API_key

All method arguments are keyword arguments, though required arguments come first and are in the order listed by the API documentation.

All methods return the parsed Python equivalent of the JSON response returned by the corresponding API method, if there is a response.


#Examples

Authentication. 

Place API credentials in a file called "shapelink_secrets.json" with the following (json) format:

```
{
    "APIKEY" : {YOUR API KEY},
    "SECRET" : {YOUR API SECRET}
}
```

Read credentials from the file and create an API-object.

```python
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 
    'shapelink_secrets.json')

api = shapelink.get_api_fromsecrets(CLIENT_SECRETS)
```

To get a user, you need the user's username and password (Shapelink does not support OAuth).

```python
user = shapelink.get_user(api, username, password)
```

Getting user's diary, challenges, profile and activities. 

```python

user.diary()

user.joined_challenges()

user.profile()

user.activities("cardio")

```