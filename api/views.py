from tkinter import Y
from numpy import save
from rest_framework.response import Response
from rest_framework.decorators import api_view
from yaml import serialize
from base.models import Item
from .serializers import ItemSerializer
import pickle
from pymongo import MongoClient
#from sklearn.linear_model import Lasso
import numpy as np


def load_model_from_DB(table):    
    data = table.find({})[0]
    return(pickle.loads(data['model']), data['degree'])

def load_poly_from_DB(table):    
    data = table.find({})[0]
    return(pickle.loads(data['model']))

@api_view(['GET'])
def getData(request):
    # Mongo client
    mongo_client = MongoClient("mongodb+srv://andrea:N9oV7qkj01LnsvLx@footballdb.ssfhubn.mongodb.net/?retryWrites=true&w=majority")

    # Open a DB 
    db = mongo_client.footballDB
    models_DB = db.models
    poly_models_DB = db.poly_model
    sc_models_DB = db.sc_model

    saved_model, polynomial_degree = load_model_from_DB(models_DB)
    poly_model = load_poly_from_DB(poly_models_DB)
    sc_model = load_poly_from_DB(sc_models_DB)


    X = np.array([ 9.0000e+02, 1.1500e+02,  1.1600e+02,  1.2200e+02,  1.1790e+02,
        1.1790e+02,  1.1400e+02,  8.0000e+00,  1.3920e+01,  6.6700e+00,
        2.5800e+00,  1.2840e+01,  4.5000e-01,  2.1000e-01,  1.3440e+01,
        1.2130e+01,  4.6720e+01,  1.0000e+00,  1.1000e+01,  1.1000e+01,
        1.3350e+02,  1.4800e+00,  7.1910e+01,  1.2200e+02,  1.4500e+02,
        1.1958e+02,  7.7000e+02,  5.9360e+01,  1.1000e+02,  1.3200e+02,
        1.2666e+02,  7.8500e+00,  6.1580e+01,  1.1673e+02,  1.3768e+02,
        1.3280e+01,  1.2200e+05,  1.1200e+02,  1.1673e+02,  6.2000e+01,
        1.0140e+03,  5.5000e+01, -2.1200e+00,  2.5600e+01,  2.5830e+01,
        1.2600e+02,  3.6000e+00,  8.8000e+01,  9.8000e+00,  8.1000e+00,
        1.5000e+00,  9.0000e+00,  1.0000e+01,  6.0000e+00]).reshape(1,-1)

    poly_X = poly_model.transform(X)
    scaled_pily_X = sc_model.transform(poly_X)
    y_pred = saved_model.predict(scaled_pily_X)


    print(y_pred)
    return Response(y_pred)

@api_view(['POST'])
def add(request):
    data=request.data
    
    # Mongo client
    mongo_client = MongoClient("mongodb+srv://andrea:N9oV7qkj01LnsvLx@footballdb.ssfhubn.mongodb.net/?retryWrites=true&w=majority")

    # Open a DB 
    db = mongo_client.footballDB
    models_DB = db.models
    poly_models_DB = db.poly_model
    sc_models_DB = db.sc_model

    saved_model, polynomial_degree = load_model_from_DB(models_DB)
    poly_model = load_poly_from_DB(poly_models_DB)
    sc_model = load_poly_from_DB(sc_models_DB)

    X_post = []
    for key, value in data.items():
        X_post.append(value)
    X_post = np.array(X_post).reshape(1,-1)

    poly_X = poly_model.transform(X_post)
    scaled_pily_X = sc_model.transform(poly_X)
    y_pred = saved_model.predict(scaled_pily_X)

    
    print(y_pred)
    return Response(y_pred)