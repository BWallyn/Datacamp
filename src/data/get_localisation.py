import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def main():
    data_path = "../../data"
    data = pd.read_csv(data_path+'/raw/Restaurant_Scores_-_LIVES_Standard.csv')
    geolocator = Nominatim(user_agent='data_camp')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    data['full_adress'] = data['business_address'] + ' ' + data['business_city'] + \
        ' ' + data['business_postal_code'] + ' ' + data['business_state']

    dic_location = {}

    def fetch_location(row):

        if(pd.isna(row)):
            return (0, 0)

        if(not dic_location.get(row)):
            location = geocode(row)
            if(location):
                point = tuple(location.point)[:-1]
                dic_location[row] = point
            else:
                return (0, 0)

        return dic_location[row]

    data['business_latitude'], data['business_longitude'] = zip(
        *data['full_adress'].apply(fetch_location))
    del dic_location

    data.to_csv(data_path+'/interim/enhanced_restaurant_scores.csv', index=False)


if __name__ == '__main__':
    main()
