class StorageDTO:
    def __init__(self, email, storage_url):
        self.email = email
        self.storage_url = storage_url

    def __str__(self):
        return f"StorageDTO(email={self.email}, storage_url={self.storage_url})"