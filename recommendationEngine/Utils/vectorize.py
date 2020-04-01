import pandas as pd
import numpy as np

from recommendationEngine.models import Answer


def get_dataframe(user_responses):
    # UserResponse queryset
    json_data = {
        "email": {"0" : user_responses[0].user.username},
        "timestamp" : {"0" : str(user_responses.order_by('-created_at')[0].created_at)}
    }
    for response in user_responses:
        json_data.update(
            {response.question.question: {"0": response.answer.answer}}
        )
    df = pd.DataFrame.from_dict(json_data)
    return df


def preprocess(df):
    columns = df.columns
    cat_cols = []
    for c in columns:
        if c not in ["email","timestamp"]:
            cat_cols.append(c)

    dummies = pd.get_dummies(df[cat_cols],drop_first=False)
    # print('Dummies --', dummies)

    df = pd.concat([df,dummies],axis = 1)

    df = df.drop(cat_cols,axis = 1)

    dcols = df.columns
    dummy_cols = []
    for c in dcols:
        if c not in ["email","timestamp"]:
            dummy_cols.append(c)
    df1 = df[dummy_cols]
    return df1

# def get_vectors(df):
#     v_dict = {}
#     v_dict['Vector'] = list(np.array(df.iloc[0]).astype(int))
#     return v_dict

def get_vectors(response_li):
    answer_li = list(
        Answer.objects.all().values_list('id', flat=True)
    )
    vec_li = []
    for i in answer_li:
        if i in response_li:
            vec_li.append(1)
        else:
            vec_li.append(0)
    
    return vec_li 
