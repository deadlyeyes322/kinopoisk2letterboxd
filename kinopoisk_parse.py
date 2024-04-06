from bs4 import BeautifulSoup as bs
import requests


RATINGS_TO_LETTERBOXD = {
    '1': '0.5',
    '2': '1',
    '3': '1.5',
    '4': '2',
    '5': '2.5',
    '6': '3',
    '7': '3.5',
    '8': '4',
    '9': '4.5',
    '10': '5',
}

def parse(url):
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    films = []
    for item in soup.find_all("div", class_="item"):
        title = item.find("div", class_="nameEng").text
        year = item.find("div", class_="nameRus").text.split()[-1].replace(")","").replace("(", "")
        rating = item.find("div", class_="vote").text

        if year == "...":
            continue

        rating = RATINGS_TO_LETTERBOXD[rating]

        films.append((title, year, rating))
    
    for film in films:
        with open("films.txt", "w", encoding="utf-8") as file:
            print(film)
            file.write(','.join(film) + "\n")


def main():
    user_id = input("Input your user-account id")
    rate_list_index = int(input("Input how many pages of your ratings"))
    URLs =[f"https://www.kinopoisk.ru/user/{user_id}/votes/list/vs/vote/page/{i}/#list" for i in range(1, rate_list_index)]

    with open("films.txt", "a", encoding="utf-8") as file:
        file.write("Title,Year,Rating\n")

    for url in URLs:
        parse(url)

if __name__ == "__main__":
    main()