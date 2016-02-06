function CartObject(settings, data_fields)
{

    this.settings = settings;
    this.data = data_fields;
    this.csrftoken = '';

    this.init = function()
    {
        this.csrftoken = this.getCsrftoken('csrftoken');
        var products = this.getProducts();
        if(!$.isEmptyObject(products))
        {
            this.getPreview(products);
            this.getTotalPrice(products);
            this.getTotalCount(products);
        }
        else
        {
            $('.removeContent').remove();
            console.log(this);
            $('.web_shop_cart-preview').html('<p style="float: left; padding-right: 41px; font-family: latolight; margin: 30px 0px 300px;">В корзине нет ни одного товара.</p>');
            return false;
        }
    };

    this.getCsrftoken = function(context)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, context.length + 1) == (context + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(context.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    this.addProduct = function(context)
    {
        var new_product = this.getDataFields(context);
        var thisObj = this;
        $.post("/api/add_product",
        {
            'p':new_product[this.data.id],
            'c':new_product[this.data.id_corrector],
            'csrfmiddlewaretoken':thisObj.csrftoken
        },
        function()
        {
            thisObj.getPreview(thisObj.getProducts());
        })
    };

    this.getProducts = function()
    {
        var thisObj = this;
        var products = {};
        $.ajax({
            url: '/api/get_products',
            async: false,
            type: 'POST',
            data:
            {
                'csrfmiddlewaretoken': thisObj.csrftoken
            },
            success: function (data)
            {
                products = data;
            }
        });

        return products;
    };

    this.getPreview = function(context)
    {
        var html = '';
        for (var obj in context)
        {
            if ((obj != 't_price') && (obj != 't_count'))
            {
                var c = context[obj];
                html +=
                '<div class="row body-cart">'+
                '<div class="col-sm-4 body-cart-cust-1">'+
                    '<img src="'+c['img_url']+'" alt="alt">'+
                    '<p class="product_name">'+c['p_name']+'</p>'+
                '</div>'+
                '<div class="col-sm-3 text-center call-1">'+
                    '<img class="product_count-remove_cart" data-p="'+ c['p'] +'" data-c="'+ ((c['c'] == null)?'':c['c']) +'" src="/static/images/add-good.png" alt="alt">'+
                    '<span class="all-good-cart count">'+c['p_count']+'</span>'+
                    '<img class="product_count-add_cart" data-p="'+ c['p'] +'" data-c="'+ ((c['c'] == null)?'':c['c']) +'" src="/static/images/rgood.png" alt="alt">'+
                '</div>'+
                '<div class="col-sm-2 price-cart-tr text-center">'+
                    '<p><span class="price">'+c['price']+'</span> грн</p>'+
                '</div>'+
                '<div class="col-sm-3 price-cart-tr">'+
                    '<p>' + (c['price'] * c['p_count']) + ' грн '+
                    '<img src="/static/images/delete_icon.png" class="product_delete" data-p="'+ c['p'] +'" data-c="'+ ((c['c'] == null)?'':c['c']) +'" alt="alt">'+
                    '</p>'+
                '</div>'+
            '</div>';
            }
        }

        if (html === '')
        {
            $('.removeContent').remove();
            console.log(this);
            $('.web_shop_cart-preview').html('<p style="float: left; padding-right: 41px; font-family: latolight; margin: 30px 0px 300px;">В корзине нет ни одного товара.</p>');
            return false;
        }

        this.getTotalCount(context);
        this.getTotalPrice(context);

        $(this.settings.cartPreviewClass).html(html);

        var CO = this;
        $(this.settings.cartPreviewClass).find(this.settings.productDeleteClass).click(function(){
            CO.deleteProduct(this);
        });

        $(this.settings.cartPreviewClass).find(this.settings.productAddItemClass).click(function(){
            CO.setAddProduct(this);
        });

        $(this.settings.cartPreviewClass).find(this.settings.productRemoveItemClass).click(function(){
            CO.setRemoveProduct(this);
        });

        return false;
    };

    this.getTotalPrice = function(context)
    {
        if (context['t_price'] == undefined)
        {
            $(this.settings.cartTotalPriceClass).html('');
        }
        else
        {
            $(this.settings.cartTotalPriceClass).html(context['t_price'] + ' грн.');
        }
    };

    this.getTotalCount = function(context)
    {
        if (context['t_price'] == undefined)
        {
            $(this.settings.cartTotalCountClass).html('');
        }
        else
        {
            $(this.settings.cartTotalCountClass).html(context['t_count']);
        }
    };

    this.getDataFields = function(context)
    {
        var data = {};
        var t = context.attributes;
        for (var i=0; i < t.length; i++)
        {
            if(t[i].name.substring(0, 5) == 'data-') {
                data[t[i].name.substring(5, t[i].name.length)] = t[i].value;
            }
        }
        return data;
    };

    this.setPriceCorrector = function(context)
    {
        var data_field = $(context).closest(this.settings.mainClass).find(this.settings.actionClass);

        data_field.attr('data-' + this.data.price, $(context).val());
        data_field.attr('data-' + this.data.id_corrector, $(context).attr('data-' + this.data.id_corrector));

        $(context).closest(this.settings.mainClass).find(this.settings.priceCorrectorPrintClass).html($(context).val());
    };

    this.deleteProduct = function(context)
    {
        var thisObj = this;
        var prod_del = this.getDataFields(context);

        $.post("/api/del_product",
        {
            'p':prod_del[thisObj.data.id],
            'c':prod_del[thisObj.data.id_corrector],
            'csrfmiddlewaretoken':thisObj.csrftoken
        },
        function()
        {
            thisObj.getPreview(thisObj.getProducts());
        });
        return true;
    };

    this.clearCart = function()
    {
        var thisObj = this;
        $.post("/api/clear_cart",
        {
            'csrfmiddlewaretoken':thisObj.csrftoken
        },
        function(data)
        {
            thisObj.getPreview(data);
        });
        return true;
    };

    this.renderOrderForm = function()
    {
        var products = this.getProducts();
        var html = '';

        for(var p in products)
        {
            if ((p != 't_count') && (p != 't_price'))
            {
                if (products[p]['c'] != null)
                {
                    html += '<input type="hidden" name="product_positions" value="' +
                        products[p]['p'] + ';' +
                        products[p]['p_count'] + ';' +
                        products[p]['c'] +
                    '">';
                }
                else
                {
                    html += '<input type="hidden" name="product_positions" value="' +
                        products[p]['p'] + ';' +
                        products[p]['p_count'] +
                    '">';
                }

            }
        }
        html += '<input type="hidden" name="total_price" value="'+ ((products['t_price'] == undefined)?'0':products['t_price']) +'">';
        $(this.settings.cartFormProductClass).html(html);
    };

    this.setAddProduct = function(context)
    {
        this.addProduct(context);
    };

    this.setRemoveProduct = function(context)
    {

        var thisObj = this;
        var prod_del = this.getDataFields(context);

        $.post("/api/dec_product",
        {
            'p':prod_del[thisObj.data.id],
            'c':prod_del[thisObj.data.id_corrector],
            'csrfmiddlewaretoken':thisObj.csrftoken
        },
        function()
        {
            thisObj.getPreview(thisObj.getProducts());
        });
        return true;
    };
}