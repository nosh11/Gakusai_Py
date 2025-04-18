


import yaml


class User:
    def __init__(self):
        self.name: str = ""
        self.level: int = 0
        self.experience: int = 0
        self.coins: int = 0
        self.items: list[str] = []
        self.achievements: list[str] = []
        self.settings: dict[str, bool] = {}
        
    def __str__(self):
        return f"User(name={self.name}, level={self.level}, experience={self.experience}, coins={self.coins}, items={self.items}, achievements={self.achievements}, settings={self.settings})"
    

    def save(self):
        # save by yaml
        import yaml
        with open("user_data.yaml", "w") as file:
            yaml.dump(self.__dict__, file)
        print("User data saved successfully.")
        
    @staticmethod
    def load():
        user: User
        with open("user_data.yaml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            user = User()
            user.__dict__.update(data)
        print("User data loaded successfully.")
        return user
    
    @staticmethod
    def load_or_create():
        try:
            return User.load()
        except FileNotFoundError:
            print("No user data found. Creating a new user.")
            return User()
        except yaml.YAMLError as e:
            print(f"Error loading user data: {e}")
            return User()
    
if __name__ == "__main__":
    user = User()
    user.name = "John Doe"
    user.level = 1
    user.experience = 0
    user.coins = 100
    user.items = ["item1", "item2"]
    user.achievements = ["achievement1"]
    user.settings = {"setting1": True, "setting2": False}
    
    print(user)
    
    # Save the user data
    user.save()
    
    # Load the user data
    loaded_user = User.load()
    print(loaded_user)