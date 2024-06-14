import jsonschema
import unittest
from fastapi.testclient import TestClient
from app.main import start_application

person_json_schema = {
            "type": "object",
            "properties": {
                "status_code": {"type": "integer"},
                "status": {"type": "string"},
                "message": {"type": "string"},
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "gender": {"type": "string"},
                            "photo_url": {"type": "string"}
                        },
                        "required": ["id", "first_name", "last_name", "gender", "photo_url"]
                    }
                }
            },
            "required": ["status_code", "status", "message", "data"]
        }

class TestPersonsAPI(unittest.TestCase):
    def setUp(self):
        # Configurar la aplicación para pruebas
        self.app = TestClient(start_application())

    def validate_response(self, response, schema):
        try:
            jsonschema.validate(response.json(), schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(f"La respuesta no cumple con la definición de la API: {e}")

    def test_get_all_persons(self):
        response = self.app.get('/persons/')
        self.assertEqual(response.status_code, 200)
        self.validate_response(response, person_json_schema)

    def test_get_person_by_id(self):
        # Prueba un ID válido
        response = self.app.get('/persons/1')
        self.assertEqual(response.status_code, 200)

        # Prueba un ID inválido
        response = self.app.get('/persons/invalid_id')
        self.assertEqual(response.status_code, 400)

    def test_add_person(self):
        # Prueba agregar una persona con datos válidos
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "male",
            "photo_url": "http://example.com/photo.jpg"
        }
        response = self.app.post('/persons/', json=data)
        self.assertEqual(response.status_code, 200)

        # Prueba agregar una persona con datos inválidos
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            # Faltan campos requeridos
        }
        response = self.app.post('/persons/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_update_person_by_id(self):
        # Prueba actualizar una persona con datos válidos
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "male",
            "photo_url": "http://example.com/photo.jpg"
        }
        response = self.app.put('/persons/1', json=data)
        self.assertEqual(response.status_code, 200)

        # Prueba actualizar una persona con datos inválidos
        invalid_data = {
            "first_name": "John",
            "last_name": "Doe",
            # Faltan campos requeridos
        }
        response = self.app.put('/persons/1', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_delete_person_by_id(self):
        # Prueba eliminar una persona con ID válido
        response = self.app.delete('/persons/1')
        self.assertEqual(response.status_code, 200)

        # Prueba eliminar una persona con ID inválido
        response = self.app.delete('/persons/invalid_id')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
