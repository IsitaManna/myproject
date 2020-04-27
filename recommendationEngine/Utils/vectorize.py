from recommendationEngine.models import Answer


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
