from bs4 import BeautifulSoup
import requests
import pandas as pd

api_key = 'AIzaSyDuNZvCLYEJEnx-vjvECR4H1ge-I6e7p8s'

class DataPipeline:
    def __init__(self, link, file_path):
        self.link = link
        self.file_path = file_path

    def process_data(self):
        self.get_data()
        self.add_coordinates_to_dataset()

    def get_data(self):
        data = []
        page_html = requests.get(self.link)
        soup = BeautifulSoup(page_html.content, "html.parser")
        concerts = soup.find_all('div', class_='elementor-post__text')
        for concert in concerts:
            link = concert.find('p', class_='elementor-post__title').find('a')['href'].strip()
            artist = concert.find('p', class_='elementor-post__title').find('a').text.strip()
            try:
                city, date = concert.find('div', class_='elementor-post__excerpt').p.text.split(',')
            except ValueError:
                date = "other"
                city = "other"

            concert_page_html = requests.get(link)
            soup = BeautifulSoup(concert_page_html.content, "html.parser")
            try:
                venue = soup.find("h2", class_="elementor-heading-title elementor-size-default").find('a').text.split(",")[1].strip()
            except:
                venue = "other"
            description = ""
            paragraphs = soup.find_all("p")
            for p in paragraphs:
                if artist in p.text:
                    description += p.text + " \n "

            data_dict = {"artist": artist, "link": link, "city": city, "date": date, "venue": venue, "description": description}
            data.append(data_dict)
        self.save_data_to_df(data)

    def save_data_to_df(self, data):
        dataframe = pd.DataFrame.from_dict(data)
        dataframe.to_csv(self.file_path, encoding="utf-8")

    def get_coordinates(self, location):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            coordinates = data['results'][0]['geometry']['location']
            return coordinates['lat'], coordinates['lng']
        else:
            return 52.191097, 19.355406

    def add_coordinates_to_dataset(self):
        df = pd.read_csv(self.file_path)
        latitudes, longitudes = [], []

        for i, sample in df.iterrows():
            latitude, longitude = self.get_coordinates(sample["venue"] + ", " + sample["city"] + ", Poland")
            latitudes.append(latitude)
            longitudes.append(longitude)

        df["latitude"] = latitudes
        df["longitude"] = longitudes
        print(df[["venue", "latitude", "longitude"]])

        df.to_csv(self.file_path)

    def add_event_scale_to_dataset(self):
        pass


def main():
    pass

if __name__ == "__main__":
    main()