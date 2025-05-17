from django.shortcuts import render
from rest_framework import generics
from shipper.models import Freight, Location, Shipper
from shipper.serializers import FreightSerializer, LocationSerializer
from shipper.permissions import IsShipper
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect
from rest_framework.response import Response
from .forms import FreightCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView


from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListAPIView

# class FreightAPIView(ListCreateAPIView):
#     serializer_class = FreightSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated, IsShipper]

#     def get_queryset(self):
#         """Only show freights owned by the current shipper"""
#         if isinstance(self.request.user, AnonymousUser):
#             raise PermissionDenied("Authentication required")
            
#         try:
#             # Get the Shipper profile associated with the user
#             shipper_profile = Shipper.objects.get(user=self.request.user)
#             return Freight.objects.filter(shipper=shipper_profile)
#         except Shipper.DoesNotExist:
#             raise PermissionDenied("User is not a registered shipper")
    
#     def perform_create(self, serializer):
#         """Automatically set shipper when creating"""
#         if isinstance(self.request.user, AnonymousUser):
#             raise PermissionDenied("Authentication required")
            
#         try:
#             shipper_profile = Shipper.objects.get(user=self.request.user)
#             serializer.save(shipper=shipper_profile)
#         except Shipper.DoesNotExist:
#             raise PermissionDenied("User is not a registered shipper")

class FreightAPIView(ListCreateAPIView):
    serializer_class = FreightSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsShipper]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'shipper/freight_post.html'  # Combined template

    def get_queryset(self):
        """Only show freights owned by the current shipper"""
        shipper_profile = Shipper.objects.get(user=self.request.user)
        return Freight.objects.filter(shipper=shipper_profile)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({
                'freights': response.data,
                'form': FreightCreateForm()  # Include empty form for GET requests
            }, template_name=self.template_name)
        return response

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            form = FreightCreateForm(request.POST)
            if form.is_valid():
                freight = form.save(commit=False)
                freight.shipper = request.user.shipper
                freight.save()
                return redirect('freight-list')
            return Response({
                'form': form,
                'freights': self.get_queryset().values()
            }, template_name=self.template_name)
        return super().create(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User role: {getattr(request.user, 'role', None)}")
        print(f"Session: {request.session.items()}")
        return super().dispatch(request, *args, **kwargs)


class FreightDetailAPIView(RetrieveAPIView):
    authentication_classes=[IsAuthenticated]
    queryset = Freight.objects.all()
    serializer_class = FreightSerializer
    lookup_field = 'id' 

class FreightUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = FreightSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsShipper]
    lookup_field = 'id' 

class FreightDelete(RetrieveDestroyAPIView):
    serializer_class = FreightSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsShipper]
    lookup_field = 'id'


# Template View (for HTML)
@method_decorator(login_required, name='dispatch')
class FreightTemplateView(TemplateView):
    template_name = 'shipper/freight_post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'shipper'):
            context['freights'] = Freight.objects.filter(shipper=self.request.user.shipper)
            context['form'] = FreightCreateForm()
        else:
            return redirect('shipper:create-shipper-profile')  # or show an error
        return context
    
# class AllFreights(ListAPIView):
#     authentication_classes=[IsAuthenticated]
#     queryset = Freight.objects.all()
#     serializer_class = FreightSerializer

# class FreightSearchView(ListView):
#     model = Freight
#     permission_classes=[IsAuthenticated]
#     template_name = 'shipper/freight_search.html'  # New template for search
#     context_object_name = 'freights'
#     paginate_by = 10  # Optional: Add pagination

#     def get_queryset(self):
#         queryset = Freight.objects.filter(status='searching')  # Only show available freights
        
#         # Get search parameters from URL (e.g., ?location1=City&location2=City)
#         location1 = self.request.GET.get('location1')
#         location2 = self.request.GET.get('location2')
        
#         if location1:
#             queryset = queryset.filter(location1__icontains=location1)
#         if location2:
#             queryset = queryset.filter(location2__icontains=location2)
        
#         return queryset

class FreightSearchView(ListView):
    model = Freight
    permission_classes = [IsAuthenticated]
    template_name = 'shipper/freight_search.html'
    context_object_name = 'freights'
    paginate_by = 10

    def get_queryset(self):
        # Start with all available freights
        queryset = Freight.objects.filter(status__iexact='searching')

        
        # Get search parameters from URL
        location1 = self.request.GET.get('location1')
        location2 = self.request.GET.get('location2')
        
        # Only apply filters if search parameters are provided
        if location1 or location2:
            if location1:
                queryset = queryset.filter(location__location1__icontains=location1)
            if location2:
                queryset = queryset.filter(location__location2__icontains=location2)
        
        return queryset