import requests

from ws.public import Service, Command, Option, ArgumentDefinition


class Search(Command):

    name = 'search'
    description = 'search github repositories'

    def available_options(self):
        return [Option('r', 'results', help='amount of results to retrieve', required=True, default=10)]

    def argument_definition(self):
        return ArgumentDefinition(min_amount=1, max_amount=1)

    def run(self):
        result = requests.get(
            '{}/search/repositories'.format(self.parent.endpoint),
            params={'q': self.arguments[0], 'per_page': int(self.options['results'])}
        ).json()
        output = [
            '{} search results:'.format(result['total_count']),
        ]
        for item in result['items']:
            output.append('{} {}'.format(item['name'], item['description']))
            output.append(item['html_url'])
            output.append('')
        print('\n'.join(output))
        # return output


class Github(Service):

    name = 'github'
    description = 'Git repository hosting service'
    endpoint = 'https://api.github.com'

    def available_commands(self):
        return [Search]
