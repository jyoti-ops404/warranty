from django.shortcuts import render
from .models import Product
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