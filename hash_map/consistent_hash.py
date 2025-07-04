import hashlib

class ConsistentHashMap:
    def __init__(self, num_slots=512, num_servers=3, virtual_servers=9):
        """
        Initialize consistent hash map.
        :param num_slots: Number of slots in the hash ring.
        :param num_servers: Initial number of physical servers.
        :param virtual_servers: Number of virtual servers per physical server.
        """
        self.num_slots = num_slots
        self.virtual_servers = virtual_servers
        self.ring = {}  # Maps slot to server name
        self.servers = {}  # Maps server name to server_id
        # Initialize with given number of servers
        for server_id in range(1, num_servers + 1):
            self.add_server(f"Server{server_id}", server_id)

    def _hash(self, key):
        """
        Hash a key to a slot in the ring.
        :param key: String or integer to hash.
        :return: Slot number.
        """
        # Use MD5 for better distribution
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server_name, server_id):
        """
        Add a server and its virtual servers to the hash ring.
        :param server_name: Name of the server (e.g., Server1).
        :param server_id: Unique server identifier.
        """
        self.servers[server_name] = server_id
        for i in range(self.virtual_servers):
            slot = self._hash(f"{server_name}:{i}")
            self.ring[slot] = server_name

    def remove_server(self, server_name):
        """
        Remove a server and its virtual servers from the hash ring.
        :param server_name: Name of the server to remove.
        """
        if server_name in self.servers:
            del self.servers[server_name]
            # Remove all virtual servers for this server
            slots_to_remove = [slot for slot, name in self.ring.items() if name == server_name]
            for slot in slots_to_remove:
                del self.ring[slot]

    def get_server(self, request_id):
        """
        Get the server for a given request ID.
        :param request_id: Integer request ID.
        :return: Server name or None if no servers available.
        """
        if not self.ring:
            return None
        slot = self._hash(request_id)
        # Find the closest slot (clockwise)
        sorted_slots = sorted(self.ring.keys())
        for s in sorted_slots:
            if slot <= s:
                return self.ring[s]
        # Wrap around to the first slot
        return self.ring[sorted_slots[0]]