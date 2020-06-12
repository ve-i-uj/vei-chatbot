# A chat bot

Тестовая задача

	Необходимо написать небольшого чат-бота использую стейт-машину
	Требования
	1.	Бот должен поддерживать работу только с телеграммом - но вы должны учесть возможность подключения другого средства коммуникации (фб, вк, скайп)
	2.	Бот должен обрабатывать следующий диалог
		1.	Какую вы хотите пиццу?  Большую или маленькую?
		2.	Большую
		3.	Как вы будете платить?
		4.	Наличкой
		5.	Вы хотите большую пиццу, оплата - наличкой?
		6.	Да
		7.	Спасибо за заказ
	3.	Для стейт машины использовать https://github.com/pytransitions/transitions
	4.	Добавить тесты для диалога
	5.	Выложить бота на хероку и подключить его к телеграмму 
	6.	Код выложить на гитхаб или хероку
	7.	Максимальный срок выполнения - 2 дня


### Локальная разработка

Задача выполнена на Python2.7

Создаём виртуальное окружение

```
# Linux
PROJECT_DIR=<YOUR_PROJECT_DIR>
cd $PROJECT_DIR
mkdir .pyvenv
python2.7 -m pip install virtualenv
python2.7 -m virtualenv .pyvenv
source .pyvenv/bin/activate
pip install --requirement ./requirements.txt

# Windows
PROJECT_DIR=<YOUR_PROJECT_DIR>
cd $PROJECT_DIR
python2.7 -m pip install virtualenv
python2.7 -m virtualenv .pyvenv
.pyvenv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;<YOUR_PROJECT_DIR>
# например, set PYTHONPATH=%PYTHONPATH%;C:\Users\burov\Documents\pC\vei-chatbot
```

### Запуск

```

python chatbot/main.py --ui=cli

```