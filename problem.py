import os
import numpy as np
import pandas as pd
import rampwf as rw
from rampwf.workflows import FeatureExtractorRegressor
from rampwf.score_types.base import BaseScoreType
from sklearn.model_selection import GroupShuffleSplit


problem_title = 'Prediction of inspection score'
_target_column_name = 'inspection_score' 
# A type (class) which will be used to create wrapper objects for y_pred
Predictions = rw.prediction_types.make_regression()
# An object implementing the workflow

class Restaurant(FeatureExtractorRegressor):
    def __init__(self, workflow_element_names=[
            'feature_extractor', 'regressor', 'tripadvisor_dataset.csv', 'historic_restaurant_scores.csv']):
        super(Restaurant, self).__init__(workflow_element_names[:2])
        self.element_names = workflow_element_names

workflow = Restaurant()

#--------------------------------------------
# Scoring
#--------------------------------------------

# Penalised root mean square error
class PenalisedRMSE(BaseScoreType):
    is_lower_the_better = True
    minimum = 0.0
    maximum = float('inf')

    def __init__(self, name='Score error', precision=2):
        self.name = name
        self.precision = precision

    def __call__(self, y_true, y_pred):
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        penalization = 1.5*(y_pred > y_true) + 1*(y_pred <= y_true)
        loss = np.sqrt(np.mean((y_true - y_pred)**2*penalisation))
        return loss

score_types = [
    # Penalised root mean square error
    PenalisedRMSE(name='Score error', precision=2),
]

#--------------------------------------------
# Cross validation
#--------------------------------------------

def get_cv(X, y):
    cv = GroupShuffleSplit(n_splits=8, test_size=0.20, random_state=42)
    return cv.split(X,y, groups=X['business_id'])

#--------------------------------------------
# Data reader
#--------------------------------------------

def _read_data(path, f_name):
    data = pd.read_csv(os.path.join(path, 'data/interim/', f_name), low_memory=False)
    y_array = data[_target_column_name].values
    X_df = data.drop(_target_column_name, axis=1)
    return X_df, y_array

def get_train_data(path='.'):
    f_name = 'TRAIN.csv'
    return _read_data(path, f_name)

def get_test_data(path='.'):
    f_name = 'TEST.csv'
    return _read_data(path, f_name)