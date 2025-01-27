from django.shortcuts import render, redirect
from Payment.models.customer import Customer
from django.views import View
from Payment.models.product import Product
from Payment.models.orders import Order
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        template = render_to_string('orderemail_template.html',
                                    {'fullname': fullname, 'phone': phone, 'address': address})
        send_mail(
            'Order have been placed',
            template,
            'Brihaspatifutsal2018@gmail.com',
            [email],
            fail_silently=False,
        )
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          email=email,
                          phone=phone,
                          fullname=fullname,
                          quantity=cart.get(str(product.id)))
            order.save()
            request.session['cart'] = {}

        return redirect('orders')


def sendordermail(request):
    send_mail(
        'New Order have been placed.',
        'This mail is to inform you that new orders have been placed by a customer. Please check your admin dashboard and confirm all orders.',
        'Brihaspatifutsal2018@gmail.com',
        ['emailthaxaena@gmail.com'],
        fail_silently=False,
    )
    return redirect('orders')


def orders_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    orders = Order.objects.all()
    lines = []
    for order in orders:
        lines.append(order.fullname)
        lines.append(order.address)
        lines.append(order.phone)
        lines.append(order.email)
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='orders.pdf')
