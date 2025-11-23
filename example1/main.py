import random
import requests
from bs4 import BeautifulSoup

URL = 'https://www.imdb.com/chart/top'

def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    movietags = soup.select('td.titleColumn')
    inner_movietags = soup.select('td.titleColumn a')
    ratingtags = soup.select('td.imdbRating strong')

    def get_year(movie_tag):
        year = movie_tag.find('span', class_='secondaryInfo').text.strip('()')
        return year

    years = [get_year(tag) for tag in movietags]
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag.text.strip()) for tag in ratingtags]
    actors_list = [tag['title'] for tag in inner_movietags]

    # Ensure all lists are the same (scraping can fail or return mismatched lengths).
    list_lengths = [len(years), len(titles), len(ratings), len(actors_list)]
    min_len = min(list_lengths)

    if min_len == 0:
        # Diagnostic: save the response HTML to help debugging in the container
        try:
            with open('last_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
        except Exception:
            pass

        print('No movies were found on the page. Parsing returned empty results.')
        print(f"Parsed lengths: years={len(years)}, titles={len(titles)}, ratings={len(ratings)}, actors={len(actors_list)}")
        print("Saved full response to 'last_response.html' for inspection.")
        return

    # Trim lists to the smallest parsed length to avoid index errors
    years = years[:min_len]
    titles = titles[:min_len]
    ratings = ratings[:min_len]
    actors_list = actors_list[:min_len]

    n_movies = min_len

    while True:
        idx = random.randrange(0, n_movies)
        print(f"{titles[idx]} ({years[idx]}), Rating: {ratings[idx]:.1f}, Starring: {actors_list[idx]}")

        user_input = input('Do you want another movie (y/[n])? ').strip().lower()
        if user_input != 'y':
            break

if __name__ == '__main__':
    main()
