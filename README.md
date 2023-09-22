# RVisionTest

Ручной частичный анализ OVAL-файла.

1. Был проведен анализ первых трех уязвимостей (патчей) в OVAL-файле. 
На мой взгляд, основными объектами, из которых состоит отдельная уязвимость являются:
 	а) Определения (definition)
	б) Критерии (сriteria)
	в) Тесты (test)
	г) Объекты (object)
	д) Состояния (state)
	е) Переменные (variables), но в нашем случае мы с ними не встречаемся

Также есть различные вспомогательные теги, которые помогают сделать код более читаемым и более точно описать те или иные объекты.

Для удобства, одна отдельная уязвимость была вынесена в файл "separate_patch_example.xml". 

2.
	a) Definition - основная часть OVAL-файла, которая говорит о чем-то важном, что система должна проверить на компьютере. В нашем случае Definition класса Patch (есть и другие), это значит, что в нем описаны патчи и обновления, которые можно применить к системе для устранения уязвимостей или улучшения безопасности.
	б) Criteria - критерии указывают на условия, при выполнении которых, данный патч должен быть применен к системе. К ним можно применять конструкции AND и OR. Они имеют описание и в них бывает ссылка на соответствующий тест.
	в) Test - тесты указывают на конкретные проверки или тесты, которые должны быть выполнены на целевой системе, чтобы удостовериться, что патч (обновление) было успешно применено или должно быть применено. Объект теста обычно имеет ссылки на объекты Object и State.
	г) Object - объекты используются для определения конкретных объектов, которые подлежат проверке или на которых должен быть применен патч. Объектом может быть программа, версия программы файл, путь и тд и тп.
	д) State - описывает ожидаемое состояние системы или объекта после применения патча. Нужен, чтобы понимать успешно применен патч или нет.

3. 
	Первая уязвимость:
		- так же как 3-я.
	Вторая уязвимость:
		- так же как 3-я.
	Третья уязвимость: 
		- тут интереснее. Так как в определении третьей уязвимости в теге \<platform> уже указана версия ОС, можно удалить из критериев проверки на версию ОС. То есть:
	
  	1) \<criterion comment="Red Hat Enterprise Linux must be installed" test_ref="oval:com.redhat.rhba:tst:20191992005"/>
  	2) \<criterion comment="Red Hat Enterprise Linux 8 is installed" test_ref="oval:com.redhat.rhba:tst:20191992003"/>
  	3) \<criterion comment="Red Hat CoreOS 4 is installed" test_ref="oval:com.redhat.rhba:tst:20191992004"/>

Напомню, что в определении 3-й уязвимости в теге \<platform> указано значение "Red Hat Enterprise Linux 8"

Критерий под номером 3) вообще противоречит тегу platform, его однозначно нужно исключить. Критерий под номером 1) тоже не совсем верный, т.к. не указывает на определенную версию ОС а, т.к. он находится внутри конструкции OR, то его значение True сделает бесполезными следующие проверки, общий результат будет True, а это противоречит тегу Platform, ведь сработает при любой версии ОС. Критерий 2) можно, в принципе, оставить. Это поможет установить более строгое соответствие ОС.

Остальные критерии: 
	в первом описании проверяют определенную версию cloud-init и подпись ключом.
	во втором описании проверяют включен ли модуль и определенные версии составных частей ruby 
	в третьем описании проверяют определенные версии составных частей openjpeg2


4. Я считаю, что упростить формат для описания уязвимостей поможет использование JSON. Он более удобочитаемый, JSON легче создавать, обрабатывать, он более гибкий и является основным форматом передачи данных по сети. Да и визуальнее он более приятный, вложенность как будто поменьше.





	