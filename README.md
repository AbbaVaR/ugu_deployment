# Вариант 16. 
## Проект БАНКОМАТЫ

Банки предоставляют возможность своим клиентам осуществлять безналичные расчеты с
помощью эмитируемых ими пластиковых карт и обналичивать деньги в банкоматах.
Каждый банк обслуживает свои банкоматы и своих клиентов по вопросам эксплуатации
эмитируемых им пластиковых карт.
Если карточка клиента эмитирована банком, обслуживающим банкомат, то операция
выдачи наличных денег банкоматом клиенту осуществляется бесплатно. Если же клиент
некоторого банка обналичивает деньги в банкомате другого банка, то банкомат снимает
комиссию (1,2 % суммы выдачи).
Клиенты осуществляют операции обналичивания денег в любое время суток и в любом
банкомате.
Необходимо разработать приложение Банкоматы, которое будет использоваться для
анализа операций обналичивания денег клиентами в банкоматах разных банков, частоты
обслуживания банкоматами клиентов с взыманием комиссионных вознаграждений, динамики
операций обналичивания денег клиентами отдельных банков в разных банкоматах за
определенные интервалы времени и др.

### В БД должна храниться информация:

* о Банках: код банка, название банка, юридический адрес;
* Банкоматах: номер банкомата, адрес банкомата, код банка (обслуживающего
банкомат);
* Клиентах: номер карточки клиента, Ф.И.О. клиента, адрес клиента, код банка
(обслуживающего клиента);
* Операциях выдачи наличных денег клиентам: номер карточки клиента, номер
банкомата, дата, время, комиссия (Да/Нет), сумма выдачи (руб.)
При проектировании БД необходимо учитывать следующее:
* банк обслуживает несколько банкоматов. Банкомат обслуживается одним банком;
* банк обслуживает несколько клиентов. Клиент обслуживается одним банком;
* банкомат обслуживает несколько клиентов. Клиент обслуживается несколькими
банкоматами;
* банкомат осуществляет несколько операций обналичивания денег. Операция
обналичивания денег связана с одним банкоматом;
* клиент осуществляет несколько операций обналичивания денег. Операция
обналичивания денег связана с одним клиентом.

### Кроме того следует учесть:
* каждый банк обязательно имеет в обслуживании банкоматы. Каждый банкомат
обязательно обслуживается банком;
* каждый банк обязательно имеет клиентов. Каждый клиент обязательно обслуживается
банком;
* каждый банкомат обязательно обслуживает клиентов. Каждый клиент обязательно
обслуживается банкоматами;
* банкомат необязательно осуществляет постоянно операции выдачи наличных денег.
Каждая операция выдачи наличных денег обязательно связана с банкоматом;
* клиент необязательно осуществляет операции обналичивания денег. Каждая операция
обналичивания денег обязательно связана с клиентом.

docker:  
* docker build -t ugu_deployment .
* sudo docker run -d --name fastapi --rm  -p 7008:7000 ugu_deployment