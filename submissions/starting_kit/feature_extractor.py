import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline


class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, X_df, y_array):
        pass

    def transform(self, X_df):
        X_encoded = X_df

        def get_range_number(x, typ):
            if typ == 'min':
                if str(x).split('€')[0] == 'nan':
                    return(np.nan)
                else:
                    return(np.int(str(x).split('€')[1].split(' ')[0]))
            if typ == 'max':
                if str(x).split('€')[0] == 'nan':
                    return(np.nan)
                else:
                    return(np.int(str(x).split('€')[2].split(' ')[0]))

        path = os.path.dirname(__file__)
        tripadvisor = pd.read_csv(os.path.join(path, 'tripadvisor_dataset.csv'), low_memory=False)
        tripadvisor['name'] = tripadvisor['name'].str.lower().str.replace('[^\w]','').apply(lambda s : ''.join(filter(str.isalpha, s)))
        tripadvisor['price_range_min'] = list(map(lambda x: get_range_number(x, 'min'), tripadvisor["price_range"]))
        tripadvisor['price_range_max'] = list(map(lambda x: get_range_number(x, 'max'), tripadvisor["price_range"]))


        def lat_long(X):
            latitude = pd.to_numeric(X['business_latitude'], downcast='float', errors='coerce')
            longitude = pd.to_numeric(X['business_longitude'], downcast='float', errors='coerce')
            return np.c_[latitude.values[:, np.newaxis], longitude.values[:, np.newaxis]]
        lat_long_transformer = FunctionTransformer(lat_long, validate=False)

        # numeric_transformer = Pipeline(steps=[
        #     ('impute', SimpleImputer(strategy='median'))])

        # def process_date(X):
        #     date = pd.to_datetime(X['Fiscal_year_end_date'], format='%Y-%m-%d')
        #     return np.c_[date.dt.year, date.dt.month, date.dt.day]
        # date_transformer = FunctionTransformer(process_date, validate=False)
        
        # def process_APE(X):
        #     APE = X['Activity_code (APE)'].str[:2]
        #     return pd.to_numeric(APE).values[:, np.newaxis]
        # APE_transformer = FunctionTransformer(process_APE, validate=False)

        def merge(X):
            X['business_name'] = X['business_name'].str.lower().str.replace('[^\w]','').apply(lambda s : ''.join(filter(str.isalpha, s)))
            df = pd.merge(X, tripadvisor, left_on='business_name', right_on='name', how='left')
            return df
        merge_transformer = FunctionTransformer(merge, validate=False)



        lat_long_cols = ['business_latitude', 'business_longitude']
        # zipcode_col = ['Zipcode']
        # date_cols = ['Fiscal_year_end_date']
        # APE_col = ['Activity_code (APE)']
        merge_col = ['business_name']
        drop_cols = ['']

        preprocessor = ColumnTransformer(
            transformers=[
                # ('zipcode', make_pipeline(zipcode_transformer, SimpleImputer(strategy='median')), zipcode_col),
                ('num', numeric_transformer, num_cols),
                # ('date', make_pipeline(date_transformer, SimpleImputer(strategy='median')), date_cols),
                # ('APE', make_pipeline(APE_transformer, SimpleImputer(strategy='median')), APE_col),
                ('merge', make_pipeline(merge_transformer, SimpleImputer(strategy='median')), merge_col),
                ('drop cols', 'drop', drop_cols),
                ])

        X_array = preprocessor.fit_transform(X_encoded)
        return X_array