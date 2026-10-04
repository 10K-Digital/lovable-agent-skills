import json
import unittest
import os

class TestClaudeHooks(unittest.TestCase):
    def test_start_event_replaced(self):
        hooks_path = os.path.join('plugins', 'lovable', 'hooks', 'claude-hooks.json')
        with open(hooks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        hooks = data.get('hooks', {})
        # "Start" should not exist; "SessionStart" should exist
        self.assertNotIn('Start', hooks, "'Start' event still present in claude-hooks.json")
        self.assertIn('SessionStart', hooks, "'SessionStart' event missing in claude-hooks.json")

if __name__ == '__main__':
    unittest.main()
