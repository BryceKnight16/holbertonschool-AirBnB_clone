#!/usr/bin/python3
import unittest
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.obj1 = BaseModel(
            id='123',
            name='test1',
            my_number=42,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        self.obj2 = BaseModel(
            id='456',
            name='test2',
            my_number=24,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        self.storage.new(self.obj1)
        self.storage.new(self.obj2)
        self.storage.save()
        self.storage.reload()
        self.objects = self.storage.all()

    def tearDown(self):
        # Clean up the file.json after each test
        with open(self.storage._FileStorage__file_path, 'w') as file:
            file.write("")

    def test_all_objects_present_when_objects_added(self):
        # Test if all objects are present when objects are added
        objects = self.objects
        expected_keys = [f"BaseModel.{self.obj1.id}", f"BaseModel.{self.obj2.id}"]
        for key in expected_keys:
            self.assertIn(key, objects)


    def test_new_adds_objects_to_storage(self):
        # Test new() method adds objects to storage
        objects = self.objects
        self.assertIn(f"BaseModel.{self.obj1.id}", objects)
        self.assertIn(f"BaseModel.{self.obj2.id}", objects)

    def test_save_serializes_objects_to_file(self):
        # Test save() method serializes objects to the JSON file
        self.storage.save()
        with open(self.storage._FileStorage__file_path, 'r') as file:
            data = json.load(file)
        objects = self.objects
        self.assertIn(f"BaseModel.{self.obj1.id}", data)
        self.assertIn(f"BaseModel.{self.obj2.id}", data)

    def test_reload_deserializes_file_to_objects(self):
        # Test reload() method deserializes file to objects
        self.storage.reload()
        objects = self.objects
        self.assertIn(f"BaseModel.{self.obj1.id}", objects)
        self.assertIn(f"BaseModel.{self.obj2.id}", objects)



    def test_reload(self):
        initial_objects = self.objects
        self.obj1.name = 'modified_test1'
        self.obj1.save()
        self.obj2.name = 'modified_test2'
        self.obj2.save()
        self.storage.reload()
        reloaded_objects = self.storage.all()
        for key in initial_objects:
            self.assertEqual(reloaded_objects.get(key).to_dict(), initial_objects.get(key).to_dict())
