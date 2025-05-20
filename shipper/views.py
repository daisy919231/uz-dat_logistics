from django.shortcuts import render
from rest_framework import generics
from shipper.models import Freight, Shipper
from shipper.serializers import FreightSerializer
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

def freight_list_create(request):
    # Get the shipper profile
    try:
        shipper_profile = Shipper.objects.get(user=request.user)
    except Shipper.DoesNotExist:
        if request.headers.get('Accept') == 'application/json':
            return Response({"error": "Shipper profile not found"}, status=403)
        return redirect('accounts:login')  # Or appropriate error page

    # Handle HTML requests
    if request.content_type != 'application/json':
        if request.method == 'GET':
            form = FreightCreateForm()
            freights = Freight.objects.filter(shipper=shipper_profile)
            return render(request, 'shipper/freight_post.html', {
                'freights': freights,
                'form': form
            })
        
        elif request.method == 'POST':
            form = FreightCreateForm(request.POST)
            if form.is_valid():
                freight = form.save(commit=False)
                freight.shipper = shipper_profile
                freight.save()
                return redirect('shipper:freight-list')
            freights = Freight.objects.filter(shipper=shipper_profile)
            return render(request, 'shipper/freight_post.html', {
                'form': form,
                'freights': freights
            }, status=400)

    # Handle API requests (JSON)
    if request.method == 'GET':
        freights = Freight.objects.filter(shipper=shipper_profile)
        serializer = FreightSerializer(freights, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FreightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shipper=shipper_profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class FreightDetailAPIView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated, IsShipper]
#     queryset = Freight.objects.all()
#     serializer_class = FreightSerializer
#     lookup_field = 'id' 

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
        
#         # Get search parameters from URL (e.g., ?origin=City&destination=City)
#         origin = self.request.GET.get('origin')
#         destination = self.request.GET.get('destination')
        
#         if origin:
#             queryset = queryset.filter(origin__icontains=origin)
#         if destination:
#             queryset = queryset.filter(destination__icontains=destination)
        
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
        origin = self.request.GET.get('origin')
        destination = self.request.GET.get('destination')
        
        # Only apply filters if search parameters are provided
        if origin or destination:
            if origin:
                queryset = queryset.filter(origin__icontains=origin)
            if destination:
                queryset = queryset.filter(destination__icontains=destination)
        
        return queryset