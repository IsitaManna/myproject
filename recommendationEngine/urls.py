from django.urls import path

from . import views
from .Views import customer_views
from .Views import question_views



urlpatterns = [
    path('', views.index, name='index'),
    path('question-response',question_views.QuestionResponseView.as_view(),name='question_response'),
    # path('register-customer',views.registerCustomer,name='registerCustomer'),
    path('fetch-customer-by-id',views.fetchCustomerById,name='fetchCustomerById'),
    path('fetch-all-customers',views.fetchAllCustomers,name='fetchAllCustomers'),
    # path('login-customer',views.loginCustomer,name = 'loginCustomer'),
    path('recommend-images-based-on-rating',views.recommendImagesBasedOnRating,name='recommendImagesBasedOnRating'),
    path('insert-question',views.insertQuestion,name='insertQuestion'),
    path('fetch-all-questions',views.fetchAllQuestions,name='fetchAllQuestions'),
    path('update-question',views.updateQuestion,name='updateQuestion'),
    path('delete-question',views.deleteQuestion,name='deleteQuestion'),
    path('insert-response',views.insertResponse,name='insertResponse'),
    path('fetch-all-responses',views.fetchAllResponses,name='fetchAllResponses'),
    path('fetch-responses-by-id',views.fetchResponsesByID,name='fetchResponsesByID'),
    path('insert-image-rating',views.insertImageRating,name='insertImageRating'),
    path('fetch-image-rating-by-email',views.fetchImageRatingByEmail,name='fetchImageRatingByEmail'),
    path('update-image-rating',views.updateImageRating,name='updateImageRating'),
    # path('fetch-question-responses',views.fetchQuestionResponses,name='fetchQuestionResponses'),
    # path('create-customer-response',views.create_customer_response,name='create_customer_response'),
    path('get-customer-response-data',views.get_customer_response_data,name='get_customer_response_data'),

    path('register-customer',customer_views.CustomerSignupView.as_view(),name='register_customer'),
    path('login-customer',customer_views.CustomerLoginView.as_view(),name = 'loginCustomer'),
    path('create-customer-response',customer_views.CustomerResponseView.as_view(),name='create_customer_response'),


]