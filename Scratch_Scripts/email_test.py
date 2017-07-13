from getpass import getpass

from machine_learning_tests.helper_functions import send_email

if __name__ == "__main__":
    send_email(
        sender="danieldopp@outlook.com",
        password=getpass("give email password: "),
        receivers=["adammorrone2@gmail.com", "kulkar17@purdue.edu", "danieldopp@outlook.com"],
        subject="Python is perty cool yo",
        message="Test of automated email messaging, let me know if you get this",
    )
