import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema

create_customer_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string"),
    coreapi.Field("fName", required=True, location="form", type="string"),
    coreapi.Field("lName", required=True, location="form", type="string"),
    coreapi.Field("password", required=True, location="form", type="string"),
    coreapi.Field("contactNo", required=True, location="form", type="string"),
    coreapi.Field("city", required=True, location="form", type="string"),
    coreapi.Field("country", required=True, location="form", type="string")
])

fetch_customer_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string")
])

fetch_login_customer_schema = AutoSchema([
    coreapi.Field("email", required=True, location="form", type="string"),
    coreapi.Field("password", required=True, location="form", type="string")
])

create_response_schema = AutoSchema([
    coreapi.Field("QuestionID", required=True, location="form", type="string"),
    coreapi.Field("answer", required=True, location="form", type="string")  
])

fetch_response_schema = AutoSchema([
    coreapi.Field("QuestionID", required=True, location="form", type="string")
])

create_question_schema = AutoSchema(manual_fields=[
coreapi.Field("question", required=True, location="form", type="string")
])

update_question_schema = AutoSchema(manual_fields=[
    coreapi.Field("id", required=True, location="form", type="integer"),
    coreapi.Field("question", required=True, location="form", type="string")
])

delete_question_schema = AutoSchema(manual_fields=[
    coreapi.Field("id", required=True, location="form", type="integer")
])

create_rating_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string"),
    coreapi.Field("imageID", required=True, location="form", type="integer"),
    coreapi.Field("rating", required=True, location="form", type="integer")
])

fetch_rating_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string")
])

update_rating_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string"),
    coreapi.Field("imageID", required=True, location="form", type="integer"),
    coreapi.Field("rating", required=True, location="form", type="integer")
])

create_customer_response_schema = AutoSchema(manual_fields=[
    coreapi.Field("email", required=True, location="form", type="string"),
    coreapi.Field("questionID", required=True, location="form", type="integer"),
    coreapi.Field("responseID", required=True, location="form", type="integer")
])