from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import logging
import random
import string

User = get_user_model()

from .models import Orders,OrderStoreData,OrderProjectData,OrderProductImages,CustomCategory,CustomSubCategory,CustomTax,CustomInterestArea,CustomIndustryFilter,CustomSolution,sendMail,DraftsendMail,NewPrjsendMail,CustomUser

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSolution
        fields = ['id','name','price','url_structure','category','sub_category','tax','about','overview','how_it_work','execution_time','short_description','image','image1','image2','image3','image4','image5']

    def to_representation(self, instance):
        data = super(SolutionSerializer, self).to_representation(instance)
        data['category'] = instance.category.category_name
        data['sub_category'] = instance.sub_category.sub_category_name
        data['tax'] = instance.tax.tax_name
        data['category_id'] = instance.category.id
        data['sub_category_id'] = instance.sub_category.id
        
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCategory
        fields = ['category_name']
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSubCategory
        fields = ['category_name','sub_category_name']

    def to_representation(self, instance):
        data = super(SubCategorySerializer, self).to_representation(instance)
        data['category_name'] = instance.category_name.category_name
        return data

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTax
        fields = ['tax_name','add_tax']

class InterestAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomInterestArea
        fields = ['interest_area_name']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomIndustryFilter
        fields = ['industry_name'] 
            
class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    pincode = serializers.CharField(required=False)
    phone_number = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    

    class Meta:
        model = User
        fields = ('id','password', 'password2', 'email', 'first_name', 'last_name', 'company', 'phone_number', 'address', 'city', 'state', 'pincode','type','gst_in','random_number','is_verified')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        digits = string.digits
        random_number = ''.join(random.choice(digits) for _ in range(4))
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=validated_data.get('company'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            pincode=validated_data.get('pincode'),
            gst_in=validated_data.get('gst_in'),
            type=validated_data.get('type'),
            random_number=random_number,
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        email_id = validated_data['email']
        subject = "Please confirm it’s You!"
        message = "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Floorwalk</title></head><body><p style='font-size:14px'>Welcome "+validated_data['first_name']+" "+validated_data['last_name']+",</p><p style='font-size:14px'>Thank you for choosing FloorWalk. You’re just one step away from getting started. Please enter the below code and verify your email with us.</p><p><button style='display:inline-block;font-weight:400;color:#212529;text-align:center;vertical-align:middle;background-color:transparent;border:1px solid transparent;padding:0.375rem 0.75rem;font-size:1rem;line-height:1.5;border-radius:0rem;background:#d0f7e1!important;border:2px solid #d0f7e1!important;color:black!important;font-size: 18px;letter-spacing: 24px;text-align: center;padding: 7px;padding-right: 0px;padding-left: 18px;font-weight: 700;'><span style='color: #0c8f45;'>"+random_number+"</span></button></p><p style='font-size:14px'>Thank You for Joining Us,</p><p style='font-size:14px;margin-top: -8px;'>Team Floorwalk.</p><br/><div style='background: #e2e2e2;padding: 5px;width: 100%;padding-left: 25px;margin-top: -7px;padding-bottom: 12px;'><p style='font-size: 17px;font-weight: 700;margin-bottom: 0px;'>Facing an issue? Get in touch with us:</p><p style='font-size: 14px;'>+91 78360 66777</p><p style='font-size: 14px;color: black!important;'><a href='mailto:contactus@floorwalk.in' target='_blank' style='color: black;font-size: 14px;'>contactus@floorwalk.in</a></p></div></body></html>"
        status = "true",
        send_mail(
            subject=subject,
            message='',
            from_email='sender@example.com',
            recipient_list=[email_id],
            fail_silently=False,
            html_message=message
        )
    
    # Generate token for the user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Create the response data
        data = {
            'id': user.id,
            'first_name': user.first_name+"*$R$*"+str(refresh),
            'last_name': user.last_name+"*$A$*"+str(access),
            'email': user.email,
            'company': user.company,
            'phone_number': user.phone_number,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'pincode': user.pincode,
            'gst_in':user.gst_in,
            'type':user.type,
            'is_verified':user.is_verified,
            'random_number':user.random_number
        }
        return data
    

class update_register_dataUserAPIViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    pincode = serializers.CharField(required=False)
    phone_number = serializers.IntegerField(required=False)
    

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'company', 'phone_number', 'address', 'city', 'state', 'pincode')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.company = validated_data.get('company', instance.company)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.gst_in = validated_data.get('gst_in', instance.gst_in)

        instance.save()

        return instance

