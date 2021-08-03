/*******Adding New Address:  Take Order page.********/
$("#new_address").click(function () {
    $('input[name=address]').prop('checked', false)
    //$('#address_field').toggle();
    $('#address_line1').val('');
    $('#address_type').val('');
    $('#deliver_to').val('');
    $('#address_id').val('');
    $('#address_line2').val('');
    $('#state').val('');
    $('#pin').val('');

});
 $("#old_adress").hide();
$("#address_type").change(function(){
var address_type = $(this).val();
if (address_type == "OTHERS"){
$('.deliver_to').show()
}
else{
$('.deliver_to').hide()
}
});
/****END Adding New Address****/
/* reset counter */

function reset_counter(){
    $('.selected_items tr').each(function (index) {
        $(this).find('.counter').text($(this).index()+1)
    })
}
/* end reset counter */

/*******Set Address Field for User Existing Address********/

$('.pre_address').on('click', '.address', function () {

    if($("input[name=delivery_type]:checked").val()=="DELIVERY"){
        selected_address = $(this).siblings('.select_address').text()
        address_type = $(this).siblings('.select_address').find('.address_type').text()
        deliver_to = $(this).siblings('.select_address').find('.deliver_to').text()
        address_line1 = $(this).siblings('.select_address').find('.address_line1').text()
        address_line2 = $(this).siblings('.select_address').find('.address_line2').text()
        state_name = $(this).siblings('.select_address').find('.state_name').text()
        pincode = $(this).siblings('.select_address').find('.pincode').text()
        address_id=$('input[name=address]').val()
        $('#address_field').show();
        $('#address_type').val(address_type);
        if (address_type == "OTHERS"){
        $('.deliver_to').show();
        }
        else{
            $('.deliver_to').hide();
        };

        $.each($("input[name=address_type]"), function( index, inputradio) {
            $(inputradio).removeAttr('checked');

            if(inputradio.value==address_type){
                 $(inputradio).attr('checked', true);
            }
            else{

            }
        });

        $("input[name=delivery_type]")
        $('#deliver_to').val(deliver_to);
        $('#address_line1').val(address_line1);
        $('#address_line2').val(address_line2);
        $('#state').val(state_name);
        $('#pin').val(pincode);
        $('#address_id').val(address_id);


    }

});
/*******END:- Setting Address Field********/


