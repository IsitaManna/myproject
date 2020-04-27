from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from recommendationEngine.models import User, Question, Answer, UserResponse


user_dict = {
    "email":"test@test.com",
    "fName":"Jhon",
    "lName":"Doe",
    "password":"test@123#",
    "contactNo":"8888777765",
    "city":"Kolkata",
    "country":"India"
}

test_question = {
    "question": "This is a test Question?",
    "answers": [
        {
            "id": 1,
            "answer": "Test answer 1"
        },
        {
            "id": 2,
            "answer": "Test answer 2"
        },
        {
            "id": 3,
            "answer": "Test answer 3"
        }
    ]
}



class CustomerSignupTestCase(APITestCase):
    
    def setUp(self):
        pass

    def test_register(self):
        resp = self.client.post(
            '/recommendation-engine/register-customer',
            user_dict,
            format='json'
        )
        self.assertEqual(201, resp.status_code)

    
class CustomerLoginTestCase(APITestCase):
    def setUp(self):
        user = User(
            username=user_dict['email'],
            first_name=user_dict['fName'],
            last_name=user_dict['lName'],
            contact_no=user_dict['contactNo'],
            city=user_dict['city'],
            country=user_dict['country']
        )
        user.set_password(user_dict['password'])
        user.save()
        tk = Token.objects.create(user=user)


    def test_login(self):
        
        resp = self.client.post(
            '/recommendation-engine/login-customer',
            {
                "email": user_dict['email'],
                "password": user_dict['password']
            },
            format='json'
        )
        self.assertEqual(200, resp.status_code)


class UserResponseTestCase(APITestCase):
    def setUp(self):
        user = User(
            username=user_dict['email'],
            first_name=user_dict['fName'],
            last_name=user_dict['lName'],
            contact_no=user_dict['contactNo'],
            city=user_dict['city'],
            country=user_dict['country']
        )
        user.set_password(user_dict['password'])
        user.save()
        self.tk = Token.objects.create(user=user)

        ques = Question(
            question=test_question['question'],
            question_type=Question.QUALITATIVE
        )
        ques.save()
        for i in test_question['answers']:
            Answer.objects.create(
                id=i['id'],
                question_id=ques.id,
                answer=i['answer']
            )


    def test_submission(self):
        # print(self.tk.key)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tk.key)
        resp = self.client.post(
            path='/recommendation-engine/create-customer-response',
            data={
                "QuesID": 1,
                "ResponseID": 1
            },
            content_type='application/json'
        )
        self.assertEqual(201, resp.status_code)

        resp = self.client.post(
            path='/recommendation-engine/create-customer-response',
            data={
                "QuesID": 1,
                "ResponseID": 3
            },
            content_type='application/json'
        )
        self.assertEqual(201, resp.status_code)