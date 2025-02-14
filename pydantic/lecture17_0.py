from pydantic import BaseModel, ValidationError

class User(BaseModel):
    age: int
    name: str
    email: str

a=User(age=25, name="John", email="john@example.com")

print(a)    
print(a.age)
print(a.name)
print(a.email)

# Example showing Pydantic's automatic type validation
try:
    # This will succeed - all types are correct
    valid_user = User(age=25, name="John", email="john@example.com")
    print("Valid user created:", valid_user)

    # This will fail - age should be int, not str
    invalid_user = User(age="twenty five", name="Jane", email="jane@example.com")
    print("You won't see this - validation will fail first")

except ValidationError as e:
    print("\nValidation Error:")
    print(e)
    # Will show detailed error explaining age must be an integer
