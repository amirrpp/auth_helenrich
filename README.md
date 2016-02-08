# auth_helenrich

Что сделано:
- добавленны страницы:
  - Вход/Регистрация с формами для входа и регистрации, поля проверяются на корректность введенных данных
  - Профиль, где можно изменить свои данные, выйти
- добавленна кнопка Регистрация/Логин в header, после входа она меняется на Здравствуйте, [имя пользователя]
- написаны тесты для вышеназванного
- т.к. главное меню присутствует на каждой странице, то main_menu вынесен в context_processors

Другие мысли:
Немного посмотрел другие приложения. У вас используются сырые запросы к БД, которые можно заменить для использования только ORM django, например:

```
    wshm.ProductParameterValue.objects.raw(
        str.format('SELECT prod_vals.id \
        FROM product_parameters_values as prod_vals \
        LEFT JOIN product_parameters_available_value as val ON val.id=prod_vals.value_id \
        JOIN product_parameters as prod_param ON prod_vals.product_parameter_id=prod_param.id \
        WHERE CAST (val.value AS {1}) >= {0}) \
        OR \
        CAST(prod_vals.custom_value AS {1}) >= {0})', from_value, sort_as))
```

можно заменить на

```
    wshm.ProductParameterValue.objects.filter(Q(custom_value__gte=10) | Q(value__value__gte=10)).values_list('id', flat=True)
```

итоговый запрос к базе получается

```
    SELECT "product_parameters_values"."id" 
      FROM "product_parameters_values" 
      LEFT OUTER JOIN "product_parameters_available_value" ON 
      ( "product_parameters_values"."value_id" = "product_parameters_available_value"."id" ) 
      WHERE ("product_parameters_values"."custom_value" >= 10 
      OR 
      "product_parameters_available_value"."value" >= 10)
```
т.е. эквивалентен начальному (нет `JOIN product_parameters as prod_param ON prod_vals.product_parameter_id=prod_param.id`, но он нигде и не используется)
