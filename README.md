Выполнение задачи для компании Ришат.

Код также содержится в docker-контейнере greytres/payments:v5

для того, чтобы развернуть приложение, необходимо запустить docker-compose.yaml, выполнив команду docker-compose up: будут сформированы необходимые контейнеры.

затем необходимо выполнить миграции командами docker-compose exec web python3 manage.py makemigrations docker-compose exec web python3 manage.py migrate --run-syncdb

для создания суперпользователя используйте docker-compose exec web python manage.py createsuperuser

подтянуть статику можно командой docker-compose exec web python3 manage.py collectstatic --no-input

создание элементов предполагается по следующим поинтам:
localhost/create_price/ - для создания цены
localhost/create_coupon/  - для создания купона на скидку
localhost/create_tax/ - для создания налога

localhost/order/ - для объединения нескольких товаров в общий заказ

localhost/item/<id>/ - страница товара, с которой его можно купить