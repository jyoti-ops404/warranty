from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Warranty, Vendor
from .forms import WarrantyForm,ContactUsForm
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from django.http import FileResponse


def homepage(request):
    productData = Product.objects.filter(featured=True)  # Only featured products
    return render(request, 'homepage.html',{'productData': productData})

def about_us(request):
    return render(request, 'aboutus.html')

def contact_us(request):
    return render(request, 'contact.html')

def products(request):
    productData = Product.objects.all()
    return render(request, 'products.html', {'productData': productData})

def product_detail(request, productId):
    product = get_object_or_404(Product, id=productId)  # Retrieve the product by ID or return a 404
    return render(request, 'product_detail.html', {'product': product})

#def customer_warrenty(request):
 #   if request.method == 'POST':
 #       form = WarrantyForm(request.POST)
  #      if form.is_valid():
  #          form.save()
   #         messages.success(request, "Form submitted successfully!")
   #         return redirect('customer_warrenty')  
   #     else:
    #        messages.error(request, "There was an error in your submission. Please check the form and try again.")
   # else:
    #    form = WarrantyForm()
   # vendors = Vendor.objects.all()  # Fetch vendors from the database
   # return render(request, 'customer-warrenty.html', {'form': form, 'vendors': vendors})
   



def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact_us')  
    else:
        form = ContactUsForm()
    
    return render(request, 'contact.html', {'form': form})



from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Vendor
from .forms import WarrantyForm
import os
from django.utils.safestring import mark_safe


def customer_warranty(request):
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            warranty = form.save()  # Save the warranty form data to the database
            
            # Generate PDF and save to a consistent location
            pdf_path = f"media/receipts/receipt_{warranty.id}.pdf"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            # Create the PDF
            p = canvas.Canvas(pdf_path)
            p.setFont("Helvetica-Bold", 16)
            p.drawString(220, 750, "Warranty Receipt")
            width, height = letter  # Set the page size (width and height)

            # Add a logo
            logo_path = "static/img/logo.png"  
            try:
                p.drawImage(logo_path, 50, height - 50, width=120, height=50)
            except:
                p.setFont("Helvetica-Bold", 10)
                p.drawString(50, height - 70, "Logo Missing")

            # Draw a border around the page
            p.setStrokeColorRGB(0, 0, 0)  # Set the color of the border (black in this case)
            p.setLineWidth(2)  # Set the thickness of the border line
            p.rect(50, 50, width - 100, height - 100)  # Draw the rectangle (x, y, width, height)

            # Add form details to the PDF
            p.setFont("Helvetica", 12)
            p.drawString(120, 720, f"Vendor: {warranty.vendor}")
            p.drawString(120, 700, f"Name: {warranty.full_name}")
            p.drawString(120, 680, f"Email: {warranty.email or 'N/A'}")
            p.drawString(120, 660, f"Phone: {warranty.phone}")
            p.drawString(120, 640, f"Model: {warranty.model}")
            p.drawString(120, 620, f"Date of Sale: {warranty.date_of_sale}")
            p.drawString(120, 600, f"Serial Number: {warranty.serial_number}")

            # Add a footer
            p.drawString(120, 550, "Thank you for submitting your warranty.")
            p.showPage()
            p.save()

            # Add a success message with the download link
            messages.success(
                request,
                mark_safe(f"Form submitted successfully! <a href='/download_pdf/{warranty.id}/'>Download Receipt</a>")
            )
            return redirect('customer_warranty')  # Redirect to display the success message

        else:
            messages.error(request, "There was an error in your submission. Please check the form and try again.")
    else:
        form = WarrantyForm()

    vendors = Vendor.objects.all()
    return render(request, 'customer-warranty.html', {'form': form, 'vendors': vendors})



def download_pdf(request, warranty_id):
    pdf_path = f"media/receipts/receipt_{warranty_id}.pdf"
    if os.path.exists(pdf_path):
      with open(pdf_path, 'rb') as pdf_file:
        response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{warranty_id}.pdf"'

         # After serving the file, delete it from the server
        try:
            os.remove(pdf_path)
        except Exception as e:
            print(f"Error while deleting file: {e}")
        return response
    else:
        return HttpResponse("The requested file does not exist.", status=404)

