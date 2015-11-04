Place JSON configuration files here with credentials/tokens/URLs/etc. for all
of the encoders and channels you wish to use.

Naming convention is `channelOrEncoderName-config.json`, and the JSON structure
should match the `requiredParams` attribute of the chanenel it's for.

These are currently used in the testing suite, and not really anywhere else.
In the future, automated compilation tools may use this to template credentials
directly into any binaries produced - who knows!
