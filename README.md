# fork-watcher

This simple tool loops thru your repositories and watches all forks.

## Usage

Generate a Github token at https://github.com/settings/tokens and select the following scopes:
   * `repo -> public_repo`
   * `notifications`
 
 Export the token and run the program:

```bash
 export GH_TOKEN=some_token
 python3 fork-watcher.py
 ```

## Example:

```bash
$ export GH_TOKEN=some_token

$ python3 fork-watcher.py 
You are currently watching 27 repos
 * repo: dbschema
  ...watching TheLady/dbschema -> success
 * repo: mysql_generate_series
  ...watching Youlina3/mysql_generate_series -> success
  ...watching blackberry-bb/mysql_generate_series -> success
