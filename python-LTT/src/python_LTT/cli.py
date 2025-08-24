import click
from .utils import call_ollama

@click.command()
@click.argument("message")
def chat(message):
    response = call_ollama(message)
    click.echo(response)