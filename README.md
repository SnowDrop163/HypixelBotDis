# Бот для верификации пользователей на Hypixel Skyblock.

### Основные возможности бота:

- Верификации пользователя с помощью Hypixel API
- Проверка наличия роли привилегии через Hypixel API
- Парсер[^1] на новости Hypixel
- Воспроизведение музыки[^2] с адекватным списком очереди

###  Верификации пользователя с помощью Hypixel API

Верификация происходит путем сравнения Discord username пользователя с тем, что указан в Hypixel API. При неуспешной верификации пользователю выведется ошибка, а при удачном прохождении верификации ник пользователя изменится на ник, который указан у него в игре и он получит роль верифицированного пользователя.
### Проверка наличия роли привилегии через Hypixel API
Сначала происходит все то же самое, что и в пункте верификации, после этого этапа бот узнает какой ранг куплен у пользователя, через Hypixel API, и выдает роль соответствующую его рангу.
### Воспроизведение музыки с адекватным списком очереди
Пока находится в активной разработке. После фикса багов напишу, что умеет.


## Планы для развития бота
### Создать базу данных
Пригодится для записи прогресса пользователей. Особенно актуально для создателей гильдии.
### Создать систему создания тикетов
В основном будет использоваться для кланов, которые делают керри.




[^1]: Временно скрыт, в скором времени открою доступ.
[^2]: Доступно в исходном коде, но требует доработки.

Начал писать бота в 1:00 ночи 23.02.2024. Все планы в ближайшее время будут выполнены.
