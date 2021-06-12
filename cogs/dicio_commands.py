import discord
from discord.ext import commands
import requests
from dicio import Dicio
from bs4 import BeautifulSoup
import random


dicio = Dicio()
class Dicio_Commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='siginificado', aliases=['sf'], help='Siginificado da palavra')
    async def meaning(self, ctx, word):
        search = get_search(word)
        await ctx.send(f"Mostrando siginificado de {search.word}:")
        if len(search.meaning) == 0:
            await ctx.send(search.etymology)
        else:
            sigstr = '^'.join(map(str, search.meaning))
            await ctx.send(sigstr.replace('^', '\n'))

    @commands.command(name='etimologia', aliases=['et'], help='Origem da palavra')
    async def etymology(self, ctx, word):
        search = get_search(word)
        await ctx.send(search.etymology)

    @commands.command(name='sinônimos', aliases=['si'], help='Palavras equivalentes')
    async def synonym(self, ctx, word):
        search = get_search(word)
        synonyms = list()
        for W in search.synonyms:
            synonyms.append(W.word)
        synonyms_str = ', '.join(map(str, synonyms))
        await ctx.send(synonyms_str)

    @commands.command(name='classe gramatical', aliases=['cg'], help='Classe gramatical')
    async def _class(self, ctx, word):
        search = get_search(word)
        await ctx.send(search.extra['Classe gramatical'])

    @commands.command(name='silabar', aliases=['ss'], help='Divisão silábica')
    async def spelling(self, ctx, word):
        search = get_search(word)
        await ctx.send(search.extra['Separação silábica'])

    @commands.command(name='plural', aliases=['pl'], help='Plurais')
    async def plural(self, ctx, word):
        search = get_search(word)
        await ctx.send(search.extra['Plural'])

    @commands.command(name='feminino', aliases=['fm'], help='Versão feminina')
    async def feminino(self, ctx, word):
        search = get_search(word)
        await ctx.send(search.extra['Femininos'])

    @commands.command(name='exemplo', aliases=['ex'], help='Um exemplo')
    async def example(self, ctx, word):
        search = get_search(word)
        examples = search.examples
        await ctx.send(random.choice(examples))


def get_query(word):
    URL = 'https://www.dicio.com.br/pesquisa.php?q={}'
    r = requests.get(URL.format(word))
    if len(r.history) != 0:
        q = word
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        q = soup.find('ul', class_='resultados').li.a['href'].replace('/', '')
    return q

search = None
def get_search(word):
    global search
    word = get_query(word)

    if search == None:
        search = dicio.search(word)
        return search

    else:
      if search.word.upper() == word.upper():
          return search
      else:
          search = dicio.search(word)
          return search

def setup(bot):
    bot.add_cog(Dicio_Commands(bot))
