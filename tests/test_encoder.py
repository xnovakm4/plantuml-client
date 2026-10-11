import unittest
from core.plantuml_encoder import encode_plantuml

class TestPlantUMLEncoder(unittest.TestCase):
    def test_encode_simple_uml(self):
        puml = "Bob -> Alice : hello"
        expected = "SyfFKj2rKt3CoKnELR1Io4ZDoSa700"
        
        encoded = encode_plantuml(puml)
        self.assertEqual(encoded, expected)

if __name__ == "__main__":
    unittest.main()
