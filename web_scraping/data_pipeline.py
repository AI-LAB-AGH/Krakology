from bs4 import BeautifulSoup
import requests
import pandas as pd
from web_scraping.api_keys import *
from openai import OpenAI
from web_scraping.gpt_prompt import *
from random import randint
from datetime import datetime
google_maps_api_key = get_google_maps_api_key()
openai_api_key = get_gpt_api_key()

class DataPipeline:
    def __init__(self, link, file_path, model):
        self.link = link
        self.file_path = file_path
        self.model = model
        self.client = OpenAI(api_key=openai_api_key)

    def process_data(self):
        self.get_data()
        self.add_coordinates_to_dataset()
        self.add_event_scale_to_dataset()


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
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={google_maps_api_key}"
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
        minimums = []
        maximums = []
        df = pd.read_csv(self.file_path)
        for i, _ in df.iterrows():
            minimum, maximum = self.prompt_gpt(get_system(), self.df_row_as_string(df, i)).split("-")
            minimums.append(minimum)
            maximums.append(maximum)
        df["min_people"] = minimums
        df["max_people"] = maximums
        df.to_csv(self.file_path)

    def prompt_gpt(self, system, prompt) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": system},
                {"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def df_row_as_string(self, df, row_index):
        row = df.iloc[row_index]
        row_str = ", ".join([f"{col}: {row[col]}" for col in ["artist", "city", "venue", "description"]])
        return row_str

    @classmethod
    def merge_event_info_with_dataset(cls, sales_df_path, concerts_df_path):
        zabka_sales_df = pd.read_csv(sales_df_path)
        concerts_df = pd.read_csv(concerts_df_path)

        zabka_sales_df["event_ID"] = -1

        nearest_found = False

        for i, sale_row in zabka_sales_df.iterrows():
            store_x = sale_row["store_localisation_x"]
            store_y = sale_row["store_localisation_y"]
            zabka_sales_df.at[i, "event_ID"] = -1
            zabka_sales_df.at[i, "is_event"] = -1
            zabka_sales_df.at[i, "min_people"] = -1
            zabka_sales_df.at[i, "max_people"] = -1


            for j, event_row in concerts_df.iterrows():
                event_x = event_row["latitude"]
                event_y = event_row["longitude"]

                if event_row["date"].strip() == sale_row["date"].strip():
                    if event_x >= store_x - 0.0045 and event_x <= store_x + 0.0045 and event_y <= store_y + 0.007 and event_y >= store_y - 0.007:
                        nearest_found = True
                        nearest_event_id = j
                        min_people = event_row["min_people"]
                        max_people = event_row["max_people"]
                        break

            if nearest_found == True:
                zabka_sales_df.at[i, "is_event"] = 1
                zabka_sales_df.at[i, "min_people"] = min_people
                zabka_sales_df.at[i, "max_people"] = max_people
                zabka_sales_df.at[i, "event_ID"] = nearest_event_id
                nearest_found = False

        zabka_sales_df.to_csv("zabka_2024_sales_updated_more.csv", index=False)

    def clean_dates_in_dataset(self):
        df = pd.read_csv(self.file_path)
        df["date"] = df["date"].apply(self.reformat_date)
        df.to_csv(self.file_path)

    def reformat_date(self, date_str):
        date_str = date_str.replace("r.", "").strip()
        try:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            return date_obj.strftime("%d.%m.%Y")
        except:
            return "01.01.1970"





def main():
    pipeline = DataPipeline("", "", "")
    pipeline.merge_event_info_with_dataset("zabka_2024_sales_more.csv", "concerts_with_scales.csv")

if __name__ == "__main__":
    main()




