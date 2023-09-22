import xml.etree.ElementTree as ET
import json
import re


class OvalToJsonConverter():
    def __init__(self) -> None:
        self.json_dict = {'oval_definitions': {}}
        self.root_node = None
        self.namespace = {
            'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5'
        }
        self.refs={
            'test_ref': [],
            'object_ref': [],
            'state_ref': [],
        }

    def convert(self, filepath) -> None:
        self.root_node = ET.parse(filepath).getroot()
        self.json_dict['oval_definitions']['definitions'] = self.parse_definitions(count=3) #первые 3 определения
        self.json_dict['oval_definitions']['tests'] = self.parse_items('test_ref')
        self.json_dict['oval_definitions']['objects'] = self.parse_items('object_ref')
        self.json_dict['oval_definitions']['states'] = self.parse_items('state_ref')

        with open(filepath.replace('.xml', '.json'), 'w') as file:
            json.dump(self.json_dict, file)

    # метод возвращает список с dict-объектами определений (definition)
    def parse_definitions(self, count) -> list:
    # берем первые "count" определений
        definition_list = []
        for definition in self.root_node.findall('.//oval:definition', self.namespace):
            definition_list.append(definition)
            if len(definition_list) == count:
                break
        result = []
        for definition in definition_list:
            result.append({"definition": self.parse_element(definition)})
        return result
    
    # метод для парсинга test, object, state (объекты на которые есть ссылки)
    def parse_items(self, ref_type) -> list:
        result_items_list = []
        for item in self.searching_for_an_item_by_id(self.refs[ref_type]):
            result_items_list.append({ref_type[:-4]: self.parse_element(item)})
        return result_items_list

    # функция рекурсивно переводит все содержимое тега в dict-объект python
    def parse_element(self, element) -> dict:
        element_data = {}
        for key, value in element.attrib.items():
            element_data[f'@{key}'] = value
            # сохранение ссылок на объекты в отдельных списках для дальнейшей работы с ними
            if (f'@{key}' == '@test_ref' or  f'@{key}' == '@object_ref' or f'@{key}' == '@state_ref'):
                self.refs[key].append(value)
            
        element_text = element.text
        if element_text and element_text.rstrip():
            element_data['text'] = element_text

        for child in element:
            # удаляем некрасивую подпись пространства имен
            child_tag= re.sub(r'\{http[^}]*\}', "", child.tag)
            if child_tag in element_data:
                # если элемент с таким тегом уже есть в данных, превращаем его в список, если это ещё не сделано \
                # нужно, чтобы не исчезли элементы с одинаковыми ключами (например критерии)
                if not isinstance(element_data[child_tag], list):
                    element_data[child_tag] = [element_data[child_tag]]
                
                # рекурсивный вызов для вложенных элементов
                element_data[child_tag].append(self.parse_element(child))
            else:
                element_data[child_tag] = self.parse_element(child)
        return element_data
    
    # поиск элементов с id, которые входят в переданный список
    def searching_for_an_item_by_id(self, id_list) -> list:
        # удаление дубликатов
        id_list = list(set(id_list))
        item_list = []
        for id in id_list:
            for element in self.root_node.iter():
                if 'id' in element.attrib and element.attrib['id'] == id:
                    # найден элемент с нужным id
                    item_list.append(element)
                    break
        return item_list
    










