from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order


def send_order_notification_to_admin(order):
    """Send email to admin when customer confirms payment"""
    try:
        admin_email = settings.ADMIN_EMAIL
        subject = f'New Order Payment Confirmation - Order #{order.order_number}'
        
        # Build order details
        order_items = order.items.all()
        items_html = '<ul>'
        items_text = ''
        for item in order_items:
            items_html += f'<li>{item.product_title} ({item.size}, {item.color}) - ₹{item.price} x {item.quantity} = ₹{item.subtotal}</li>'
            items_text += f'- {item.product_title} ({item.size}, {item.color}) - ₹{item.price} x {item.quantity} = ₹{item.subtotal}\n'
        items_html += '</ul>'
        
        # Check if payment proof exists
        payment_proof_text = ''
        payment_proof_html = ''
        if hasattr(order, 'payment_proof'):
            proof = order.payment_proof
            if proof.reference_id:
                payment_proof_text = f'Reference ID: {proof.reference_id}\n'
                payment_proof_html = f'<p><strong>Reference ID:</strong> {proof.reference_id}</p>'
        
        context = {
            'order': order,
            'order_number': order.order_number,
            'customer_name': order.user.get_full_name() or order.user.username,
            'customer_email': order.user.email,
            'shipping_address': order.shipping_address,
            'total_amount': order.total_amount,
            'items_html': items_html,
            'items_text': items_text,
            'payment_proof_text': payment_proof_text,
            'payment_proof_html': payment_proof_html,
            'upi_reference': order.upi_reference or 'Not provided',
        }
        
        html_message = render_to_string('emails/admin_order_notification.html', context)
        plain_message = render_to_string('emails/admin_order_notification.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to admin: {str(e)}")
        return False


def send_order_confirmation_to_user(order):
    """Send confirmation email to user when admin approves order"""
    try:
        user_email = order.user.email
        if not user_email:
            return False
        
        subject = f'Order Placed Successfully - Order #{order.order_number}'
        
        # Build order details
        order_items = order.items.all()
        items_html = '<ul>'
        items_text = ''
        for item in order_items:
            items_html += f'<li>{item.product_title} ({item.size}, {item.color}) - ₹{item.price} x {item.quantity} = ₹{item.subtotal}</li>'
            items_text += f'- {item.product_title} ({item.size}, {item.color}) - ₹{item.price} x {item.quantity} = ₹{item.subtotal}\n'
        items_html += '</ul>'
        
        context = {
            'order': order,
            'order_number': order.order_number,
            'customer_name': order.user.get_full_name() or order.user.username,
            'shipping_address': order.shipping_address,
            'total_amount': order.total_amount,
            'items_html': items_html,
            'items_text': items_text,
            'status': order.get_status_display(),
        }
        
        html_message = render_to_string('emails/user_order_confirmation.html', context)
        plain_message = render_to_string('emails/user_order_confirmation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to user: {str(e)}")
        return False




