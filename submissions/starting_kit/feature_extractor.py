import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class FeatureExtractor(object):
    def __init__(self):
        path = os.path.dirname(__file__)
        tripadvisor = pd.read_csv(os.path.join(path, 'tripadvisor_dataset.csv'), low_memory=False)
        tripadvisor.loc[:, 'name'] = tripadvisor.loc[:, 'name'].str.lower()
        tripadvisor.loc[:, 'name'] = tripadvisor.loc[:, 'name'].str.replace('[^\w]','')
        tripadvisor.loc[:, 'name'] = tripadvisor.loc[:, 'name'].apply(lambda s : ''.join(filter(str.isalpha, s)))
        tripadvisor.drop_duplicates('name', inplace=True)
        tripadvisor.loc[:, 'cuisines'] = tripadvisor.loc[:, 'cuisines'].apply(lambda x: self.get_first(x))
        tripadvisor.loc[:, 'special_diets'] = tripadvisor.loc[:, 'special_diets'].apply(lambda x: self.get_first(x))
        tripadvisor.loc[:, 'meals'] = tripadvisor.loc[:, 'meals'].apply(lambda x: self.get_first(x))
        self.tripadvisor = tripadvisor


    def get_first(self, x):
                if isinstance(x, str):
                    res = x.split(',')[0]
                    return res
                else:
                    return x

    def merge(self, X):
            X.loc[:, 'business_name'] = X.loc[:, 'business_name'].str.lower()
            X.loc[:, 'business_name'] = X.loc[:, 'business_name'].str.replace('[^\w]','')
            X.loc[:, 'business_name'] = X.loc[:, 'business_name'].apply(lambda s : ''.join(filter(str.isalpha, s)))
            df = pd.merge(X, self.tripadvisor, left_on='business_name', right_on='name', how='left')
            return df


    def transform(self, X_df):
        return self.preprocessor.transform(self.merge(X_df.copy()))

    def fit(self, X_df, y_array):
        X_encoded = self.merge(X_df.copy())


        def lat_long(X):
            latitude = pd.to_numeric(X['business_latitude'], downcast='float', errors='coerce')
            longitude = pd.to_numeric(X['business_longitude'], downcast='float', errors='coerce')
            return np.c_[latitude.values[:, np.newaxis], longitude.values[:, np.newaxis]]

        lat_long_transformer = FunctionTransformer(lat_long, validate=False)


        def zipcodes(X):
            zipcode_nums = pd.to_numeric(X['business_postal_code'], errors='coerce')
            return zipcode_nums.values[:, np.newaxis]

        zipcode_transformer = FunctionTransformer(zipcodes, validate=False)


        numeric_transformer = Pipeline(steps=[
            ('impute', SimpleImputer(strategy='median'))
        ])


        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])


        num_cols = ['business_id', 'rating', 'n_review_excellent', 'n_review_verygood', 
                    'n_review_average', 'n_review_poor', 'n_review_terrible']
        cat_cols = ['inspection_type', 'risk_category', 'price_type', 'cuisines', 
                    'special_diets', 'meals']
        lat_long_cols = ['business_latitude', 'business_longitude']
        zipcode_col = ['business_postal_code']
        drop_cols = ['business_address', 'business_city', 'business_location',
                     'business_name', 'business_phone_number', 'list_reviews',
                     'business_state', 'full_adress', 'inspection_date', 'inspection_id',
                     'neighborhood', 'violation_description', 'violation_id', 'link', 
                     'name', 'location', 'borough', 'price_range', 'features']

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, num_cols),
                ('cat', categorical_transformer, cat_cols),
                ('lat_long', make_pipeline(lat_long_transformer, SimpleImputer(strategy='median')), lat_long_cols),
                ('zipcode', make_pipeline(zipcode_transformer, SimpleImputer(strategy='median')), zipcode_col),
                ('drop cols', 'drop', drop_cols),
            ])

        self.preprocessor.fit(X_encoded, y_array)
        