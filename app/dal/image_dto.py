class ImageDTO:
    def __init__(self, storage_url, image, embedded, id=None):
        self.id = id
        self.storage_url = storage_url
        self.image = image
        self.embedded = embedded

    def __str__(self):
        return f"ImageDTO(id={self.id}, storage_url={self.storage_url}, image={self.image})"