class update_verify_dataUserAPIViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'is_verified')

    def update(self, instance, validated_data):
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)

        instance.save()

        return instance

class changePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        
        msg = 'Password change successfully'
        raise serializers.ValidationError({"message": msg})
        

# Serializer to Register User
class CheckEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True)
    password = serializers.CharField(required=False)
    password2 = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('id','password', 'password2', 'email', 'first_name', 'last_name', 'company', 'phone_number', 'address', 'city', 'state', 'pincode','gst_in')
        
    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Email already exists, return False
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Create the response data
            data = {
                'id': user.id,
                'first_name': user.first_name+"*$R$*"+str(refresh),
                'last_name': user.last_name+"*$A$*"+str(access),
                'email': user.email,
                'company': user.company,
                'phone_number': user.phone_number,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'pincode': user.pincode,
                'gst_in':user.gst_in,
                
            }
            return data
        else:
            # Email does not exist, return True
            msg = 'Email does not exist'
            raise serializers.ValidationError({"Email": msg})

class changeoldtonewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check that old password matches
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        # Check that new password fields match
        if new_password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        attrs['password'] = new_password
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        
        msg = 'Password change successful'
        raise serializers.ValidationError({"message": msg})

        
# Serializer to Register User
class send_mail_serializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = sendMail
        fields = ('email', 'subject', 'message','name')

    def create(self, validated_data):
        email = validated_data['email']
        subject = validated_data['subject']
        message = validated_data['message']
        status = "true",
        send_mail(
            subject=subject,
            message=message,
            from_email='sender@example.com',
            recipient_list=[email],
            fail_silently=False,
            html_message=message
        )
    
        # Create the response data
        data = {
            'email': email,
            "message":message,
            "subject":subject,
            "status":status,
        }
        return data

class active_project_email_serializer(serializers.ModelSerializer):
    class Meta:
        model = sendMail
        fields = ('email', 'subject', 'message','name',)

    def create(self, validated_data):
        email = ''
        subject = "Welcome on Onboard the FloorWalk Express."
        message = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Test</title></head><body><p>Hey ' +validated_data.get("name")+'</p><p>How’s it going? I hope you’re feeling as great as we are knowing that you’ve decided to join a bunch of amazing people by availing our service. We are thrilled to have you on board!</p><p>We just wanted to take a moment to say thank you for choosing FloorWalk, we could not be more excited about the prospect of working with you! Please make sure to check the attachment below for your payment receipt.</p><p>Your project is now in active status and our team is already notified about it. We’ll be sure to get started on your order as soon as possible so you can view your results on the user dashboard. If you have any questions or concerns along the way, don’t hesitate to reach out to us at <a href="mailto:contactus@floorwalk.in">contactus@floorwalk.in</a></p><p>Thanks again for choosing us! Stay cool, my friend.</p><p>Team FloorWalk.</p></body></html>'
        status = "true",
        send_mail(
            subject=subject,
            message='',
            from_email='sender@example.com',
            recipient_list=['rinkal.budtech@gmail.com', 'akshay.budtech@gmail.com', 'yogesh.budtech@gmail.com'],
            fail_silently=False,
            html_message=message
        )
    
        # Create the response data
        data = {
            'name': validated_data.get('name'),
            "message":"mail sent successfully",
        }
        return data

