class AnimeCharacter:
    def __init__(self, *args, **kwargs):
        self.character_id = None
        self.character_description = None
        self.anime_id = None
        self.character_name = None
        self.character_rating = None
        self.character_image = None

        self.set_attributes(args, kwargs)

    def set_attributes(self, args, kwargs):
        attributes = ["character_id", "character_description", "anime_id", "character_name", "character_rating", "character_image"]
        for i, value in enumerate(args):
            if i < len(attributes):
                setattr(self, attributes[i], value)

        for key, value in kwargs.items():
            if key in attributes:
                setattr(self, key, value)

        # Check if all required attributes are set
        missing_attributes = [attr for attr in attributes if getattr(self, attr) is None]
        if missing_attributes:
            raise ValueError(f"Missing required attributes: {', '.join(missing_attributes)}")

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "character_description": self.character_description,
            "anime_id": self.anime_id,
            "character_name": self.character_name,
            "character_rating": self.character_rating,
            "character_image": self.character_image
        }