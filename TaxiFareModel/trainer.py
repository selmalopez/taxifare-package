# imports
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from TaxiFareModel.utils import *
from TaxiFareModel.encoders import *
from TaxiFareModel.data import *
from TaxiFareModel.trainer import *


class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):


        """defines the pipeline as a class attribute"""
        dist_pipe = Pipeline([
        ('dist_trans', DistanceTransformer()),
        ('stdscaler', StandardScaler())
        ])
        time_pipe = Pipeline([
        ('time_enc', TimeFeaturesEncoder('pickup_datetime')),
        ('ohe', OneHotEncoder(handle_unknown='ignore'))
        ])
        preproc_pipe = ColumnTransformer([
        ('distance', dist_pipe, ["pickup_latitude", "pickup_longitude", 'dropoff_latitude', 'dropoff_longitude']),
        ('time', time_pipe, ['pickup_datetime'])
        ], remainder="drop")

        pipe = Pipeline([
        ('preproc', preproc_pipe),
        ('linear_model', LinearRegression())
        ])

        self.pipeline = pipe


    def run(self):
        """set and train the pipeline"""
        self.pipeline.fit(self.X,self.y)



    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        return compute_rmse(y_pred, y_test)



if __name__ == "__main__":
    # get data
    df = get_data()
    df = clean_data(df, test=False)
    # clean data
    #Trainer().clean_data()
    # set X and y
    X = df.drop('fare_amount', axis=1)
    y = df['fare_amount']

    # hold out
    # train
    # evaluate
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    t = Trainer(X_train, y_train)
    print(X_train)
    t.set_pipeline()
    t.run()
    rmse = t.evaluate(X_test, y_test)
    print(rmse)
