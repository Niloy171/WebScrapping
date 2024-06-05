import requests
from bs4 import BeautifulSoup


def get_actor_filmography_wikipedia(actor_name):
    search_url = f"https://en.wikipedia.org/wiki/{actor_name.replace(' ', '_')}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print("Failed to retrieve Wikipedia page.")
        return None, None

    soup = BeautifulSoup(response.content, 'html.parser')

    filmography_section = None
    possible_headings = ['Filmography', 'Career', 'Acting career']
    for heading in possible_headings:
        filmography_section = soup.find('span', {'id': heading})
        if filmography_section:
            break

    if not filmography_section:
        print("Filmography section not found on Wikipedia.")
        return None, None

    movies = []
    filmography_table = filmography_section.find_next('table', class_='wikitable')
    if filmography_table:
        rows = filmography_table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) > 1:
                movie_title = cells[0].get_text(strip=True)
                movie_year = cells[1].get_text(strip=True)
                movies.append((movie_title, movie_year))
    else:
        filmography_list = filmography_section.find_next('ul')
        if filmography_list:
            items = filmography_list.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                parts = text.split('(')
                if len(parts) > 1:
                    movie_title = parts[0].strip()
                    movie_year = parts[-1].split(')')[0].strip()
                    movies.append((movie_title, movie_year))
    sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)
    return actor_name, sorted_movies


def main():
    actor_name = input("Enter the actor's name: ")
    name, movies = get_actor_filmography_wikipedia(actor_name)

    if name:
        print(f"Movies of {name} in descending order:")
        for movie, year in movies:
            print(f"{year} - {movie}")
    else:
        print("Actor not found or filmography section missing.")


if __name__ == "__main__":
    main()
