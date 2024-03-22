from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet
import numpy as np


def predict_user(user0_username, user1_username, hypo_text):
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    user0_vectors = np.array([tweet.vector for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vector for tweet in user1.tweets])

    X_train = np.vstack([user0_vectors, user1_vectors])

    zeros = np.zeros(user0_vectors.shape[0])
    ones = np.ones(user1_vectors.shape[0])

    y_train = np.concatenate([zeros, ones])

    log_reg = LogisticRegression().fit(X_train, y_train)

    hypo_vectors = vectorize_tweet(hypo_text).reshape(1, -1)

    return log_reg.predict(hypo_vectors)[0]
