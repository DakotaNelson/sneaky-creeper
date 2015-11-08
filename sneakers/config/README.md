Place JSON configuration files here with credentials/tokens/URLs/etc. for all of the encoders and channels you wish to use. The name of these files should be '[encoder/channel name]-config.json'.

For example, the Twitter channel config file should be named `'twitter-config.json'`.

As for formatting, the json file should be an object with a single key which is the encoder/channel name, with the value as an object with the key: value parameter pairings required for the encoder/channel.

For example for the Twitter channel, the json file should look like:
```
{
    "twitter": {
        "key": "atwitterapikey",
        "secret": "atwitterapisecret",
        "name": ... ,
        ...,
    }
}

```