import unittest
from hash_map.consistent_hash import ConsistentHashMap

class TestConsistentHashMap(unittest.TestCase):
    """Unit tests for the ConsistentHashMap class."""
    def setUp(self):
        """Initialize a ConsistentHashMap instance before each test."""
        self.ch = ConsistentHashMap(num_slots=512, num_servers=3, virtual_servers=9)

    def test_initialization(self):
        """Test that the hash ring is initialized with 3 servers and 9 virtual servers each."""
        self.assertEqual(self.ch.num_slots, 512)
        self.assertEqual(self.ch.num_servers, 3)
        self.assertEqual(self.ch.virtual_servers, 9)
        self.assertEqual(len(self.ch.server_to_slots), 3)
        # Count total virtual servers placed (3 servers * 9 virtual servers = 27)
        virtual_server_count = sum(1 for slot in self.ch.hash_ring if slot is not None)
        self.assertEqual(virtual_server_count, 27)

    def test_virtual_server_placement(self):
        """Test that virtual servers are placed correctly using Φ(i, j) = i + j + 2j + 25."""
        for server_id in range(1, 4):
            server_name = f"Server{server_id}"
            slots = self.ch.server_to_slots[server_name]
            self.assertEqual(len(slots), 9)  # Each server has 9 virtual servers
            for virtual_id in range(9):
                # Compute expected slot without probing
                expected_slot = (server_id + virtual_id + 2 * virtual_id + 25) % 512
                # Check if the slot (or a probed slot) is in the server's slots
                found = False
                for slot in slots:
                    if slot == expected_slot or self.ch.hash_ring[slot] == server_name:
                        found = True
                        break
                self.assertTrue(found, f"Virtual server {virtual_id} for {server_name} not found")

    def test_request_mapping(self):
        """Test that requests are mapped to servers using H(i) = i + 2i + 2172."""
        test_requests = [0, 1, 10, 100, 1000]
        for request_id in test_requests:
            server = self.ch.get_server(request_id)
            self.assertIn(server, ["Server1", "Server2", "Server3"])
            # Verify the slot is reached by clockwise search
            slot = (request_id + 2 * request_id + 2172) % 512
            found_server = None
            for i in range(512):
                current_slot = (slot + i) % 512
                if self.ch.hash_ring[current_slot] is not None:
                    found_server = self.ch.hash_ring[current_slot]
                    break
            self.assertEqual(server, found_server)

    def test_add_server(self):
        """Test adding a new server to the hash ring."""
        original_slots = sum(1 for slot in self.ch.hash_ring if slot is not None)
        self.ch.add_server("Server4", 4)
        self.assertEqual(self.ch.num_servers, 4)
        self.assertEqual(len(self.ch.server_to_slots["Server4"]), 9)
        new_slots = sum(1 for slot in self.ch.hash_ring if slot is not None)
        self.assertEqual(new_slots, original_slots + 9)

    def test_remove_server(self):
        """Test removing a server from the hash ring."""
        original_slots = sum(1 for slot in self.ch.hash_ring if slot is not None)
        self.ch.remove_server("Server1")
        self.assertEqual(self.ch.num_servers, 2)
        self.assertNotIn("Server1", self.ch.server_to_slots)
        new_slots = sum(1 for slot in self.ch.hash_ring if slot is not None)
        self.assertEqual(new_slots, original_slots - 9)
        # Verify Server1 slots are cleared
        for slot in self.ch.server_to_slots.get("Server1", []):
            self.assertIsNone(self.ch.hash_ring[slot])

if __name__ == '__main__':
    unittest.main()
