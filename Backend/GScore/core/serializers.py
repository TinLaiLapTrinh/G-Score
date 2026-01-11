from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User as DjangoUser
from .models import User, Student, Course, Lecturer, StudentExamResult
from utilities import choice



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "dob",
            "email",
            "address",
            "avatar",
            "phone_number",
            "user_type",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username đã tồn tại")
        if len(value) < 4:
            raise serializers.ValidationError("Username phải >= 4 ký tự")
        return value

    def validate_password(self, value):
        validate_password(value)  # dùng validator của Django
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu phải >= 8 ký tự")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email đã được sử dụng")
        return value


    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["avatar"] = instance.avatar.url if instance.avatar else None
        return data

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source="course",
        write_only=True
    )

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "registration_number",
            "full_name",
            "course_id",  
            "course",     
        ]

    def validate_registration_number(self, value):
        if Student.objects.filter(registration_number=value).exists():
            raise serializers.ValidationError("Mã số học sinh đã tồn tại")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        course = validated_data.pop("course")

        user_data["user_type"] = choice.UserType.STUDENT

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        student = Student.objects.create(
            user=user,
            course=course,
            **validated_data
        )
        return student
    
class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer()


    class Meta:
        model = Lecturer
        fields = [
            "id",
            "lecturer_code",
            "full_name",
            "department",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["user_type"] = choice.UserType.LECTURER

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        lecturer = Lecturer.objects.create(
            user=user,
            **validated_data
        )
        return lecturer
    
class StudentExamResultSerializer(serializers.ModelSerializer):
    blocks = serializers.SerializerMethodField()

    class Meta:
        model= StudentExamResult
        fields= ['registration_number','math','literature',
                 'foreign_language','physics','chemistry',
                 'biology','history','geography','civic_education',
                 'foreign_language_code','blocks']
        
    def get_blocks(self, obj):
        """
        Tính điểm trung bình cho từng khối đủ môn
        """
        result = {}

        for block_code, subjects in choice.EXAM_BLOCKS.items():
            scores = []

            for subject in subjects:
                score = getattr(obj, subject, None)
                if score is None:
                    break
                scores.append(score)

            if len(scores) == len(subjects):
                result[block_code] = round(sum(scores), 2)

        return result
    
