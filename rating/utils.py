from . import models

def validateRating(rate):
    return type(rate) is int and rate>=0 and rate<=10

def calculateTotalRate(id):
    ratings = models.Rating.objects.filter(joke=id)
    result = 0
    for rate in ratings:
        result += rate.rate
    return round(result/len(ratings),2)

