import unicodedata

def remove_accents(input_str):
    # Normalize the input string to decompose the accents
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filter out the combining characters (accents)
    return ''.join([char for char in nfkd_form if not unicodedata.combining(char)])
