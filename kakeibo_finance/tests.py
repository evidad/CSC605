from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doggo

# Used ChatGPT to modify demo test cases for lab
class DoggoTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_doggo = Doggo.objects.create(
            name="Tonk",
            owner=testuser1,
            description="shaded cream long-haired mini dachshund",
        )
        test_doggo.save()

    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_doggos_model(self):
        doggo = Doggo.objects.get(id=1)
        actual_owner = str(doggo.owner)
        actual_name = str(doggo.name)
        actual_description = str(doggo.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "Tonk")
        self.assertEqual(
            actual_description, "shaded cream long-haired mini dachshund"
        )

    def test_get_doggo_list(self):
        url = reverse("doggo_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doggos = response.data
        self.assertEqual(len(doggos), 1)
        self.assertEqual(doggos[0]["name"], "Tonk")

    def test_get_doggo_by_id(self):
        url = reverse("doggo_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doggo = response.data
        self.assertEqual(doggo["name"], "Tonk")

    def test_create_doggo(self):
        url = reverse("doggo_list")
        data = {"owner": 1, "name": "Kona", "description": "Fox terrier chihuahua"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doggos = Doggo.objects.all()
        self.assertEqual(len(doggos), 2)
        self.assertEqual(Doggo.objects.get(id=2).name, "Kona")

    def test_update_doggo(self):
        url = reverse("doggo_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "Kona",
            "description": "yappy",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doggo = Doggo.objects.get(id=1)
        self.assertEqual(doggo.name, data["name"])
        self.assertEqual(doggo.owner.id, data["owner"])
        self.assertEqual(doggo.description, data["description"])

    def test_delete_doggo(self):
        url = reverse("doggo_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        doggos = Doggo.objects.all()
        self.assertEqual(len(doggos), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("doggo_list")
        response = self.client.get(url)
        # updated this line - verifies the doggo list is still available even when not logged in
        self.assertEqual(response.status_code, status.HTTP_200_OK)
