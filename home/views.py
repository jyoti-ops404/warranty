from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Warranty, Vendor
from .forms import WarrantyForm
# Create your views here.

# View for the /add page
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/view')  # Redirect to the /view page after saving
#     else:
#         form = StudentForm()
#     return render(request, 'add.html', {'form': form})

# # View for the /view page
# def view_students(request):
#     students = Student.objects.all()  # Retrieve all students from the datab

def homepage(request):
    productData = Product.objects.all()
    return render(request, 'homepage.html',{'productData': productData})

def about_us(request):
    return render(request, 'aboutus.html')

#def customer_warrenty(request):
    # return render(request, 'customer-warrenty.html')

def products(request):
    return render(request, 'products.html')

def product_detail(request, productId):
    product = get_object_or_404(Product, id=productId)  # Retrieve the product by ID or return a 404
    return render(request, 'product_detail.html', {'product': product})

def customer_warrenty(request):
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warranty_list.html')  # Redirect to the list page
    else:
        form = WarrantyForm()
    vendors = Vendor.objects.all()  # Fetch vendors from the database
    return render(request, 'customer-warrenty.html', {'form': form, 'vendors': vendors})
    #return render(request, 'customer-warrenty.html', {'form':form})
    #return render(request, 'customer-warrenty.html', {'vendors': Vendor})

# @login_required
# def warranty_list(request):
#     if request.user.is_superuser:  # Admin can see all warranties
#         warranties = Warranty.objects.all()
#     else:  # Vendors can only see their associated warranties
#         vendor = Vendor.objects.filter(user=request.user).first()
#         warranties = Warranty.objects.filter(vendor=vendor)
#     return render(request, 'warranty_list.html', {'warranties': warranties})