class ConsistentHashMap:
    """
    Consistent Hash Map Implementation
    This module implements a consistent hash map that maps requests to servers using a hash ring.
    It supports adding and removing servers, and uses virtual servers to balance load.
    """
    def __init__(self, num_slots=512, num_servers=3, virtual_servers=9):
        """
        Initialize the consistent hash map.
        :param num_slots: Total number of slots in the hash ring (H_slots = 512).
        :param num_servers: Number of physical servers (N = 3).
        :param virtual_servers: Number of virtual servers per physical server (K = 9).
        """
        self.num_slots = num_slots
        self.num_servers = num_servers
        self.virtual_servers = virtual_servers
        # Initialize hash ring as an array of None (512 slots)
        self.hash_ring: list[str | None] = [None] * num_slots
        # Track server-to-virtual-server mappings for removal
        self.server_to_slots = {f"Server{i}": [] for i in range(1, num_servers + 1)}
        # Populate the hash ring with virtual servers
        self._populate_ring()

    def _virtual_server_hash(self, server_id, virtual_id):
        """
        Compute hash for a virtual server using Φ(i, j) = i + j + 2j + 25.
        :param server_id: Integer ID of the server (1-based).
        :param virtual_id: Integer ID of the virtual server (0 to K-1).
        :return: Hash value (slot index).
        """
        return (server_id + virtual_id + 2 * virtual_id + 25) % self.num_slots

    def _request_hash(self, request_id):
        """
        Compute hash for a request using H(i) = i + 2i + 2172.
        :param request_id: Integer ID of the request.
        :return: Hash value (slot index).
        """
        return (request_id + 2 * request_id + 2172) % self.num_slots

    def _populate_ring(self):
        """
        Populate the hash ring with virtual servers for each physical server.
        Uses linear probing to resolve slot conflicts.
        """
        for server_id in range(1, self.num_servers + 1):
            server_name = f"Server{server_id}"
            for virtual_id in range(self.virtual_servers):
                # Compute initial slot for the virtual server
                slot = self._virtual_server_hash(server_id, virtual_id)
                original_slot = slot
                # Linear probing to find an empty slot
                while self.hash_ring[slot] is not None:
                    slot = (slot + 1) % self.num_slots
                    if slot == original_slot:
                        raise Exception("Hash ring is full, cannot place virtual server")
                # Place the server in the slot
                self.hash_ring[slot] = server_name
                self.server_to_slots[server_name].append(slot)

    def add_server(self, server_name, server_id):
        """
        Add a new server with K virtual servers to the hash ring.
        :param server_name: Name of the server (e.g., 'Server4').
        :param server_id: Integer ID for the server.
        """
        self.num_servers += 1
        self.server_to_slots[server_name] = []
        for virtual_id in range(self.virtual_servers):
            slot = self._virtual_server_hash(server_id, virtual_id)
            original_slot = slot
            while self.hash_ring[slot] is not None:
                slot = (slot + 1) % self.num_slots
                if slot == original_slot:
                    raise Exception("Hash ring is full, cannot place virtual server")
            self.hash_ring[slot] = server_name
            self.server_to_slots[server_name].append(slot)

    def remove_server(self, server_name):
        """
        Remove a server and its virtual servers from the hash ring.
        :param server_name: Name of the server to remove (e.g., 'Server1').
        """
        if server_name in self.server_to_slots:
            for slot in self.server_to_slots[server_name]:
                self.hash_ring[slot] = None
            del self.server_to_slots[server_name]
            self.num_servers -= 1

    def get_server(self, request_id):
        """
        Map a request to a server by finding the nearest virtual server slot (clockwise).
        :param request_id: Integer ID of the request.
        :return: Name of the server handling the request.
        """
        if not self.server_to_slots:
            return None
        slot = self._request_hash(request_id)
        # Search clockwise for the next non-empty slot
        for i in range(self.num_slots):
            current_slot = (slot + i) % self.num_slots
            if self.hash_ring[current_slot] is not None:
                return self.hash_ring[current_slot]
        return None  # Fallback if no server is found (should not happen with valid setup)