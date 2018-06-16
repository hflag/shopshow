from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    '''当一个订单成功创建后，
    发送一个email通知'''
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                                               order.id)
    mail_sent =send_mail(subject, message,
                         'hflag@163.com',
                         [order.email])
    return mail_sent