$('#mobile').focusout(function () {

    /*******
        Fetching User Details From Mobile Number:
        If New Mobile Number It will create New User.

    ********/
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var mobile = $(this).val();
    if($("input[name=delivery_type]:checked").val()=="DELIVERY"){
        $("#old_adress").show();
     }


    var fullname = $('#user_name').val();

    if (mobile.length >= 10) {
        $.ajax({
            url: "/admin/getuser/",
            type: "POST",
            data: {
                'mobile': mobile,
                'name': fullname,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (res) {
                if (res.status) {
                    if(res.new_user==false){
                        $('#recent_order_btn').css('display', 'block')
                        address = ''
                        $('.wallet_amount').text(res.data.wallet_point);
                        $('#user_name').val(res.data.name)
                        $("#newuser").text('');
                        $('.pre_address').html('')

                        if (res.data.address.length > 0) {
                            $.each(res.data.address, function (index, obj) {

                                address += `<label  class="col-md-3 col-sm-3 col-xs-12 pre_address"><input type="radio" name='address' class='address' value=` + obj.id + `>
                                    <address class="select_address"><span class="address_type">` + obj.address_type + `</span>
                                    <span class="deliver_to">` + obj.deliver_to + `</span>,
                                    <span class="address_line1"> ` + obj.address_line1 + `</span>,
                                    <span class="address_line2"> ` + obj.address_line2 + `</span> <br>
                                    <span > ` + obj.country + `</span>,
                                    <span class="pincode">` + obj.pincode + `</span>
                                    </address></label>`;
                            });
                        $('.pre_address').append(address)

                        }
                    else {
                        $('.pre_address').html('<p>N/A<p>');
                        }
                    }
                else{
                    $("#newuser").text("This is new user");
                    $('.wallet_amount').text(res.data.wallet_point);
                }
                }
            else {
                alert(res.message);
                $('#mobile').val('');
                $('#user_name').val('');

            }
            }
        });
    }
});
/*******END:- User's Detail Fetching ********/

$('#user_name').focusout(function () {


    /*******
        Creating/updating User's Name based On Mobile Number

    ********/
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var mobile = $('#mobile').val();
    var fullname = $('#user_name').val();
    console.log(fullname, mobile)
    if (mobile.length >= 10) {
        $.ajax({
            url: "/admin/update-username/",
            type: "POST",
            data: {
                'mobile': mobile,
                'name': fullname,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (res) {

            }
        });
    }
});

count = 1

// Manage SubTotal Amount
function addSubTotal() {
    var TotalValue = 0;
    $(".selected_items tr").each(function () {
        TotalValue += parseFloat($(this).find('.total').text());
    });
    return (TotalValue > 0) ? TotalValue : '0.00';
}

// Manage Payable Amount
function payable_amount() {
    var subtotal = addSubTotal();
    var taxes = Number($('#applied_taxes').text());
    var payable_amount = subtotal + (taxes)
    return (payable_amount > 0) ? payable_amount : 0.00;
}

// Manage Grand Total
function grandTotal() {
    var subtotal = addSubTotal();
    //var packing_charge = packingCharge();
    var packing_charge = Number($('#packing_charge').text());
    var shipping_value = Number($('#shipping_value').val());
    var redeem_value = Number($('#redeem_points').text());
   // var discount_value = Number($('#discount_value').val());
    var total_tax_value = Number($('#applied_taxes').text())
    var applied_discount = Number($('#applied_discount').text());
    var payable_amount = (subtotal + shipping_value + packing_charge + total_tax_value) - (redeem_value + applied_discount)
    var actual_grand_total = (subtotal + shipping_value + packing_charge + total_tax_value) - (applied_discount)
    $("#actual_grand_total").text(actual_grand_total)
    return ((payable_amount) > 0) ? (payable_amount) : '0.00';
}

// Manage Packing Charges

//function packingCharge() {
//    var packing_charge;
//    var subtotal = addSubTotal();
//    var shipping_value = Number($('#shipping_value').val());
//    var redeem_value = Number($('#redeem_points').text());
//    var discount_value = Number($('#discount_value').val());
//    //$('#applied_discount').text(calculateTotalDiscount())
//    var payable_amount = (subtotal + shipping_value) - (redeem_value + discount_value)
//
//    if (payable_amount <= 150) {
//        packing_charge = 0.00
//    } else {
//        if (payable_amount > 150 && payable_amount <= 300) {
//            packing_charge = 10.00;
//        } else if (payable_amount > 300 && payable_amount <= 600) {
//            packing_charge = 20.00;
//        } else {
//            packing_charge = 30.00;
//        }
//    }
//    return packing_charge;
//}




//Manage Detail if Shipping value Changes
//$("#shipping_value").change(function () {
//    var shipping_value = $(this).val();
//    if (shipping_value == '') {
//        shipping_value = 0
//    }
//    var grand_total = grandTotal();
//    $('#grand_total').text(grand_total);
//});


//$("#discount_value").change(function () {
//    var grand_total = grandTotal();
//    $('#grand_total').text(grandTotal());
//    $('#payable_amount').text(payable_amount());
//    $('#packing_charge').text(Number($('#packing_charge').text()))
//    $('#grand_total').text(grand_total);
//
//})


// Manage Selected Item after  removing any of them

$(".selected_items").on("click", ".close", function () {

    item_price = Number($(this).closest('tr').find('.total').text());
    tax_on_item = Number($(this).closest('tr').find('.total_tax').text());
    discount_on_item = Number($(this).closest('tr').find('.discount_on_item').text());
    quantity = Number($(this).closest('tr').find('.item_quantity').val());
    //total_discount_on_item = (discount_on_item * quantity)
    total_discount_on_item = calculateDiscount(item_price, discount_on_item);
    total_tax = calculateTax(item_price, tax_on_item);

    so_for_tax = Number($('#applied_taxes').text());
    so_for_discount = Number($('#applied_discount').text());

    new_total_tax = so_for_tax - total_tax;
    new_total_discount = so_for_discount - total_discount_on_item;

    $('#applied_taxes').text(new_total_tax.toFixed(2))
    $('#applied_discount').text(new_total_discount.toFixed(2))

    $(this).closest("tr").remove();

    $('#packing_charge').text(Number($('#packing_charge').text()))
    $('#subtotal').text(addSubTotal());
    $('#grand_total').text(grandTotal());
    $('#payable_amount').text(payable_amount());
    $('#grand_total').text(grandTotal());

    reset_counter();

});

//Collect the all data from Form and  item order table here

$(document).ready(function () {

    $('.save_order').click(function () {

        var formdata = new FormData($("#order_form")[0])

        formdata.append("payable_price", payable_amount());

        formdata.append("points", Number($('#redeem_points').text()));


        if($("input[name=delivery_type]:checked").val()=="DELIVERY"){

            formdata.append("delivery_charge", Number($('#shipping_value').val()));
        }
        else{

            formdata.append("delivery_charge", '0.0');

        }

        formdata.append("total_price", addSubTotal());
        formdata.append("discount", Number($('#applied_discount').text()));
        formdata.append("packing_charge", Number($('#packing_charge').text()));
        formdata.append("grand_total", grandTotal());
        formdata.append("actual_grand_total", Number($('#actual_grand_total').text()));
        formdata.append("special_note", ($('input[name=special_note]').val()));


        formdata.append("order_status", 1); // 1 order confirmation

        var delivery_type = $('input[name=delivery_type]:checked').val();
        var address_type = $('input[name=address_type]:checked').val();
        var address_id = $('input[name=address]:checked').val();
        if(address_id==undefined){
            address_id =''
        }
        var payment_method = $('input[name=payment_method]:checked').val();

        var address_line1 = $('#address_line1').val();
        var address_line2 = $('#address_line2').val();
        //var state = $('#state').val();
        var pin = $('#pin').val();

        formdata.append("address_type", address_type);
        formdata.append("address_id", address_id);
        formdata.append("address_line1", address_line1);
        formdata.append("address_line2", address_line2);
        formdata.append("payment_method", payment_method);
        formdata.append("delivery_type", delivery_type)
        formdata.append("kitchen", $(".kitchen_list option:selected").val())

        if($("input[name=delivery_type]:checked").val()=="DELIVERY"){
        formdata.append("delivery_boy", $("#delivery_boy option:selected").val())
        }
        else{
        formdata.append("delivery_boy", '')
        }

        //formdata.append("state", state);

        formdata.append("pin", pin);


        var order_item = []

        $('.selected_items tr').each(function () {

            item_id = $(this).find('.item').data('item_id');
            quantity = $(this).find('.item_quantity').val();
            variant_type = $(this).find('.quantity_type').text();
            total = $(this).find('.total').text();
            unit_price = $(this).find('.unit').text();
            tax_on_item = parseFloat($(this).find(".total_tax").text());
            calculated_tax = calculateTax(total, tax_on_item);
            data = {
                item_id: item_id,
                quantity: quantity,
                quantity_type: variant_type,
                total_price: total,
                unit_price: unit_price,
                'tax_value': calculated_tax
            }
            order_item.push(data);
        });

        formdata.append("order_item", JSON.stringify(order_item));
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        formdata.append("csrfmiddlewaretoken", csrftoken);

        if ($("#order_form").isValid()) {
            console.log(order_item)
            if ($('.selected_items tr').length > 0) {
                loader($('.save_order'));
                $.ajax({
                    url: '/admin/saveorder/',
                    type: "POST",
                    data: formdata,
                    processData: false,
                    contentType: false,
                    success: function (res) {
                        if (res.status) {
                            new PNotify({
                                title: 'Success!',
                                text: 'Order Updated successfully.',
                                type: 'success',
                                styling: 'bootstrap3',
                                nonblock: {
                                    nonblock: true
                                }
                            });

                            window.location.href = "/admin/allorder/";

                        }
                        else{
                        alert(res.message)
                        reset_loader($('.save_order'));

                        }
                    }
                });
            } else {
                bootbox.alert("please select Item");
                reset_loader($('.save_order'));
            }
        } else {
            bootbox.alert("please fill all the required field.");
            reset_loader($('.save_order'));
        }
    });
});


//Apply/un-apply User's Point.
$('#redeem_checkbox').click(function () {
    var wallet_amount = $('.wallet_amount').text();
    if ($('#redeem_checkbox').is(':checked')) {
        $('#redeem_points').text(wallet_amount);
        $('#subtotal').text(addSubTotal());
        $('#grand_total').text(grandTotal());
        $('#payable_amount').text(payable_amount());
        $('#grand_total').text(grandTotal());
    } else {
        $('#redeem_points').text('0.00');
        $('#subtotal').text(addSubTotal());
        $('#grand_total').text(grandTotal());
        $('#payable_amount').text(payable_amount());
        $('#grand_total').text(grandTotal());
    }
});

/*-------------
for auto fill item
---------------*/

$(document).ready(function () {
    var hide_list = true;
    $(".item_list").hover(function () {
        hide_list = false
    }, function () {
        hide_list = true
    });

    // AUTO Suggestion Item  List.
    $("#search_item").on('keyup', function (event) {
        var val = $(this).val();
        var kitchen_id = $('#kitchen').val()
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        console.log(val, val.length)
        if(val.length!=0){
        /*calling ajax to get matching order list */
            $.post('/admin/finditems/', {
                item_name: val,
                kitchen_id: kitchen_id,
                csrfmiddlewaretoken: csrftoken,
            }, function (res) {
                $(".item_list .items").show();
                $(".item_list .items").html('')

                if (res.data.length > 0) {
                    $(".item_list").show()
                    $.each(res.data, function (i, u) {
                        var out_of_stock = (u.is_outof_stock) ? '<i class="fa fa-ban" style="font-size:20px;color:red"><span style="font-size:15px;color:red;"" > Not available</span></i>' : '';
                        var out_of_stock_class = (u.is_outof_stock) ? "out_of_stock" : "";

                        var user_html = $(`<li class="` + out_of_stock_class + `" data-toggle="modal" data-id="` + u.id + `">` + u.name + '   ' + out_of_stock + `</li>`);
                        $(".item_list .items").show();
                        $(".item_list .items").append(user_html);
                    })
                } else {

                    $(".item_list .items").show();
                    $(".item_list .items").html("<p class='not_match'>No Match Found<p>");
                }
            })
        }
        else {
            $(".item_list .items").hide()
        }
    });
});

// Selecting ITEM From  auto suggestion  ITEM LIST
count = $('.selected_items tr').length;

$('.items').on('click', 'li', function () {
    count = $('.selected_items tr').length;
    var id = $(this).data('id');
    console.log(id, "item_id")
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $(".item_list .items").hide();

    $.post('/admin/itemdetails/', {
        item_id: id,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        console.log(data);
        data = data.data


        var list = $(`<tr>
                       <td class="delete_order"><button type="button" class="close" aria-label="Close">
                       <span aria-hidden="true">&times;</span>
                       </button></td>
                       <td class="counter"></td>
                       <td class="item" data-item_id='0'>
                       <span class='item_name'></span>
                       <span class='total_bg'><span class='item_tax'></span>
                       <div class='total_tax hidden'></div>
                       <span class='discount_val'></span>
                       <span class='discount_on_item hidden'></span>
                       </td>
                       <td class="quantity_type">50</td>
                       <td class="quantity">1</td>
                       <td class="unit">1</td>
                       <td class="total"></td>
                   </tr>`)

        var variant_items = $(`<div class="card col-lg-6">
                            <div class="card-body text-center card_pop variant_item_detail">
                            <p class="card-text variant_type">Half</p>
                            <p class="card-text variant_price" data-total_tax='0' data-total_discount='0' >0</p>
                            </div>
                            </div>`)

        $(".counter", list).text(++count);
        $(".category", list).text(data.name);
        $(".item .item_name", list).text(data.name);
        $(".item", list).attr('data-item_id', data.id);
        $(".quantity_type", list).html(`-`);

        if (data.is_variant == 1) {
            $('#myModal').modal('show');
            $('.modal-body').html('');

            $.each(data.item_prices, function (i, v) {


                $(".variant_type", variant_items).text(v.quantity_type);
                $(".variant_price", variant_items).text(v.price);
                $(".variant_price", variant_items).data('total_tax', data.total_tax);
                $(".variant_price", variant_items).data('total_discount', data.total_discount);

                $('.modal-body').append(variant_items);
            });
        }

        $(".quantity", list).html(`<div class='input-group plus-minus-input'>
                                            <div class='input-group-button minus'>
                                            <button type='button' class='button hollow circle' data-quantity='minus' data-field='quantity'>
                                            <i class='fa fa-minus' aria-hidden='true'></i></button></div>
                                            <input class='input-group-field input-number item_quantity' type='number' name='quantity' value='1'>
                                            <div class='input-group-button plus'>
                                            <button type='button' class='button hollow circle' data-quantity='plus' data-field='quantity'>
                                            <i class='fa fa-plus' aria-hidden='true'></i></button>
                                            </div>
                                            </div>`);

        $(".unit", list).text(data.base_price);
        $(".total", list).text(Number(data.base_price * 1));
        $(".total_tax", list).text(data.total_tax)
        $('.selected_items').append(list)
        console.log(Number(data.base_price * 1));
        var tax_html = '';
        var total_tax_on_item = 0
        $.each(data.tax_on_item, function (i, v) {
            tax_html += v.title + '@' + v.amount;
            total_tax_on_item += Number(v.amount);
        });
        $('.item_tax', list).html(tax_html)


        var discount_html = '';
        var total_discount_on_item = 0
        var applied_discount = parseFloat($('#applied_discount').text());

        $.each(data.discount_on_item, function (i, v) {
            discount_html += v.title + '@' + v.percentage + ',\n'
            total_discount_on_item += Number(v.percentage);
        });

        //total_applied = Number(applied_discount) + Number(data.total_discount)
         $('.discount_on_item',list).text(total_discount_on_item.toFixed(2))
         $('.discount_val', list).html(discount_html)

        if (data.is_variant != 1) {
        total_applied_for_item = calculateDiscount(data.base_price, data.total_discount);
            $('#applied_discount').text(Number(applied_discount)+Number(total_applied_for_item))  //applied_discount=from the total_discount, total_applied_for_item= for current item
        }

        if (data.is_variant != 1) {
            calculated_tax = calculateTax(data.base_price, data.total_tax);
            var applied_taxes = parseFloat($('#applied_taxes').text());
            sum_taxes = Number(applied_taxes) + Number(calculated_tax)
            $('#applied_taxes').text(sum_taxes.toFixed(2))
        }

//
//        if (data.is_variant == 1) {
//            calculated_discount = calculateDiscount(data.base_price, data.total_discount);
//            var applied_discount = parseFloat($('#applied_discount').text());
//            sum_discount = Number(applied_discount) + Number(calculated_discount)
//            //total_applied = Number(applied_discount) + Number(data.total_discount)
//            $('#applied_discount').text(sum_discount.toFixed(2))
//        }

        var subtotal = addSubTotal();
        var grand = grandTotal();
        $('#subtotal').text(subtotal);
        $('#packing_charge').text(Number($('#packing_charge').text()))
        $('#payable_amount').text(payable_amount());
        $('#grand_total').text(grandTotal());
        //$('#applied_discount').text(calculateTotalDiscount())

    });
});

function calculateTax(base_price, tax_val) {
    var tax = base_price * (tax_val / 100);
    return tax.toFixed(2);
}
function calculateDiscount(item_price, discount_percent) {
    var discount = item_price * (discount_percent / 100);
//       if(max>discount){
//        discount= discount
//       }
//       else{
//        discount= max
//       }
    return discount.toFixed(2);
}

$(".selected_items").on("click", ".plus", function (e) {

    /***
     Manage Taxes as Discount after (+1) items
    ***/

    var input = $(this).prev('.input-number');
    var val = parseFloat($(input).val(), 10);
    $(input).val(val + 1);
    var val = val + 1

    var that_row = $(this).closest("tr");
    var price = $(that_row).find('.unit').text();
    console.log("fididid ",price);
    tax_on_item = parseFloat($(that_row).find(".total_tax").text());
    discount_on_item = parseFloat($(that_row).find(".discount_on_item").text());
    console.log(discount_on_item)

    $(that_row).find(".total").text(parseFloat(val * price));

    for_appy_text = $('#applied_taxes').text();

    for_applied_discount_txt = $('#applied_discount').text();

    calculated_tax = calculateTax(price, tax_on_item);
    calculated_discount = calculateDiscount(price, discount_on_item)

    $('#applied_taxes').text(Number(for_appy_text) + Number(calculated_tax));
    $('#applied_discount').text(Number(for_applied_discount_txt) + Number(calculated_discount));

    var subtotal = addSubTotal();
    $('#subtotal').text(subtotal)
    $('#payable_amount').text(payable_amount());
    $('#packing_charge').text(Number($('#packing_charge').text()))
    $('#grand_total').text(grandTotal());
    //$('#applied_discount').text(calculateTotalDiscount())
})


$('.selected_items').on('click', '.minus', function () {

    /***
      Manage Taxes as Discount after (-1) items
    ***/

    var input = $(this).next('.input-number');
    var val = parseFloat($(input).val(), 10);
    $(input).val(val - 1);
    val = val - 1
    if (val == 0) {
        $(this).closest("tr").remove();
    }
    var that_row = $(this).closest("tr");
    price = $(that_row).find('.unit').text();

    tax_on_item = parseFloat($(that_row).find(".total_tax").text());
    discount_on_item = parseFloat($(that_row).find(".discount_on_item").text());

    $(that_row).find(".total").text(parseFloat(val * price));
    for_appy_text = $('#applied_taxes').text();
    for_applied_discount = $('#applied_discount').text();
    calculated_tax = calculateTax(price, tax_on_item);
    calculated_discount = calculateDiscount(price, discount_on_item)

    $('#applied_taxes').text(Number(for_appy_text) - Number(calculated_tax));
    //$('#applied_discount').text(Number(for_applied_discount) - Number(discount_on_item));
    $('#applied_discount').text(Number(for_applied_discount) - Number(calculated_discount));

    var subtotal = addSubTotal();
    $('#subtotal').text(subtotal)
    $('#payable_amount').text(payable_amount());
    $('#packing_charge').text(Number($('#packing_charge').text()))
    $('#grand_total').text(grandTotal());

})

// Selecting Item Quantity Type for POP-UP (e.g  Half/Full/Pcs)
$('.modal-body').on('click', '.variant_item_detail', function () {

    var this_row = $('.selected_items tr:last');
    price = (this_row).find('.unit').text();
    tax_on_item = parseFloat((this_row).find(".total_tax").text());


    this_row.find(".unit").text($(this).find('.variant_price').text());
    this_row.find(".quantity_type").text($(this).find('.variant_type').text());
    this_row.find(".total").text($(this).find('.variant_price').text());
    this_row.find(".total_tax").text($(this).find('.variant_price').data('total_tax'));
    this_row.find(".discount_on_item").text($(this).find('.variant_price').data('total_discount'));

    price = (this_row).find('.unit').text();
    tax_on_item = parseFloat((this_row).find(".total_tax").text());
    discount_on_item = parseFloat((this_row).find(".discount_on_item").text());

    $('#myModal').modal('hide');

    calculated_tax = calculateTax(price, tax_on_item);

    for_appy_txt = $('#applied_taxes').text();
    if ($('.selected_items tr').length > 1) {
        $('#applied_taxes').text(Number(for_appy_txt) + Number(calculated_tax));
    } else {
        $('#applied_taxes').text(Number(calculated_tax));
    }

    pre_discount = calculateDiscount(price, discount_on_item)

    for_apply_discount = $('#applied_discount').text();
    if ($('.selected_items tr').length > 1) {
        $('#applied_discount').text(Number(for_apply_discount) + Number(pre_discount));
    } else {
        $('#applied_discount').text(Number(pre_discount));
    }


    var subtotal = addSubTotal();
    $('#subtotal').text(subtotal)
    $('#payable_amount').text(payable_amount());
    $('#packing_charge').text(Number($('#packing_charge').text()))
    $('#grand_total').text(grandTotal());

})


// Link to  Redirect of user's Recent Order
$("#recent_order_btn").click(function () {
    mobile = $('#mobile').val()
    window.location = "/admin/recent-order/?mobile=" + mobile;
})

$('#taxes_detail').click(function () {
    /*******
    POP-UP for individual item Tax Detail
    ********/

    $('#tax_detail_modal').modal('show')
    $('.tax_detail_modal').html("")

    $('.selected_items tr').each(function () {

        name = $(this).find('.item_name').text();
        total_tax = $(this).find('.total_tax').text();
        total = $(this).find('.total').text();

        var tax_html = $(`<tr class="">
                        <td class="tax_item_name">
                            </td>
                            <td class="tax_total_value">
                            </td>
                            <td class="tax_total_tax_rate">
                            </td>
                            <td class="tax_total_tax">
                            </td>
                            </tr>`);

        $(".tax_item_name", tax_html).text(name)
        $(".tax_total_tax_rate", tax_html).text(Number(total_tax).toFixed(2))
        $(".tax_total_tax", tax_html).text(calculateTax(total, total_tax))
        $(".tax_total_value", tax_html).text(total)
        $('.tax_detail_modal').append(tax_html);
    });
});

$('#discount_detail').click(function () {
    /*******
        POP-UP for individual item Discount Detail
    ********/

    $('#discount_detail_modal').modal('show')
    $('.discount_detail_modal').html("")
    $('.selected_items tr').each(function () {

        name = $(this).find('.item_name').text();
        discount_on_item = Number($(this).find('.discount_on_item').text());
        quantity = Number($(this).find('.item_quantity').val());
        total = $(this).find('.total').text();

        var discount_html = $(`<tr class="">
                            <td class="discount_item_name">
                            </td>
                            <td class="item_total_value">
                            </td>
                            <td class="discount_total_value">
                            </td>
                            <td class="discount_quantity">
                            </td>
                            <td class="discounted_value">
                            </td>
                            </tr>`);

        $(".discount_item_name", discount_html).text(name)
        $(".item_total_value", discount_html).text(total)
       // $(".discount_total_value", discount_html).text(discount_on_item)
        $(".discount_total_value", discount_html).text(calculateDiscount(total, discount_on_item))

        $(".discount_quantity", discount_html).text(quantity)
        $(".discounted_value", discount_html).text(total - (calculateDiscount(total, discount_on_item)))
        $('.discount_detail_modal').append(discount_html);
    });
});

$(document).ready(function () {
    // Loading Form validator library
    $.validate({
        modules: 'date,security,file'
    });
});

$("input[name=delivery_type]").click(function(){

    if($("input[name=delivery_type]:checked").val()=="SELF-PICKUP"){

        $("#address_field").hide();
        $("#old_adress").hide();
        $("#reorder_address").hide();
        $("#shipping_value").val('0.00');
        $('#grand_total').text(grandTotal());
    }
    else{
        $("#address_field").show();
        $("#old_adress").show();
        $("#reorder_address").show();
        $("#shipping_value").val($(".kitchen_list option:selected").data('delivery_charges'));
        $('#grand_total').text(grandTotal());
    }
})
