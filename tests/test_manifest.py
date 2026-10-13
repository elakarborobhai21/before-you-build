import json
import unittest

from tests.helpers import frontmatter, read

REPO_URL = "https://github.com/elakarborobhai21/before-you-build"


class ManifestTests(unittest.TestCase):
    def test_plugin_json_fields(self):
        data = json.loads(read(".claude-plugin/plugin.json"))
        self.assertEqual(data["name"], "before-you-build")
        self.assertEqual(data["version"], "0.1.0")
        self.assertEqual(data["license"], "MIT")
        self.assertEqual(data["repository"], REPO_URL)
        self.assertTrue(data["description"].strip())

    def test_marketplace_lists_plugin(self):
        data = json.loads(read(".claude-plugin/marketplace.json"))
        self.assertEqual(data["name"], "before-you-build")
        self.assertTrue(data["owner"]["name"].strip())
        self.assertEqual(data["plugins"][0]["name"], "before-you-build")
        self.assertEqual(data["plugins"][0]["source"], "./")

    def test_license_is_mit(self):
        text = read("LICENSE")
        self.assertTrue(text.startswith("MIT License"))
        self.assertIn("Copyright (c) 2026 Yaseer Ahsan", text)

    def test_frontmatter_helper(self):
        self.assertEqual(
            frontmatter("---\nname: x\ndescription: y\n---\nbody"),
            {"name": "x", "description": "y"},
        )
        with self.assertRaises(ValueError):
            frontmatter("no block")


if __name__ == "__main__":
    unittest.main()
