from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from api.models import Cheese

API_URL = "/api/"

class CheeseApiTests(TestCase):
    def create_payload(self, **overrides):
        payload = {
            "name": "Parmesan",
            "milk_type": "COW",
            "expiration_date": (date.today() + timedelta(days=365)).isoformat(),
            "price_eur_per_kg": 18.5,
            "country_of_origin": "IT",
        }
        payload.update(overrides)
        return payload


    def test_health_ok(self):
        resp = self.client.get(f"{API_URL}health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": 'Im alive'})

    def test_create_cheese_success(self):
        resp = self.client.post(API_URL+"create", data=self.create_payload(), content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Parmesan")
        self.assertEqual(data["milk_type"], "COW")
        self.assertEqual(data["country_of_origin"], "IT")
        self.assertEqual(Cheese.objects.count(), 1)

    def test_create_cheese_invalid_country(self):
        resp = self.client.post(API_URL+"create", data=self.create_payload(country_of_origin="Slovakia"), content_type="application/json")
        self.assertEqual(resp.status_code, 422)
        self.assertEqual(Cheese.objects.count(), 0)

    def test_list_cheeses(self):
        self.client.post(API_URL+"create", data=self.create_payload(name="Parmesan"), content_type="application/json")
        self.client.post(API_URL+"create", data=self.create_payload(name="Gouda", country_of_origin="NL"), content_type="application/json")
        resp = self.client.get(API_URL+"list")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_get_cheese_by_id(self):
        cid = self.client.post(API_URL+"create", data=self.create_payload(), content_type="application/json").json()["id"]
        resp = self.client.get(f"{API_URL}{cid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], cid)

    def test_get_cheese_not_found(self):
        resp = self.client.get(f"{API_URL}9999999999999")
        self.assertEqual(resp.status_code, 404)

    def test_put_cheese(self):
        cid = self.client.post(API_URL+"create", data=self.create_payload(), content_type="application/json").json()["id"]
        new_payload = self.create_payload(
            name="Grana Padano",
            expiration_date=(date.today() + timedelta(days=100)).isoformat(),
            price_eur_per_kg=21.0,
            country_of_origin="IT",
        )
        resp = self.client.put(f"{API_URL}{cid}", data=new_payload, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["name"], "Grana Padano")
        self.assertEqual(data["price_eur_per_kg"], 21.0)

    def test_patch_cheese(self):
        cid = self.client.post(API_URL+"create", data=self.create_payload(), content_type="application/json").json()["id"]
        resp = self.client.patch(f"{API_URL}{cid}", data={"price_eur_per_kg": 25.0}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["price_eur_per_kg"], 25.0)
        obj = Cheese.objects.get(id=cid)
        self.assertEqual(obj.name, "Parmesan")

    def test_delete_cheese(self):
        cid = self.client.post(API_URL+"create", data=self.create_payload(), content_type="application/json").json()["id"]
        resp = self.client.delete(f"{API_URL}{cid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"success": True})
        self.assertFalse(Cheese.objects.filter(id=cid).exists())

    def test_delete_cheese_not_found(self):
        resp = self.client.delete(f"{API_URL}999999998")
        self.assertEqual(resp.status_code, 404)
