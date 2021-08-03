from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.urls import reverse
from requests import Response
from libraries.SMS import SendSms
from apps.stores.models import Item, Kitchen, ItemPrice,KitchenDelivery
from apps.stores.models import Store
from config import settings
from apps.users.models import User, Group, Address, UserWallet
from libraries.DataTables import DataTables
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from libraries.utils import get_kitchen_or_error
from pkbadmin.serializers.user_serializer import UserSerializer
from apps.orders.models import Order, OrderItems, OrderLog
from pkbadmin.serializers.item_serializer import ItemDetailSerializer
from apps.common.models import FinancialYear
from django.db.models import Sum
from pkbadmin.views.decorators import GroupRequiredMixin
from pkbadmin.serializers.order_serialzer import OrderSerializer
from datetime import date, datetime
from pytz import timezone as tz
from libraries.Functions import discount_active

from apps.users.models import UserWalletLog


class GetUsers(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        mobile = request.POST.get('mobile')

        try:
            user, created = User.objects.get_or_create(mobile=mobile, username=mobile)
            user.groups.add(Group.objects.get(name='User'))
            user_data = UserSerializer(user).data

        except IntegrityError:
            return JsonResponse({'data': '', 'status': False,
                                 'message': "This mobile registered as a manager. Please user other mobile number!"})
        except Exception:
            return JsonResponse({'data': '', 'status': False,
                                 'message': "Something went wrong..!!"})

        if created:
            return JsonResponse({'data': user_data, 'status': True, 'new_user': True, 'message': "New User"})
        else:
            return JsonResponse({'data': user_data, 'status': True, 'new_user': False, 'message': "Existing User"})


class UpdateUserName(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        User.objects.filter(mobile=mobile).update(name=name)
        return JsonResponse({'status': True})


class GetOrders(GroupRequiredMixin, View):
    group_required = ['Owner', 'Manager']

    def post(self, request):
        order_status = request.POST.get('order_status')
        kitchen_id = request.POST.get("kitchen_id")
        if "Owner" in request.user.group_name:
            if order_status is not "" and kitchen_id is not "":

                qs = Order.objects.filter(order_status=order_status, kitchen_id=kitchen_id)

            elif order_status is not "" and kitchen_id is "":

                qs = Order.objects.filter(order_status=order_status)

            elif order_status is "" and kitchen_id is not "":

                qs = Order.objects.filter(kitchen_id=kitchen_id)

            else:

                qs = Order.objects.all()

        else:
            if order_status is not "" and kitchen_id is not "":

                qs = Order.objects.filter(order_status=order_status, kitchen_id=kitchen_id)

            elif order_status is not "" and kitchen_id is "":

                qs = Order.objects.filter(order_status=order_status, kitchen__manager__manager=request.user)

            elif order_status is "" and kitchen_id is not "":

                qs = Order.objects.filter(kitchen_id=kitchen_id)
            else:
                qs = Order.objects.filter(kitchen__manager__manager=request.user)

        datatable = DataTables(request, Order)
        datatable.COLUMN_SEARCH = ['order_no', 'user__name', 'user__mobile', 'delivery_address']
        datatable.select('id', 'order_no', 'user__name', 'user__mobile', 'grand_total', 'delivery_address',
                         'created_on', 'order_status', 'status')
        datatable.set_queryset(qs)
        # print(datatable.set_queryset(qs))

        return datatable.response()


class FindItems(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        response = {'status': False, 'msg': '', 'data': {}}
        item_name = request.POST.get('item_name')
        kitchen_id = request.POST.get('kitchen_id')
        try:

            items = Item.objects.values('name', 'id', 'is_outof_stock').filter(name__icontains=item_name,
                                                                               category__kitchen_id=kitchen_id)[:5]

            response['status'] = True
            response['data'] = list(items)
        except Exception as e:
            print(e)
            response['status'] = False
            response['msg'] = 'Some error occurred! Please reload the page'

        return JsonResponse(response)


class GetItemDetails(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        response = {'status': False, 'msg': '', 'data': {}}
        item_id = request.POST.get('item_id')
        try:
            item = Item.objects.get(id=item_id)
            item_detail_serializer_data = ItemDetailSerializer(item)
            response['status'] = True
            response['data'] = item_detail_serializer_data.data
        except Exception as e:
            print(e)
            response['status'] = False
            response['msg'] = 'Some error occured ! Please reload the page'

        return JsonResponse(response)


class SaveOrder(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        response = {'status': False, 'msg': '', 'data': {}}
        data = request.POST
        mobile = data.get('mobile')
        delivery_type = data.get('delivery_type')
        full_address = ''
        user = User.objects.select_related('userwallet').get(mobile=mobile)
        user_wallet = int(user.userwallet.amount)
        if user.group_name == 'Manager':
            response['status'] = False
            response['message'] = 'This mobile registered as a manager. Please user other mobile number!'
            return JsonResponse(response)

        else:
            if delivery_type == "DELIVERY":
                address_type = data.get('address_type')
                address_line1 = data.get('address_line1')
                address_line2 = data.get('address_line2')
                # state = data.get('state')
                pincode = data.get('pin')
                address_id = data.get('address_id')
                deliver_to = data.get('deliver_to')

                if address_id:
                    """
                    Address Update Process:- If address_id availble it will update the  address as per input.
                    
                    """
                    Address.objects.filter(id=int(address_id)).update(address_type=address_type,
                                                                      address_line1=address_line1,
                                                                      address_line2=address_line2,
                                                                      pincode=pincode, country="India",
                                                                      created_on=timezone.now(),
                                                                      user_id=user.id)
                elif address_type in ["HOME", "WORK","OTHERS"]:

                    """
                    Address Update Process:- If address_id not set and address type is in [HOME, WORK]
                    it will fetch the based on address_type and user
                    and update the user's address as per input.
    
                    """
                    address = Address.objects.filter(user_id=user.id, address_type=address_type).update(
                        address_type=address_type,
                        address_line1=address_line1,
                        address_line2=address_line2,
                        # state=state,
                        pincode=pincode, country="India",
                        created_on=timezone.now(),
                        user_id=user.id)
                    if address ==0:
                        """
                            if above fails to update the user's address it will falls in this condition,
                            and create a new address with new address type
                        """
                        Address.objects.create(address_type=address_type,
                                               address_line1=address_line1,
                                               address_line2=address_line2,
                                               deliver_to=deliver_to,
                                               # state=state,
                                               pincode=pincode, country="India",
                                               created_on=timezone.now(),
                                               user_id=user.id)
                full_address = ','.join(
                    [address_type, address_line1, address_line2,
                     pincode]) if address_line1 else None  # it will save in order tabel.


            curr_fin_year = FinancialYear.objects.all()
            try:
                last_order = Order.objects.latest('id')  # Get last Order Detail for Order no. and order_receipt_no
                last_order_no = last_order.order_no
                last_receipt = last_order.receipt_no
                order_fin_year = last_order.financial_year

            except Exception as e:
                last_order_no = '0'
                last_receipt = '0'
                order_fin_year = None

            if len(curr_fin_year) == 1:
                curr_fin_year = FinancialYear.objects.get(id=curr_fin_year[0].id).financial_year

            if order_fin_year and (
                    order_fin_year == curr_fin_year):  # Restart Receipt_no from 1 if Financial Year change.
                receipt_no = eval(last_receipt) + 1
            else:
                receipt_no = 1

            order_status = data.get('order_status')
            ordered_items = eval(data.get('order_item'))
            payable_price = data.get('payable_price')
            grand_total = eval(data.get('grand_total'))
            actual_grand_total = eval(data.get('actual_grand_total'))
            points = eval(data.get('points'))

            try:
                if points >= actual_grand_total:
                    points = actual_grand_total
                    user.userwallet.amount = user_wallet - int(actual_grand_total)
                    user.save()
                    UserWalletLog.objects.create(user_id=user.id, amount=-float(actual_grand_total),
                                                 wallet_log_for="spent against order no {}".format(
                                                     eval(last_order_no) + 1),
                                                 created_on=timezone.now())
                else:
                    user.userwallet.amount = user_wallet - int(points)
                    user.save()
                    UserWalletLog.objects.create(user_id=user.id, amount=-float(points),
                                                 wallet_log_for="spent against order no {}".format(
                                                     eval(last_order_no) + 1),
                                                 created_on=timezone.now())

                order = Order.objects.create(
                    purchase_method=data.get('payment_method'),
                    estimated_delivery_time=45,
                    offer_id=1,
                    earn_points=eval(data.get('payable_price')) / 10,
                    created_on=timezone.now(),
                    updated_on=timezone.now(),
                    order_notes='first_order',
                    delivery_address=full_address if full_address else "SELF-PICKED Order",
                    delivery_type=data.get('delivery_type', "SELF-PICKED"),
                    delivery_boy=data.get('delivery_boy', ''),
                    special_note=data.get('special_note'),
                    points=points,
                    delivery_charge=data.get('delivery_charge'),
                    total_price=data.get('total_price'),
                    total_discount=data.get('discount'),
                    packaging_charges=data.get('packing_charge'),
                    order_status=data.get('order_status'),
                    grand_total=grand_total,
                    payable_price=payable_price,
                    kitchen_id=data.get('kitchen'),
                    user_id=user.id,
                    financial_year=curr_fin_year,
                    receipt_no=receipt_no,
                    order_no=eval(last_order_no) + 1
                )
                OrderLog.objects.create(
                    order_status=order_status,
                    created_on=timezone.now(),
                    order_id=order.id,
                    updated_by=request.user,
                )
                for item in ordered_items:
                    OrderItems.objects.create(order_id=order.id, offer_id=1, **item)

                SendSms().pkb_order_confirmation(number=mobile, order_id=order.order_no, estimated_delivery_time=45)

                response['status'] = True
                response['msg'] = 'Order successfully placed'
                layer = get_channel_layer()
                # kitchen = Kitchen.objects.get(id=data.get('kitchen'))
                # print(kitchen.group_name)
                async_to_sync(layer.group_send)('kitchen', {
                    "type": "kitchen.message",
                    "kitchen_id": data.get('kitchen'),
                    "username": request.user.username,
                    "message": "{}".format(model_to_dict(order)),
                })
            except Exception as e:
                print(e)
                response['status'] = False
                response['msg'] = str(e)

            return JsonResponse(response)


class Orders(GroupRequiredMixin, View):
    group_required = ['Manager','Owner' ]

    template_name = 'orders/takeorder.html'

    def get(self, request):
        kitchen = Kitchen.objects.get(manager__manager=request.user)

        delivery = KitchenDelivery.objects.filter(kitchen=kitchen)

        delivery_boy = [delivery_boy.deliver_boy for delivery_boy in delivery]
        return render(request, self.template_name, {'delivery_boys': delivery_boy,'kitchen':kitchen})


class AllOrders(GroupRequiredMixin, View):
    group_required = ['Owner', 'Manager']

    template_name = 'orders/allorder.html'

    def get(self, request):
        user = request.user
        if "Owner" in request.user.group_name:
            store = request.user.storeowner.store.id
            kitchens = Kitchen.objects.filter(store_id=store,is_deleted=False)

            return render(request, self.template_name, {"kitchens": kitchens})
        else:
            kitchens = Kitchen.objects.get(is_deleted=False, manager__manager=user)
            return render(request, self.template_name, {"kitchens": kitchens})


class OrderDetail(GroupRequiredMixin, View):
    group_required = ['Owner', 'Manager']
    template_name = 'orders/vieworder.html'

    def get(self, request, pk):
        items = []
        order = Order.objects.get(pk=pk)
        user = User.objects.get(pk=order.user_id)
        order_item = OrderItems.objects.filter(order_id=pk)
        total_tax = OrderItems.objects.filter(order_id=pk).aggregate(Sum('tax_value'))
        order_logs = OrderLog.objects.filter(order_id=pk)
        delivery_boy_no = order.delivery_boy
        delivery = KitchenDelivery.objects.filter(kitchen=order.kitchen)

        delivery_boy = [delivery_boy.deliver_boy for delivery_boy in delivery]

        # print( order_logs)
        for order_item in order_item:
            items.append(order_item)

        return render(request, self.template_name, {"order": order, 'user': user, 'order_item': items,
                                                    'total_tax': total_tax['tax_value__sum'],
                                                    'user_mobile': user.mobile,
                                                    'delivery_address': order.delivery_address,
                                                    'order_logs': order_logs,
                                                    'delivery_boy': delivery_boy,
                                                    'deliver_boy_name': User.objects.get(
                                                        id=delivery_boy_no).name if delivery_boy_no else "Not assigned"})


class UpdateOrder(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']

    def post(self, request):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        user = User.objects.get(pk=order.user_id)
        mobile = user.mobile
        order_status = request.POST.get('order_status')
        delivery_id = request.POST.get('user_id')
        estimated_delivery_time = request.POST.get('estimated_delivery_time')
        if estimated_delivery_time and order_status == Order.ORDER_STATUS_CONFIRMED:
            Order.objects.filter(id=order_id).update(
                order_status=order_status,
                estimated_delivery_time=estimated_delivery_time,
                delivery_boy=delivery_id
            )
            OrderLog.objects.create(
                order_status=order_status,
                created_on=timezone.now(),
                order_id=order_id,
                updated_by=request.user,
            )
            SendSms().pkb_order_confirmation(number=mobile, order_id=order.order_no,
                                             estimated_delivery_time=estimated_delivery_time)
            return JsonResponse({'status': True, 'message': 'Order status Update Successfully!'})
        else:
            Order.objects.filter(id=order_id).update(
                order_status=order_status,
            )
            OrderLog.objects.create(
                order_status=order_status,
                created_on=timezone.now(),
                order_id=order_id,
                updated_by=request.user,
            )
            if order_status == Order.ORDER_STATUS_CONFIRMED:
                # print(order.earn_points)
                credit_amount = int(order.earn_points)
                user_wallet = UserWallet.objects.get(user_id=order.user_id)
                user_wallet.amount = int(credit_amount + user_wallet.amount)
                UserWallet.save()

                OrderLog.objects.create(
                    order_status=order_status,
                    created_on=timezone.now(),
                    order_id=order_id,
                    updated_by=request.user,
                )

                SendSms().pkb_order_delivered(number=mobile, credit_point=credit_amount, total_point=user_wallet.amount)

            if order_status == Order.ORDER_STATUS_DECLINED:
                OrderLog.objects.create(
                    order_status=order_status,
                    created_on=timezone.now(),
                    order_id=order_id,
                    updated_by=request.user,
                )
                SendSms().pkb_order_canceled(number=mobile, order_id=order.order_no)

            return JsonResponse({'status': True, 'message': 'Order status Update Successfully!'})


class GetRecentOrder(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'orders/recent_order.html'

    def get(self, request):
        mobile = request.GET.get('mobile')

        try:
            user = User.objects.get(mobile=mobile)
            orders = user.order_set.all().order_by('-id')

            return render(request, self.template_name, {'orders': orders[:5], 'return_user': user})


        except Exception as e:

            return render(request, self.template_name, {'error': 'Something went wrong'})


class Reorder(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'orders/re_order.html'

    def get(self, request):
        order_id = request.GET.get('re_order_id')
        print(dir(request.user))

        sub_total = 0.00   # total items core prices
        sub_total_tax = 0.00  # total applied calculated taxes
        total_with_taxes = 0.00  # total items core prices+ total applied taxes
        sub_total_discount = 0.00  # total applied calculated discounts




        try:
            order = Order.objects.get(id=order_id)
            item_ids = order.orderitems.all()
            delivery_boys_query = KitchenDelivery.objects.filter(kitchen=order.kitchen)

            delivery_boys = [delivery_boy.deliver_boy for delivery_boy in delivery_boys_query]

            order_items_info = []
            discount_list = []
            indian_time = tz('Asia/Kolkata')

            for ord_item in item_ids:

                if ord_item.item.is_variant:

                    item_price_obj = ItemPrice.objects.get(item=ord_item.item, quantity_type=ord_item.quantity_type)

                    sub_total += float((item_price_obj.price)*ord_item.quantity)

                    total_tax = 0.0
                    item_total_tax_amount_title = ''

                    for tax in item_price_obj.item.item_taxes.all():
                        if not tax.tax.is_deleted:
                            item_total_tax_amount_title += tax.tax.title + '@' + str(tax.tax.amount)
                            total_tax += float(tax.tax.amount)

                    sub_total_tax += self.calculate_percent(item_price_obj.price, total_tax)* ord_item.quantity # for tax calculation

                    total_with_taxes = sub_total + sub_total_tax

                    total_discount = 0.0
                    item_total_discount_amount_title = ''

                    for discount in item_price_obj.item.discount_items.all():
                        if not discount.discount.is_deleted and discount_active(discount):
                            item_total_discount_amount_title += discount.discount.title + '@' + str(
                                discount.discount.percentage)
                            total_discount = total_discount + float(discount.discount.percentage)

                    sub_total_discount += self.calculate_percent(item_price_obj.price, total_discount)*ord_item.quantity  # for discount percent calculation

                    item_data = {
                        'name': item_price_obj.item.name,
                        'id': item_price_obj.item.id,
                        'total_tax': round(total_tax,2),
                        'total_tax_amount_title_string': item_total_tax_amount_title,
                        'quantity': ord_item.quantity,
                        'quantity_type': ord_item.quantity_type,
                        'unit_price': round(item_price_obj.price,2),
                        'total_discount': round(total_discount,2) if total_discount else 0.0,
                        'total_discount_amount_string': item_total_discount_amount_title,
                    }
                    order_items_info.append(item_data)

                else:

                    item_obj = Item.objects.get(id=ord_item.item_id)

                    # manage Taxes
                    sub_total+=(float(item_obj.base_price))*ord_item.quantity

                    total_tax = 0.0
                    item_total_tax_amount_title = ''

                    for tax in item_obj.item_taxes.all():
                        if not tax.tax.is_deleted:
                            item_total_tax_amount_title += tax.tax.title + '@' + str(tax.tax.amount)
                            total_tax = total_tax + float(tax.tax.amount)

                    sub_total_tax += self.calculate_percent(item_obj.base_price, total_tax)*ord_item.quantity  # for tax calculation
                    total_with_taxes = float(sub_total) + sub_total_tax

                    # manage Discount
                    total_discount = 0.0
                    item_total_discount_amount_title = ''

                    for discount in item_obj.discount_items.all():
                        if not discount.discount.is_deleted and discount_active(discount):
                            item_total_discount_amount_title += discount.discount.title + '@' + str(
                                discount.discount.percentage)
                            total_discount = total_discount + float(discount.discount.percentage)

                    sub_total_discount += self.calculate_percent(item_obj.base_price, total_discount)*ord_item.quantity

                    item_data = {
                        'name': item_obj.name,
                        'id': item_obj.id,
                        'total_tax': total_tax,
                        'total_tax_amount_title_string': item_total_tax_amount_title,
                        'quantity': ord_item.quantity,
                        'quantity_type': ord_item.quantity_type if ord_item.quantity_type else 'BASE',
                        'unit_price': item_obj.base_price,
                        'total_discount': total_discount if total_discount else 0.0,
                        'total_discount_amount_string': item_total_discount_amount_title
                    }
                    order_items_info.append(item_data)

            return render(request, self.template_name,
                          {'order': order,
                           'items_detail': order_items_info,
                           'delivery_boys': delivery_boys,
                           'sub_total': round(sub_total,2),
                           'item_price_with_tax': round(total_with_taxes,2),
                           'sub_total_tax': round(sub_total_tax,2),
                           'sub_total_discount': round(sub_total_discount,2),
                           'grand_total': (float(total_with_taxes)+float(order.kitchen.packing_charges)+float(order.kitchen.delivery_charges))-float(sub_total_discount)

                           })

        except Exception as e:
            print(e)
            return render(request, self.template_name, {'error': 'Something went wrong'})

    @staticmethod
    def calculate_percent(price, percent):
        return (float(price )* float(percent))/100


class OrderBill(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'orders/bill.html'

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            order_tax = order.orderitems.all().aggregate(Sum('tax_value'))
            print(order_tax, "Hello")

            return render(request, self.template_name, {'order': order, 'total_tax': order_tax['tax_value__sum']})

        except Exception as e:
            print(e)
            return render(request, self.template_name, {'error': 'Something went wrong'})


class OrderKOT(GroupRequiredMixin, View):
    group_required = ['Super admin', 'Manager']
    template_name = 'orders/kot.html'

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        return render(request, self.template_name, {'order': order})
