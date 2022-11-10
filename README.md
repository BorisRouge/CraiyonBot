Бот для взаимодействия с Craiyon.com
===============================

Работающий образец можно пощупать здесь: https://t.me/FedInfoBot


### Порядок запуска

* Собран на Ubuntu 22.04 LTS.
* Подразумеваются установленные Python и Postgresql, наличие API-ключей Telegram, Yandex.Translate.

1. Внести учетные данные (телеграм, переводчик, постгрес) в тестовый файл окружения sample.env
2. 
```shell 
pip install -r requirements.txt
```
3. 
```shell 
python start.py
```