class draft_project_email_serializer(serializers.ModelSerializer):
    class Meta:
        model = DraftsendMail
        fields = ('solution_name', 'number_of_audit', 'started_date','message')

    def create(self, validated_data):
        subject = "You might have an unfinished project"
        message = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Test</title></head><body><p>Hey There</p><p>Looks like a customer went off track.</p><p>The payment for the project is still pending. Following are the details - </p><p>1. Solution: '+validated_data.get('solution_name')+'</p><p>2. Number of Audits: '+validated_data.get('number_of_audit')+'</p><p>3. Started date: '+validated_data.get('started_date')+'</p><p>Thanks again for choosing us! Stay cool, my friend.</p><p>Team FloorWalk.</p></body></html>'
        status = "true",
        send_mail(
            subject=subject,
            message='',
            from_email='sender@example.com',
            recipient_list=['rinkal.budtech@gmail.com', 'akshay.budtech@gmail.com', 'yogesh.budtech@gmail.com'],
            fail_silently=False,
            html_message=message
        )
    
        # Create the response data
        data = {
            'solution_name': validated_data.get('solution_name'),
            "number_of_audit":validated_data.get('number_of_audit'),
            "started_date":validated_data.get('started_date'),
            "message":"mail sent successfully"
         
        }
        return data


class new_project_email_serializer(serializers.ModelSerializer):
    class Meta:
        model = NewPrjsendMail
        fields = ('solution_name', 'number_of_audit', 'started_date','message','name')

    def create(self, validated_data):
        subject = "Looks like You have another request"
        message = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Test</title></head><body><p>Hey '+validated_data.get('name')+',</p><p>Looks like you’re getting popular!</p><p>You have another project request. Following are the details -  </p><p>1. Solution: '+validated_data.get('solution_name')+'</p><p>2. Number of Audits: '+validated_data.get('number_of_audit')+'</p><p>3. Started date: '+validated_data.get('started_date')+'</p><p>To view more details about the project click here. Please assign the project to a manager to begin execution.</p><p>Hurry up, the lines getting longer!</p><p>Team FloorWalk.</p></body></html>'
        status = "true",
        send_mail(
            subject=subject,
            message='',
            from_email='sender@example.com',
            recipient_list=['rinkal.budtech@gmail.com', 'akshay.budtech@gmail.com', 'yogesh.budtech@gmail.com'],
            fail_silently=False,
            html_message=message
        )
    
        # Create the response data
        data = {
            'solution_name': validated_data.get('solution_name'),
            "number_of_audit":validated_data.get('number_of_audit'),
            "started_date":validated_data.get('started_date'),
            "name":validated_data.get('name'),
            "message":"mail sent successfully"
         
        }
        return data


class confirm_send_mail_serializer(serializers.ModelSerializer):
    class Meta:
        model = NewPrjsendMail
        fields = ('solution_name', 'number_of_audit', 'started_date','message','name')

    def create(self, validated_data):
        subject = "Welcome to Floorwalk!"
        message = "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Test</title></head><body><p>Dear "+validated_data.get('name')+",</p><p>We're thrilled to welcome you to Floorwalk! Your account has been successfully registered and you can now log in to our platform with your chosen username and password.</p><p>As a registered user, you can avail our wide range of offerings. Our team is always here to help you get the most out of our platform, so if you have any questions or concerns, please don't hesitate to reach out to us.</p><p>Thank you for choosing us! </p><p>Team Floorwalk </p></body></html>"
        status = "true",
        send_mail(
            subject=subject,
            message='',
            from_email='sender@example.com',
            recipient_list=['rinkal.budtech@gmail.com', 'akshay.budtech@gmail.com', 'yogesh.budtech@gmail.com'],
            fail_silently=False,
            html_message=message
        )
    
        # Create the response data
        data = {
            "name":validated_data.get('name'),
            "message":"mail sent successfully"
         
        }
        return data

