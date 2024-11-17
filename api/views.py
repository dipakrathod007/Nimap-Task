from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from .models import Client, Project
from .serializers import ClientListSerializer,ClientCreateSerializer,ClientDetailSerializer,ClientUpdateSerializer,ProjectCreateSerializer,ProjectSerializer

class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    permission_classes = [IsAuthenticated]

# get client
class ClientCreateView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = [IsAuthenticated]

# update client
class ClientDetailView(RetrieveAPIView):
    queryset = Client.objects.prefetch_related('projects')  # Optimize with prefetch
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]



class ClientUpdateView(UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer
    permission_classes = [IsAuthenticated]


# Delete Client

class ClientDeleteView(DestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can delete

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        # Customize the response to return status 204 explicitly
        response.data = None
        return response


# create project for that client

class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=request.user)
            response_serializer = ProjectCreateSerializer(project)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(users=request.user)

        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data, status=200)

