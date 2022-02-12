import requests

def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_pokemon_list(params={}):
    response = generate_request('https://pokeapi.co/api/v2/pokedex/national', params)
    
    pokemonListName = []
    if response:
       pokemonList = response.get('pokemon_entries')

       for value in pokemonList:
           pokemonListName.append(value.get('pokemon_species').get('name'))

       return pokemonListName

    return pokemonListName