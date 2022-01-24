import requests
import json
import os


def set_token():
    """ Read token from env variable end set it """

    global token

    try:
        token = os.environ['GH_TOKEN']
    except KeyError:
        raise RuntimeError(
            'Missing Github token. Use `export GH_TOKEN=my_token`')


def get_subscriptions():
    """ Get my current subscriptions"""

    subscriptions_list = []
    page = 1

    while True:
        subscriptions = requests.get('https://api.github.com/user/subscriptions?page=%d' % page,
                                     auth=('token', token))
        subscriptions = subscriptions.json()

        # Stop looping when we went thru all pages
        if not subscriptions:
            break

        # Add subscriptions
        subscriptions_list = subscriptions_list + [subscription['full_name']
                                                   for subscription in subscriptions]

        # Increment page number
        page += 1

    print('You are currently watching %d repos' % len(subscriptions_list))

    return subscriptions_list


def get_forks(forks_url):
    """ Fetch and return forks """

    page = 1

    while True:
        # Retrieve the list of forks
        forks = requests.get(forks_url + '?page=%d' % page,
                             auth=('token', token))
        forks = forks.json()

        # Stop looping when we went thru all pages
        if not forks:
            break

        for fork in forks:
            yield {
                'full_name': fork['full_name'],
                'subscription_url': fork['subscription_url']
            }

        # Increment page number
        page += 1


def subscribe(subscription_url):
    """ Subscribe to a repository """

    # Prepare subscription payload
    payload = {
        'subscribed': True,
        'ignored': False
    }

    # Subscribe
    subscription = requests.put(
        subscription_url,
        auth=('token', token),
        data=json.dumps(payload)
    )

    return True if subscription.status_code >= 200 and subscription.status_code < 300 else False


def get_repos():
    """ Get the list of repositories excluding forks """

    page = 1

    while True:
        repos = requests.get('https://api.github.com/user/repos?page=%d' % page,
                            auth=('token', token))
        repos = repos.json()

        # Stop looping when we went thru all pages
        if not repos:
            break
        
        for repo in repos:
            if repo['fork'] is False:
                yield repo

        # Increment page number
        page += 1


def search_and_subscribe():
    """ Loop thru repositories, fetch forks and subscribe """

    for repo in get_repos():
        print(' * repo: %s' % (repo['name']))

        # Loop thru forks
        for fork in get_forks(repo['forks_url']):
            if fork['full_name'] not in current_subscriptions:
                # Attempt to subscribe
                res = subscribe(fork['subscription_url'])

                print('  ...watching %s -> %s' %
                      (fork['full_name'], 'success' if res is True else 'failed'))


def main():
    global current_subscriptions, token

    # Read token from env
    set_token()

    # Get my current subscriptions
    current_subscriptions = get_subscriptions()

    # Loop thru forks and subscribe
    search_and_subscribe()


if __name__ == '__main__':
    main()
