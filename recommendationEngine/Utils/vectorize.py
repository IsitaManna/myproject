import json
from scipy.spatial import distance
from recommendationEngine.models import Answer, OCRImage


FLOOR_TAGS = ["balcony/ porch","bath","bedroom","bonus","closet","deck/outdoor space","den","dining room",
           "door","entry","firepit/fireplace","garage","hot tub","kitchen/living room","kitchen","laundry",
           "living room","mudroom","office","pantry","stair","storage","sunroom","utility","WIC","window",
           "living/ dining","kitchen/dining","hall","linen","Misc/cinema"]


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


def get_customer_reponse_vect(user_response):
    dataList = user_response.values()
    custDict = {}
    for tag in FLOOR_TAGS:
        if (tag == "closet") or (tag == "dining room") or (tag == "kitchen") or (tag == "living room"):
            custDict[tag] = 1
        else:
            custDict[tag] = 0
    for data in dataList:
        if data['question_id'] == 4:
            custDict["bedroom"] = int(Answer.objects.get(id=data["answer_id"]).answer)
        elif data['question_id'] == 5:
            custDict["bath"] = int(Answer.objects.get(id=data["answer_id"]).answer)
        elif data['question_id'] == 7:
            custDict["living room"] = 1
            custDict['den'] = 1
        elif data['question_id'] == 9:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["firepit/fireplace"] = 1
        elif data['question_id'] == 10:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["bonus"] = 1
        elif data['question_id'] == 11:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["office"] = 1
        elif data['question_id'] == 8:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans == "Mud Room":
                custDict['mudroom'] = 1
            elif ans == "Small Laundry Area":
                custDict["laundry"] = 1

    custvect = list(custDict.values())
    
    return custvect


def get_vector_distance(customer_vect):
    ocrimages = OCRImage.objects.all()
    dist_li = []
    for img in ocrimages:
        imgdict = json.loads(img.data_dict)

        imgvect = list(imgdict.values())
        dst = distance.euclidean(customer_vect, imgvect)
        dist_li.append(
            {
                "img":str(img.image_path),
                "dist":dst,
                "id": img.id
            }
        )
    return dist_li