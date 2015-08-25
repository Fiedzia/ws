import requests

from ws.public import Service, Command, Option


class SearchRepos(Command):
    pass


class Search(Command):

    def available_options(self):
        return [Option('q', 'query', help='query string', required=True)]

    def run(self):
        result = requests.get(
            '{}/search/repositories'.format(self.parent._meta.endpoint),
            params={'q': self.options['q'], 'per_page': 10}.json()
        )
        output = [
            '{} search results:'.format(result['total_count']),
        ]
        for item in result['items']:
            output.append('name: ' + item['name'])
            output.append('description: ' + item['description'])
            output.append('url: ' + item['url'])
        return output


class Github(Service):

    name = 'github'

    def help(self):
        return 'Github service cli'

    def available_commands(self):
        return [Search]

    def __init__(self, env):
        super().__init__(self, env)
        self._meta.endpoint = 'https://api.github.com'
