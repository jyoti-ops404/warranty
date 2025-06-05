from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, ProductType
from django.contrib.auth.decorators import login_required
from .models import Warranty, Vendor,Inquiry
from .forms import WarrantyForm,ContactUsForm,InquiryForm
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from django.http import FileResponse
import json
from collections import defaultdict

def homepage(request):
    productData = Product.objects.filter(featured=True)  # Only featured products
    batteryTypes = ProductType.objects.filter(type='Battery')
    otherItemTypes = ProductType.objects.filter(type='Other Item')

    return render(request, 'homepage.html', {
        'productData': productData,
        'batteryTypes': batteryTypes,
        'otherItemTypes': otherItemTypes,
    })

def about_us(request):
    return render(request, 'aboutus.html')

def contact_us(request):
    return render(request, 'contact.html')

def calculator(request):
    product_type = get_object_or_404(ProductType, id=1)
    productData = Product.objects.filter(type=product_type)
    serialized_data = json.dumps([
        {
            'id': p.id,
            'productName': p.productName,
            'Ah': p.Ah,
            'Volt': p.Volt,
            'price': p.price,
            'productImage': p.productImage.url if p.productImage else ''
        } for p in productData
    ])

    return render(request, 'calculator.html', {
        'productDataJson': serialized_data
    })

def all_products(request):
    grouped_products = defaultdict(list)

    for product in Product.objects.select_related('type').all():
        grouped_products[product.type].append(product)

    return render(request, 'products.html', {
        'grouped_products': grouped_products.items(),
    })

def category_products(request, typeId):
    product_type = get_object_or_404(ProductType, id=typeId)
    productData = Product.objects.filter(type=product_type)
    return render(request, 'category_products.html', {
        'productData': productData,
        'productType': product_type
    })

def product_detail(request, productId):
    product = get_object_or_404(Product, id=productId)
    inquiry_made = False

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()
            inquiry_made = True  # Flag to show success message
    else:
        form = InquiryForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'form': form,
        'inquiry_made': inquiry_made,
    })



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
from reportlab.lib import colors
from .models import Vendor
from .forms import WarrantyForm
import os
from django.utils.safestring import mark_safe


def customer_warranty(request):
    if request.method == 'POST':
        form = WarrantyForm(request.POST)
        if form.is_valid():
            warranty = form.save()

            pdf_path = f"media/receipts/receipt_{warranty.id}.pdf"
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            margin_x = 60
            y = height - 60

            # Line 1: Logo (top-left)
            logo_path = "static/img/logo.png"
            if os.path.exists(logo_path):
                c.drawImage(logo_path, margin_x, y - 10, width=100, height=40, preserveAspectRatio=True)
            else:
                c.setFont("Helvetica", 10)
                c.drawString(margin_x, y, "Logo Missing")

            y -= 60  # space below logo

            # --- Line 2: Title (centered) ---
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(width / 2, y, "Warranty Receipt")

            # --- Draw Border ---
            c.setStrokeColor(colors.black)
            c.setLineWidth(1.2)
            c.rect(40, 40, width - 80, height - 100)

            y -= 40

            # --- Section: Customer Information ---
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin_x, y, "Customer Information")
            y -= 25
            c.setFont("Helvetica", 12)
            c.drawString(margin_x, y, f"Name: {warranty.full_name}")
            y -= 20
            c.drawString(margin_x, y, f"Phone: {warranty.phone}")
            y -= 20
            c.drawString(margin_x, y, f"Email: {warranty.email or 'N/A'}")

            y -= 40

            # --- Section: Product Information ---
            c.setFont("Helvetica-Bold", 14)
            c.drawString(margin_x, y, "Product Information")
            y -= 25
            c.setFont("Helvetica", 12)
            c.drawString(margin_x, y, f"Vendor: {warranty.vendor}")
            y -= 20
            c.drawString(margin_x, y, f"Model: {warranty.model}")
            y -= 20
            c.drawString(margin_x, y, f"Serial Number: {warranty.serial_number}")
            y -= 20
            c.drawString(margin_x, y, f"Date of Sale: {warranty.date_of_sale.strftime('%B %d, %Y')}")

            # --- Footer ---
            y -= 40
            c.setStrokeColor(colors.grey)
            c.line(margin_x, y, width - margin_x, y)
            y -= 20
            c.setFont("Helvetica-Oblique", 11)
            c.setFillColor(colors.darkgreen)
            c.drawString(margin_x, y, "Thank you for submitting your warranty. Please keep this receipt for future reference.")

            # Finalize
            c.showPage()
            c.save()

            messages.success(
                request,
                mark_safe(f"Form submitted successfully! <a href='/download_pdf/{warranty.id}/'>Download Receipt</a>")
            )
            return redirect('customer_warranty')

        else:
            messages.error(request, "There was an error in your submission. Please check the form and try again.")
    else:
        form = WarrantyForm()

    vendors = Vendor.objects.all()
    battery_types = ProductType.objects.all()
    products = Product.objects.all().values('id', 'model', 'type')
    product_data = list(products)
    return render(request, 'customer-warranty.html', {
        'form': form,
        'vendors': vendors,
        'battery_types': battery_types,
        'product_data': product_data,
    })



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

