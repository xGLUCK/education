import json

from api import PetFriends
from settings import valid_email, valid_password
import os
import random

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#----------Практикум-----------

def test_add_new_pet_simple_with_valid_data (name='Барбоскин', animal_type='двортерьер',
                                     age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert (status == 200), "статус не 200"
    assert (result['name'] == name), "Имя нового питомца не совпадает с введенным"

def test_set_photo_with_valid_data_with_duplicate_check (pet_photo='images/P1040103.jpg'):
    """добавление фото к последнему добавленному питомцу с корректными данными"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и добавляем фото
    pet_id = my_pets['pets'][0]['id']
    old_photo = my_pets['pets'][0]['pet_photo']
    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, что статус 200, фото не отсутствует и фото обновилось
    assert (status == 200), "статус не 200"
    assert (my_pets['pets'][0]['pet_photo'] != ""), "Фото не добавлено"
    assert (my_pets['pets'][0]['pet_photo'] != old_photo), "Фото совпадает со старым. Либо не загрузилось новое, либо новое действительно совпадает со старым"

def test_set_photo_with_valid_data_without_duplicate_check (pet_photo='images/P1040103.jpg'):
    """добавление фото к последнему добавленному питомцу с корректными данными"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и добавляем фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, что статус 200, фото не отсутствует и фото обновилось
    assert (status == 200), "статус не 200"
    assert (my_pets['pets'][0]['pet_photo'] != ""), "Фото не добавлено"

def test_get_api_key_for_invalid_user():
    """ Проверяем что запрос api ключа возвращает статус 403 и в тезультате не содержится слово key"""
    rnd = random
    email = str(rnd.randint(1000000000000,9000000000000)) + '@kom.kom'
    password = str(rnd.randint(100000,9000000))
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert not ('key' in result)

def test_update_foreign_pet_info():
    #пытаемся поменять данные у чужого питомца

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список питомцев пустой, то просим добавить нового, иначе тест некорректен
    assert (len(all_pets['pets']) != 0),"Питомцев нет. добавьте нового с другого аккаунта"

    # Берём id первого питомца из списка и пытаемся поменять данные
    pet_id = all_pets['pets'][0]['id']
    name = 'ПытаемсяПоменять'
    animal_type = 'ЧужиеДанные'
    age = 20
    status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    #Повтоно запрашиваем питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    #Проверка статуса http запроса и проверка самих данных
    assert (status != 200), "Сервером был принят запрос на изменение данных чужого питомца"
    unacceptable_conditions = (all_pets['pets'][0]['name'] == 'ПытаемсяПоменять')or(all_pets['pets'][0]['animal_type']=='ЧужиеДанные')
    #Если id успел поменятся - не проверяем. Для тестов на высоконагруженном проекте могут успеть загрузить другие карточки.
    assert (all_pets['pets'][0]['id'] == pet_id and unacceptable_conditions), "Данные изменены пользователем, у которого не должно быть таких прав"

def test_successful_delete_foreign_pet():
    #Пытаемся удалить чужого питомца

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список питомцев пустой, то просим добавить нового, иначе тест некорректен
    assert (len(all_pets['pets']) != 0),"Питомцев нет. добавьте нового с другого аккаунта"

    # Берём id первого питомца из списка и пытаемся удалить его
    pet_id = all_pets['pets'][5]['id'] # удаляет шестого питомца, чтоб не сильно мешать другим
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Повтоно запрашиваем питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert (status != 200), "Сервером был принят запрос на удаление чужого питомца"
    assert (pet_id in all_pets.values()), "Чужой питомец был удален пользователем, у которого не должно быть таких прав"

def test_set_photo_with_invalid_data(pet_photo='images/P1040103.jpg'):
    """добавление фото к последнему добавленному питомцу с Некорректными данными"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Если фото было - удаляем всю карточку и заводим новую. Данные те-же, но без фото
    if my_pets['pets'][0]['pet_photo'] != "":
        buf_name = my_pets['pets'][0]['name']
        buf_type = my_pets['pets'][0]['animal_type']
        buf_age = my_pets['pets'][0]['age']
        pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        pf.add_new_pet_simple(auth_key, buf_name, buf_type, buf_age)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #убираем api key
    auth_key.pop('key')
    auth_key.update({'key': ''})

    # Берём id первого питомца из списка и добавляем фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, что статус 200, фото не отсутствует и фото обновилось
    assert (status != 200), "статус 200 при отсутвии API KEY в запросе"

    if my_pets != str: #PetFriends.get_list_of_pets возвращает str, если не получается вернуть json
        assert (my_pets['pets'][0]['pet_photo'] != ""), "Фото добавлено пользователем, у которого не должно быть таких прав"

def test_add_new_pet_simple_without_apikey():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #убираем api key
    auth_key.pop('key')
    auth_key.update({'key': ''})

    status, result = pf.add_new_pet_simple(auth_key, 'тестовый', 'питомец', '5')
    assert (status != 200), "статус 200. Запрос был без api key."

def test_add_new_pet_simple_with_big_age (name='Барбоскин', animal_type='двортерьер',
                                     age='9999999'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert (status == 200), "статус не 200"
    assert (int(result['age']) > 999 ), "Возраст противоречит здравому смыслу и законам природы"

def test_add_new_pet_simple_with_big_age (name='Барбоскин', animal_type='двортерьер',
                                     age='-20'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert (status == 200), "статус не 200"
    assert (int(result['age']) < 0 ), "Отрицательный возраст"
