$(function(){
    var settings = {
        mainClass: '.product-add_to_cart',
        actionClass: '.add-to-cart',
        saveHour: 3,
        cartPreviewClass: '.web_shop_cart-preview',
        cartTotalPriceClass: '.web_shop_cart-total_price',
        cartTotalCountClass: '.web_shop_cart-total_count',
        cartClearClass: '.web_shop_cart-clear_all',
        cartFormProductClass: '.web_shop_cart-product_hidden_field',
        cartFormOrderClass: '.web_shop_cart-form_order',
        priceCorrectorCheckInput: '.product-price_corrector input[type="radio"]',
        priceCorrectorCheckClass: '.product-price_corrector',
        priceCorrectorPrintClass: '.product-price_corrector_print',
        productDeleteClass: '.product_delete',
        productAddItemClass: '.product_count-add_cart',
        productRemoveItemClass: '.product_count-remove_cart',
        buttonValueDefault: 'В корзину',
        buttonValueAdded: 'Добавить',
        buttonCountClass: '.button-lable_count'
    };

    var data_fields = {
        id: 'p',
        id_corrector: 'c',
        price: 'price',
        count: 'count'
    };

    var WebShopCart = new CartObject(settings, data_fields);

    WebShopCart.init();

    if($(WebShopCart.settings.actionClass).length > 0) {
        $(WebShopCart.settings.actionClass).click(function () {
            WebShopCart.addProduct(this);
        });
    }

    if($(WebShopCart.settings.priceCorrectorCheckClass).length > 0) {
        $(WebShopCart.settings.priceCorrectorCheckInput).click(function () {
            WebShopCart.setPriceCorrector(this);
        });
        for(var i=0; i<$(WebShopCart.settings.priceCorrectorCheckClass).length; i++)
        {
            $(WebShopCart.settings.priceCorrectorCheckClass).eq(i).find('input[type="radio"]').first().click();
        }
    }

    if($(WebShopCart.settings.cartClearClass).length > 0) {
        $(WebShopCart.settings.cartClearClass).click(function () {
            WebShopCart.clearCart();
        });
    }

    if($(WebShopCart.settings.cartFormOrderClass).length > 0) {
        WebShopCart.renderOrderForm();
    }

    if($(WebShopCart.settings.cartFormOrderClass).length > 0) {
        $(WebShopCart.settings.cartFormOrderClass).submit(function () {
            WebShopCart.clearCart();
        });
    }
});