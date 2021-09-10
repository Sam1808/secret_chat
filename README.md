# Подключаемся к подпольному чату

## Программа, чтобы через командную строку таскать для *бабы Зины* коды.

### Как развернуть утилиту для *бабы Зины*:

Делаем всё под python 3.7 и выше.

1. Скачайте код:
```shell
git clone https://github.com/Sam1808/secret_chat.git
```
2. Разверните [виртуальное окружение](https://devman.org/encyclopedia/pip/pip_virtualenv/) и зависимости:  
```shell
pip install -r requirements.txt
```
3. Создайте конфигурационный файл `config.yaml` со следующим содержимым (он нам пригодится только для отправки сообщений):

```yaml
#config.yaml
# URL подпольного чата 
chat_url: minechat.dvmn.org
# Порт для отправки сообщений в тот самый подпольный чат
send_port: 0000
# Токен пользователя, если он у вас есть
token:
# Включить отладку? (пустое значение - False)
debug:
# Зарегистрировать ли нового пользователя? (пустое значение - нет)
new_user:
# Указать свое имя пользователя в чате
name:
```

*Аргументов на самом деле больше, включая и имя конфигурационного файла. Их много, но всё-таки не достаточно,
чтобы делать отдельные конфигурации для отправки сообщений и их получения. Итак, подробнее...*

### Как *бабе Зине* запустить скрипт для чтения чата:

- вся конфигурация по умолчанию уже описана в файле `receive.py`, поэтому достаточно запустить:  
```python
python3 receive.py
```
- если конфигурацию надо поправить, то сначала надо ознакомиться с аргументами:  
```python
python3 receive.py --help
```
- пример детализации аргументов:   
```python
python3 receive.py --url new.secret.url --receive_port 9999 --history new_file.txt
```

### Что увидит *баба Зина*:

- всю переписку в консоли
- всю историю переписки, с момента запуска скрипта, в файле истории

### Как *бабе Зине* запустить скрипт для отправки сообщения в чат:

Отправка сообщений с помощью скрипта `send.py`. Отправка чуть сложнее, чем прием, тут появляется
обязательный аргумент командной строки `--message` (иначе, что вы собрались отправлять?), и 
все аргументы описанные в `config.yaml`. Итак...  
- список всех аргументов, традиционно:
```python
python3 send.py --help
```
- если вы отправляете сообщение впервые и у вас нет никаких регистрационных данных, скрипт
автоматически все сделает за вас и сохранит чуствительные данные в `register_info.txt`:
```python
python3 send.py --message 'Hello my friends!'
```
- далее скрипт всегда будет отправлять данные от имени зарегистированного пользователя, пока вы 
не удалите `register_info.txt` или явно не укажите `token` другого пользователя, например:  
```python
python3 send.py --message 'Hello my friends!' --token 11223344ldfssdfsdfsd
```
- если имя пользоватея вам надоело, перерегистрируйтесь:  
```python
python3 send.py --message 'Hello my friends!' --new_user=True
```
- если хотите подробно видеть в консоли все происходящее, включите DEBUG:  
```python
python3 send.py --message 'Hello my friends!' --debug=True
```
- а ещё можно явно зарегистировать свое имя пользователя, хотя в чате оно будет не особо явное. 
Не забудьте удалить старые регистрационные данные (файл `register_info.txt`) перед регистрацией такого пользователя. 
Считаете, что это достойно автоматизации? Скажите об этом!
```python
python3 send.py --message 'Hello my friends!' --name Zina_super_baba
```

Почти все указанные опции можно прописать на постоянной основе в `config.yaml`, 
и даже `message`, как бы глупо это не казалось.
### Ошибки:

- скрипт отправки сообщений будет отказываться запускаться, пока вы не создадите файл конфигурации;
- скрипт косо посмотрит на вас, если при отправке нет `--message`;
- скрипт не ломается, если символы переноса строки `\n` попали в имя пользователя или в текст сообщения.
