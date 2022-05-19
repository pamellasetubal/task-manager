from fastapi import status
from fastapi.testclient import TestClient

from task_manager.manager import TASKS, app

tasks = "/tasks"
application_json = "application/json"
content_type = "Content-Type"


def test_when_list_task_should_receive_200_status_code():
    client = TestClient(app)
    response = client.get(tasks)
    assert response.status_code == status.HTTP_200_OK


def test_when_list_task_the_format_should_return_json():
    client = TestClient(app)
    response = client.get(tasks)
    assert response.headers[content_type] == application_json


def test_when_list_task_the_return_should_be_a_list():
    client = TestClient(app)
    response = client.get(tasks)
    assert isinstance(response.json(), list)


def test_when_list_tasks_the_task_should_return_an_id():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "ended",
        }
    )
    client = TestClient(app)
    response = client.get(tasks)
    assert "id" in response.json().pop()
    TASKS.clear()


def test_when_list_tasks_the_task_should_return_a_title():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "ended",
        }
    )
    client = TestClient(app)
    response = client.get(tasks)
    assert "title" in response.json().pop()
    TASKS.clear()


def test_when_list_tasks_the_task_should_return_a_description():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "ended",
        }
    )
    client = TestClient(app)
    response = client.get(tasks)
    assert "description" in response.json().pop()
    TASKS.clear()


def test_when_list_tasks_the_task_should_return_a_status():
    TASKS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "title 1",
            "description": "description 1",
            "status": "ended",
        }
    )
    client = TestClient(app)
    response = client.get(tasks)
    assert "status" in response.json().pop()
    TASKS.clear()


def test_task_should_accept_post_method():
    client = TestClient(app)
    response = client.post(tasks)
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_when_a_task_has_no_title_should_return_422_status_code():
    client = TestClient(app)
    response = client.post(tasks, json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_title_should_contain_between_3_and_50_character():
    client = TestClient(app)
    response = client.post(tasks, json={"title": 2 * "*"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = client.post(tasks, json={"title": 51 * "*"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_task_should_have_a_description():
    client = TestClient(app)
    response = client.post(tasks, json={"description": "description1"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_description_should_contain_up_to_140_character():
    client = TestClient(app)
    response = client.post(tasks, json={"title": "title1", "description": "*" * 141})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_when_create_a_task_itself_should_be_returned():
    client = TestClient(app)
    task_expected = {"title": "title1", "description": "description1"}
    response = client.post(tasks, json=task_expected)
    task_created = response.json()
    assert task_created["title"] == task_expected["title"]
    assert task_created["description"] == task_expected["description"]
    TASKS.clear()


def test_when_create_task_its_id_should_be_unique():
    client = TestClient(app)
    task_one = {"title": "title1", "description": "description1"}
    task_two = {"title": "title2", "description": "description2"}
    response_one = client.post(tasks, json=task_one)
    response_two = client.post(tasks, json=task_two)
    assert response_one.json()["id"] != response_two.json()["id"]
    TASKS.clear()


def test_when_create_task_status_should_be_default_and_not_ended():
    client = TestClient(app)
    task = {"title": "title1", "description": "description1"}
    response = client.post(tasks, json=task)
    assert response.json()["status"] == "not ended"
    TASKS.clear()


def test_when_create_a_task_should_return_201_status_code():
    client = TestClient(app)
    task = {"title": "title2", "description": "description2"}
    response = client.post(tasks, json=task)
    assert response.status_code == status.HTTP_201_CREATED
    TASKS.clear()


def test_when_create_a_task_it_should_be_persisted():
    client = TestClient(app)
    task = {"title": "title3", "description": "description3"}
    client.post(tasks, json=task)
    assert len(TASKS) == 1
    TASKS.clear()
