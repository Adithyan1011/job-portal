from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import JobDb,ApplicationDb
from .serializers import JobSerializer ,RegistrationSerializer ,ApplicationSerializers
from rest_framework import permissions
class jobListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request): 
        qs = JobDb.objects.all()
        serilaizer_instance = JobSerializer(qs,many = True)
        return Response(serilaizer_instance.data)

    def post(self,request):
        serializer_instance = JobSerializer(data = request.data) 
        if serializer_instance.is_valid():
            serializer_instance.save(created_by = request.user)
            return Response(data={
                "message":"Added Successfully"
            })
        else:
            return Response(serializer_instance.errors)

class JobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        qs = get_object_or_404(JobDb,id = pk)
        serializer_instance = JobSerializer(qs)
        return Response(serializer_instance.data)

    def put(self,request,pk):
        qs = get_object_or_404(JobDb,id = pk)
        if qs.created_by == request.user:
            serializer_instance= JobSerializer(qs,data = request.data)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data={
                    "message":"Updated successfully"
                })
            else:
                return Response(serializer_instance.errors,status=403)
        else:
            return Response("access denied!")

    def delete(self,request,pk):
        qs = get_object_or_404(JobDb,id = pk)
        if qs.created_by == request.user:
            qs.delete()
            return Response({"message":"Job deleted successfully "})
        else:
            return Response({"messgae":"access denied"},status=403)
class RegistrationView(APIView):
    def post(self,request):
        Serializer_instance = RegistrationSerializer(data = request.data)
        if Serializer_instance.is_valid():
            Serializer_instance.save()
            return Response({"message":"created successfuly"})
        return Response(Serializer_instance.errors)

class MyjobList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        qs = JobDb.objects.filter(created_by = request.user)
        Serializer_instance = JobSerializer(qs ,many =True)
        return Response(Serializer_instance.data)

class ApplicationView(APIView):
    permission_classes =[permissions.IsAuthenticated]
    def post(self,request):
        Serializer_instance=ApplicationSerializers(data = request.data)
        if Serializer_instance.is_valid():
            job =Serializer_instance.validated_data["job"]
            if job.created_by == request.user:
                return Response({
                    "message":"you cannoot apply for your own job"
                })
            if ApplicationDb.objects.filter(
                job = job,applicant=request.user).exists():
                return Response({"message":"you have already applied"})
            Serializer_instance.save(applicant=request.user)

            return Response({
                "message": "Applied successfully"
            })

        else:
            return Response(Serializer_instance.errors)

class MyApplicationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ApplicationDb.objects.filter(applicant=request.user)
        serializer_instance = ApplicationSerializers(qs, many=True)
        return Response(serializer_instance.data)