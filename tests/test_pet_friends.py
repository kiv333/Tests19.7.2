from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password
import os
import pytest

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


@pytest.mark.negative
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    """ 1 Негативный тест с проверкой невалидных значений not_valid_email, not_valid_password. """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


@pytest.mark.negative
def test_get_all_pets_with_not_valid_filter_faild(filter='Собака'):
    """ 2 Негативный тест. Проверяем что запрос с невалидным значением filter возвращает 500 и не выдает значений.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список питомцев."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200


def test_add_new_pet_with_valid_data(name='семён', animal_type='белка',
                                     age='8', pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) (со строкой возвращает 500 ответ )

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_special_characters_data(name='!@#$%^&*_+', animal_type='!@#$%^&*_+', age='8', pet_photo='images/P1040103.jpg'):
    """3 Проверяем что можно добавить питомца с корректными данными спецсимволами в разделах name и animal_type """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

@pytest.mark.negative
def test_add_new_pet_with_not_valid_data_faild(name='семён', animal_type='белка',
                                     age='5', pet_photo='images/P1040103.jpg'):
    """4 Проверяем что можно добавить питомца с некорректными данными в раздел age """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age

def generate_string(n):
   return "x" * n

def test_add_new_pet_with_valid_2_data(name=generate_string(255),
                                       animal_type=generate_string(255) ,
                                     age='А', pet_photo='images/pephoto.jpg'):
    """5 с валидными данными в размере 255 символов в разделах animal_type и name """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['animal_type'] == animal_type
    assert result['name'] == name

@pytest.mark.negative
def test_add_new_pet_with_not_valid_data_faild(name='', animal_type='',
                                     age='', pet_photo='images/P1040103.jpg'):
    """6 Проверяем создание питомца с пустыми значениями в разделах name, animal_type,age """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == animal_type

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    """Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев"""
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/P1040103.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='', animal_type='Белк', age=6):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_with_valid_data(name='Джон', animal_type='медведь',
                                     age='8'):
    """Проверяем что можно добавить питомца (без фото) с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

@pytest.mark.negative
def test_add_new_pet_without_photo_with_valid_data_faild(name='', animal_type='',
                                     age=''):
    """7 Негативный тест.Проверяем создание питомца с пустыми значениями в разделах  animal_type,age (без фото)."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == animal_type

def test_post_change_pet_foto(pet_photo='images/cat1.jpg'):
    """Проверяем добавление нового фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового (БЕЗ ФОТО) и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Добавляем фото
    status, result = pf.post_change_pet_photo(auth_key, pet_id, pet_photo)
    print(result )
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] !=0

@pytest.mark.negative
def test_post_change_pet_foto_faild(pet_photo='images/1.txt'):
    """8 Негативный тест. Отправляем вместо фото текстовый файл"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового (БЕЗ ФОТО) и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Добавляем фото
    status, result = pf.post_change_pet_photo(auth_key, pet_id, pet_photo)
    print(result)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] !=0

@pytest.mark.negative
def test_add_photo_pet_not_photo(pet_photo='images/VrY.gif'):
    # Проверяем фото другого формата на добавления к существующему питомцу. Ожидаем ошибку 400
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets) > 0:
        status, result = pf.post_change_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 400
        assert pet_photo not in result

def test_successful_update_self_pet_info_numbers(name='54366', animal_type='754567', age=6):
    """10 Проверяем возможность обновления значений name, animal_type о питомце только цифрами"""

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

