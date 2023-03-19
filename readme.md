# stuendlich bot

## about

Send a message to all followers in the activitypub network (Mastodon, GotoSocial, ...) every full hour.
This Python script uses no other dependencies except core Python 3.7+.

Deployed version: [@stuendlich@cress.space](https://fedi.cress.space/@stuendlich) (German, Europe/Berlin, private)


## setup

- Get an access-token for your bot, see <https://madflex.de/setup-a-bot-on-gotosocial/>
- create a `config.json` like this:
```
{
  "access_token": "insert_access_token_here",
  "timezone": "Europe/Berlin",
  "template": "Es ist jetzt {time} Uhr.",
  "server_url": "fedi.cress.space",
  "visibility": "private"
}
```
- change `timezone`, `server_url` and `template` for your setup.
- The string in `template` is "It is now {time}." in German.
- `visibility` should be either "private" or "unlisted" - don't be rude and use public
- add a cron to trigger the script every hour, i.e.
```
0 * * * * python /path/to/stuendlich.py
```
