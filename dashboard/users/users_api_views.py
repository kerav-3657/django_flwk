from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required


from .serializers import OrderSerializer,FetchOrderSerializer,update_register_dataUserAPIViewSerializer,RegisterSerializer,CheckEmailSerializer,changePasswordSerializer,CheckEmailSerializerSendMail,CategorySerializer,SubCategorySerializer,IndustrySerializer,TaxSerializer,InterestAreaSerializer,SolutionSerializer,send_mail_serializer,active_project_email_serializer,draft_project_email_serializer,new_project_email_serializer,confirm_send_mail_serializer,changeoldtonewPasswordSerializer,update_verify_dataUserAPIViewSerializer
from .models import Orders,OrderStoreData,CustomCategory,CustomSubCategory,CustomTax,CustomIndustryFilter,CustomInterestArea,CustomSolution,CustomUser

class SolutionCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cat_qs = CustomSolution.objects.filter(is_active=True)
        cat_serializers = SolutionSerializer(cat_qs, many=True)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cat = get_object_or_404(CustomSolution, url_structure=pk)
        cat_serializers = SolutionSerializer(cat)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        cat_serializers = SolutionSerializer(data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_201_CREATED)

class IndustryCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cat_qs = CustomIndustryFilter.objects.all()
        cat_serializers = IndustrySerializer(cat_qs, many=True)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cat = get_object_or_404(CustomIndustryFilter, id=pk)
        cat_serializers = IndustrySerializer(cat)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        cat_serializers = IndustrySerializer(data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, ):
        cat = get_object_or_404(CustomIndustryFilter, id=pk)
        cat_serializers = IndustrySerializer(instance=cat, data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        cat = get_object_or_404(CustomIndustryFilter, id=pk)
        cat.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)	
    
class InterestAreaCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cat_qs = CustomInterestArea.objects.all()
        cat_serializers = InterestAreaSerializer(cat_qs, many=True)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cat = get_object_or_404(CustomInterestArea, id=pk)
        cat_serializers = InterestAreaSerializer(cat)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        cat_serializers = InterestAreaSerializer(data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, ):
        cat = get_object_or_404(CustomInterestArea, id=pk)
        cat_serializers = InterestAreaSerializer(instance=cat, data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        cat = get_object_or_404(CustomInterestArea, id=pk)
        cat.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)	
    
class CategoryCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cat_qs = CustomCategory.objects.all()
        cat_serializers = CategorySerializer(cat_qs, many=True)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cat = get_object_or_404(CustomCategory, id=pk)
        cat_serializers = CategorySerializer(cat)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        cat_serializers = CategorySerializer(data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, ):
        cat = get_object_or_404(CustomCategory, id=pk)
        cat_serializers = CategorySerializer(instance=cat, data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        cat = get_object_or_404(CustomCategory, id=pk)
        cat.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)

class TaxCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cat_qs = CustomTax.objects.all()
        cat_serializers = TaxSerializer(cat_qs, many=True)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cat = get_object_or_404(CustomTax, id=pk)
        cat_serializers = TaxSerializer(cat)
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        cat_serializers = TaxSerializer(data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, ):
        cat = get_object_or_404(CustomTax, id=pk)
        cat_serializers = TaxSerializer(instance=cat, data=request.data)
        cat_serializers.is_valid(raise_exception=True)
        cat_serializers.save()
        return Response(cat_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        cat = get_object_or_404(CustomTax, id=pk)
        cat.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)	
    
class SubCategoryCurd(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        subcat_qs = CustomSubCategory.objects.all()
        subcat_serializers = SubCategorySerializer(subcat_qs, many=True)
        return Response(subcat_serializers.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        subcat = get_object_or_404(CustomSubCategory, id=pk)
        subcat_serializers = SubCategorySerializer(subcat)
        return Response(subcat_serializers.data, status=status.HTTP_200_OK)

    def create(self, request):
        subcat_serializers = SubCategorySerializer(data=request.data)
        subcat_serializers.is_valid(raise_exception=True)
        subcat_serializers.save()
        return Response(subcat_serializers.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, ):
        subcat = get_object_or_404(CustomSubCategory, id=pk)
        subcat_serializers = SubCategorySerializer(instance=subcat, data=request.data)
        subcat_serializers.is_valid(raise_exception=True)
        subcat_serializers.save()
        return Response(subcat_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        subcat = get_object_or_404(CustomSubCategory, id=pk)
        subcat.delete()
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)

class FetchOrders(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):        
        cat_qs = Orders.objects.all()
        cat_serializers = FetchOrderSerializer(cat_qs, many=True)
        return Response(cat_serializers.data or {}, status=status.HTTP_200_OK)            
# class LoginView(views.APIView):
#     # This view should be accessible also for unauthenticated users.
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = serializers.LoginSerializer(data=self.request.data,
#             context={ 'request': self.request })
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return Response(None, status=status.HTTP_202_ACCEPTED)



class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class update_register_dataUserAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = update_register_dataUserAPIViewSerializer
    queryset = CustomUser.objects.all()    

class update_verify_dataUserAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = update_verify_dataUserAPIViewSerializer
    queryset = CustomUser.objects.all()    


class checkEmailWithToken(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckEmailSerializer

class checkEmailWithSendMail(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CheckEmailSerializerSendMail

class changePassword(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = changePasswordSerializer
    queryset = CustomUser.objects.all()

class changeoldtonewPassword(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = changeoldtonewPasswordSerializer
    queryset = CustomUser.objects.all()

class send_mail(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = send_mail_serializer

class active_project_email(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = active_project_email_serializer

class draft_project_email(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = draft_project_email_serializer

class new_project_email(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = new_project_email_serializer

class confirm_send_mail(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = confirm_send_mail_serializer


class CreateOrderAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer

# class CreateOrderAPIView(generics.CreateAPIView):
#     serializer_class = OrderSerializer

#     def post(self, request, format=None):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