# Serializer to Register User
class CheckEmailSerializerSendMail(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True)
    password = serializers.CharField(required=False)
    password2 = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('id','password', 'password2', 'email', 'first_name', 'last_name', 'company', 'phone_number', 'address', 'city', 'state', 'pincode','gst_in')
        
    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Email already exists, return False
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            email = validated_data.get('email')
            subject = "FloorWalk <> Please confirm it’s You!"
            message = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Test</title></head><body><p>test</p></body></html>'
            status = "true",
            send_mail(
                subject=subject,
                message='',
                from_email='sender@example.com',
                recipient_list=[email],
                fail_silently=False,
                html_message=message
            )

        # Create the response data
            data = {
                'id': user.id,
                'first_name': user.first_name+"*$R$*"+str(refresh),
                'last_name': user.last_name+"*$A$*"+str(access),
                'email': user.email,
                'company': user.company,
                'phone_number': user.phone_number,
                'address': user.address,
                'city': user.city,
                'state': user.state,
                'pincode': user.pincode,
                'gst_in':user.gst_in,
                
            }
            return data
        else:
            # Email does not exist, return True
            msg = 'Email does not exist'
            raise serializers.ValidationError({"Email": msg})

class OrderStoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStoreData
        fields = ('id', 'store_name', 'store_address', 'store_city', 'store_state', 'store_postalcode', 'store_responses',)

class OrderProjectDataImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductImages
        fields = ('id','image')

class OrderProjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProjectData
        fields = ('id', 'product_desc', 'product_brand', 'product_name',)        

