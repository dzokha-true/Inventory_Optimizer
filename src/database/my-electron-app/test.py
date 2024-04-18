import sys

# Example credentials
# WARNING: In a real application, never store passwords in plain text!
# Always use proper password management by hashing and salting passwords.
users = {
    "user1": "password1",
    "admin": "adminpassword"
}

def login(username, password):
    # Check if the username exists and the password matches.
    if users.get(username) == password:
        print("Success")  # Output for successful login
        return True
    else:
        print("Failure")  # Output for failed login
        return False

if __name__ == "__main__":
    # Check if username and password are provided as command-line arguments
    if len(sys.argv) == 3:
        _, username, password = sys.argv
        login(username, password)
    else:
        print("Usage: LoginSystem.py <username> <password>")
        sys.exit(1)

