"""
- Views should be free from logical detailing
"""
import json
import traceback

from django.core.exceptions import ObjectDoesNotExist, ValidationError

# Create your views here.
from django.db import transaction
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TodoList,ProjectCode
from .serializers import TodoListSerializer,ProjectCodeSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


class ProjCodeListView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        """ Fetch the all task list  from the TodoList Models

        > GET: http://{{ip}}/todo/projcode/ """
        try:
            proj_code_obj = ProjectCode.objects.filter(is_deleted=False)
            if not proj_code_obj:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            proj_code_obj = ProjectCodeSerializer(proj_code_obj, many=True).data
            return Response({"data": proj_code_obj}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error get all record > uncaught exception > %s " % str(traceback.format_exc()))
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        """
        Add the projectcode to the ProjectCode Models

        > POST: http://{{ip}}/todo/projcode/

         jsonbody ====>
        {
           "pcode":"Smile",
           "pcode":"3001",

        }"""
        try:
            jsondata = json.loads(request.body)
            proj_code_obj = ProjectCodeSerializer(data=jsondata)

            if proj_code_obj.is_valid():
                proj_code_obj.save()
            return Response(proj_code_obj.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # checking here require keys in the request body
            return Response(data={"message": str(e) + ' required'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            # attribute missing while stroing the data
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            # if serializer is not valid or missing of the key
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # if serializer is not valid or missing of the key
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TODOListView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request, format=None):
        """ Fetch the all task list  from the TodoList Models

        > GET: http://{{ip}}/todo/task/ """
        try:
            todo_obj = TodoList.objects.filter(is_deleted=False)
            if not todo_obj:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            todo_obj = TodoListSerializer(todo_obj, many=True).data
            return Response({"data": todo_obj}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error get all record > uncaught exception > %s " % str(traceback.format_exc()))
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        """
        Add the send/request gallaryimages to the GallaryImages Models

        > POST: http://{{ip}}/todo/task/

         jsonbody ====>
        {
           "pcode":1,
           "user_id":"3001",
           "title":"Checking images detail",
           "content":"Not accepting base 64 data",
           "priority":0,
           "end_date":"2021-03-27"

        }"""
        try:
            jsondata = json.loads(request.body)
            if not jsondata['title']:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            todo_obj = TodoListSerializer(data=jsondata)
            if todo_obj.is_valid():
                todo_obj.save()

            return Response(todo_obj.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # checking here require keys in the request body
            return Response(data={"message": str(e) + ' required'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            # attribute missing while stroing the data
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            # if serializer is not valid or missing of the key
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # if serializer is not valid or missing of the key
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TODODetailView(APIView):

    def get(self, request, format=None):
        """ Fetch the task detail from the TodoList Models

        > GET: http://{{ip}}/todo/taskdetail/ """
        print("request.GET.get('task_id')---------", request.GET.get('task_id'))
        try:
            todo_task_obj = TodoList.objects.filter(id=request.GET.get('task_id'), is_deleted=False)
            print("todo_task_obj------------", todo_task_obj)
            if not todo_task_obj:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            todo_task_obj = TodoListSerializer(todo_task_obj, many=True).data
            return Response({"data": todo_task_obj}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as objNE:
            # Model object does not exist
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error get images> uncaught exception > %s " % str(traceback.format_exc()))
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, format=None):
        """Add the update/get task details to the TodoList Models

        > patch: http://{{ip}}/todo/taskdetails/

         jsonbody ====>
        {
          "pcode":1,
           "user_id":"3001",
           "title":"Checking images detail",
           "content":"Not accepting base 64 data",
           "priority":0,
           "end_date":"2021-03-27"
        }"""
        try:
            self.task_id = request.GET.get('task_id')
            jsondata = json.loads(request.body)
            todo_task_obj = TodoListSerializer(TodoList.objects.get(id=self.task_id), data=jsondata,
                                                      partial=True)
            if todo_task_obj.is_valid():
                todo_task_obj.save()
                return Response(todo_task_obj.data, status=status.HTTP_201_CREATED)

        except KeyError as KeyEr:
            return Response(data=KeyEr.__dict__, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, format=None):
        """Add the update/get task details to the TodoList Models

        > delete: http://{{ip}}/todo/taskdetails/?task_id=1

      """
        try:
            self.task_id = request.GET.get('task_id')
            todo_detail_obj = TodoList.objects.get(id=self.task_id)
            # TODO Trigger atomic transaction so logic is executed in a single transaction
            with transaction.atomic():
                # Start transaction.
                # Failure of any operation, rollbacks other operations
                todo_detail_obj.is_deleted = True
                todo_detail_obj.save()
                return Response(status=status.HTTP_200_OK)

        except KeyError as KeyEr:
            return Response(data=KeyEr.__dict__, status=status.HTTP_406_NOT_ACCEPTABLE)

        except AttributeError as attr:
            return Response({"details": "attribute missing"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as objNE:
            return Response(objNE.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as exc:
            return Response(exc.__dict__, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