# Serializer to New Order
class OrderSerializer(serializers.ModelSerializer):
    order_store_data = OrderStoreDataSerializer(many=True)
    order_project_data = OrderProjectDataSerializer(many=True)
    #order_product_data = OrderProjectDataImageSerializer(many=True)            
    order_date = serializers.DateTimeField(required=False)
    project_name = serializers.CharField(required=True)
    start_date = serializers.CharField(required=True)
    end_date = serializers.CharField(required=True)
    audience_preference = serializers.CharField(required=False)
    total_responses = serializers.CharField(required=False)
    solution_price = serializers.CharField(required=False)
    subtotal = serializers.CharField(required=False)
    tax_per = serializers.CharField(required=False)
    total_tax = serializers.CharField(required=False)
    final_total = serializers.CharField(required=False)
    order_status = serializers.CharField(required=False)

    class Meta:
        model = Orders
        fields = ('id','order_id','order_date','user','category','subcategory','solution','project_name','start_date','end_date','industry_selection','audience_preference','age_range','occupation','income_range','car_price_range','interest_area','total_responses','solution_price','subtotal','tax_per','total_tax','final_total','order_status','order_store_data','order_project_data',)
        extra_kwargs = {
            'project_name': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
        }

    def create(self, validated_data,request=None):
        order = Orders.objects.create(
            order_date=timezone.now(),
            user=validated_data['user'],
            category=validated_data['category'],
            subcategory=validated_data['subcategory'],
            solution=validated_data['solution'],
            project_name=validated_data['project_name'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            industry_selection=validated_data['industry_selection'],
            audience_preference=validated_data.get('audience_preference', 0),
            age_range=validated_data.get('age_range', None),
            occupation=validated_data.get('occupation', None),
            income_range=validated_data.get('income_range', None),
            car_price_range=validated_data.get('car_price_range', None),
            interest_area=validated_data.get('interest_area', None),
            total_responses=validated_data.get('total_responses', 0.0),
            solution_price=validated_data.get('solution_price', 0.0),
            subtotal=validated_data.get('subtotal', 0.0),
            tax_per=validated_data.get('tax_per', 0.0),
            total_tax=validated_data.get('total_tax', 0.0),
            final_total=validated_data.get('final_total', 0.0),
            order_status=validated_data.get('order_status', 0.0),
        )
        order.save()

        new_order_id = f'FW{str(order.id).zfill(5)}'
        order.order_id = new_order_id
        order.save()
        
        

        order_store_data = validated_data.pop('order_store_data')
        for order_store in order_store_data:
            orderstoredata = OrderStoreData.objects.create(
                order=order,
                store_name=order_store.get('store_name', ''),
                store_address=order_store.get('store_address', ''),
                store_city=order_store.get('store_city', ''),
                store_state=order_store.get('store_state', ''),
                store_postalcode=order_store.get('store_postalcode', 0),
                store_responses=order_store.get('store_responses', 0),
            )
            orderstoredata.save()
            
        order_project_data = validated_data.pop('order_project_data')
        for order_product in order_project_data:
            orderProjectdata_set = OrderProjectData.objects.create(
                order=order,
                product_desc=order_product.get('product_desc', ''),
                product_brand=order_product.get('product_brand', ''),
                product_name=order_product.get('product_name', ''),
                
            )
            orderProjectdata_set.save()
                        
        #order_product_data = validated_data.pop('order_product_data')
        #for image in order_product_data:
            #file = request.FILES[image]
            #if file is not None:            
                #file_content = ContentFile(file.read())
                #file_name = image.name
                #file_path = os.path.join(MEDIA_data, file_name)
                #default_storage.save(file_path, file_content)
                #file_url = default_storage.url(file_path)
                #order_product_image = OrderProductImages.objects.create(
                    #order=order,
                    #image=file_url,
                #)
                #order_product_image.save()
                
       
        data = {
            "id": order.id,
            "user": order.user,
            "order_id": order.order_id,
            "order_date": order.order_date,
            "category": order.category,
            "subcategory": order.subcategory,
            "solution": order.solution,
            "project_name": order.project_name,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "industry_selection": order.industry_selection,
            "audience_preference": order.audience_preference,
            "age_range": order.age_range,
            "occupation": order.occupation,
            "income_range": order.income_range,
            "car_price_range": order.car_price_range,
            "interest_area": order.interest_area,
            "total_responses": order.total_responses,
            "solution_price": order.solution_price,
            "subtotal": order.subtotal,
            "tax_per": order.tax_per,
            "total_tax": order.total_tax,
            "final_total": order.final_total,
            "order_status": order.order_status,
            "order_store_data":order.order_store_data,
            "order_project_data":order.order_project_data,
        }
        return data

class FetchOrderSerializer(serializers.ModelSerializer):
    order_store_data = OrderStoreDataSerializer(many=True)
    order_project_data = OrderProjectDataSerializer(many=True)
    order_date = serializers.DateTimeField(required=False)
    project_name = serializers.CharField(required=True)
    start_date = serializers.CharField(required=True)
    end_date = serializers.CharField(required=True)
    audience_preference = serializers.CharField(required=False)
    age_range = serializers.CharField(required=False)
    occupation = serializers.CharField(required=False)
    income_range = serializers.CharField(required=False)
    car_price_range = serializers.CharField(required=False)
    interest_area = serializers.CharField(required=False)
    total_responses = serializers.CharField(required=False)
    solution_price = serializers.CharField(required=False)
    subtotal = serializers.CharField(required=False)
    tax_per = serializers.CharField(required=False)
    total_tax = serializers.CharField(required=False)
    final_total = serializers.CharField(required=False)
    order_status = serializers.CharField(required=False)

    class Meta:
        model = Orders
        fields = ('id','order_id','order_date','user','category','subcategory','solution','project_name','start_date','end_date','industry_selection','audience_preference','age_range','occupation','income_range','car_price_range','interest_area','total_responses','solution_price','subtotal','tax_per','total_tax','final_total','order_status','order_store_data','order_project_data')
    
    def to_representation(self, instance):
        data = super(FetchOrderSerializer, self).to_representation(instance)
        data['category_name'] = instance.category.category_name
        data['sub_category'] = instance.subcategory.sub_category_name
        data['solution_name'] = instance.solution.name
        
        return data
