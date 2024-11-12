from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token, fake
from core.environment.host import get_host_for_locust_testing


class SignupBehavior(TaskSet):
    def on_start(self):
        self.signup()

    @task
    def signup(self):
        response = self.client.get("/signup")
        csrf_token = get_csrf_token(response)

        response = self.client.post("/signup", data={
            "email": fake.email(),
            "password": fake.password(),
            "csrf_token": csrf_token
        })
        if response.status_code != 200:
            print(f"Signup failed: {response.status_code}")


class LoginBehavior(TaskSet):
    def on_start(self):
        self.ensure_logged_out()
        self.login()

    @task
    def ensure_logged_out(self):
        response = self.client.get("/logout")
        if response.status_code != 200:
            print(f"Logout failed or no active session: {response.status_code}")

    @task
    def login(self):
        response = self.client.get("/login")
        if response.status_code != 200 or "Login" not in response.text:
            print("Already logged in or unexpected response, redirecting to logout")
            self.ensure_logged_out()
            response = self.client.get("/login")

        csrf_token = get_csrf_token(response)

        response = self.client.post("/login", data={
            "email": 'user1@example.com',
            "password": '1234',
            "csrf_token": csrf_token
        })
        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")


class ForgotPasswordBehavior(TaskSet):
    def on_start(self):
        self.ensure_logged_out()

    def ensure_logged_out(self):
        response = self.client.get("/logout")
        if response.status_code != 200:
            print(f"Logout failed or no active session: {response.status_code}")

    @task
    def forgot_password(self):
        response = self.client.get("/forgotpassword/")
        if response.status_code != 200:
            print(f"Failed to access forgot password form: {response.status_code}")
            return

        csrf_token = get_csrf_token(response)
        email = fake.email()
        response = self.client.post("/forgotpassword/", data={
            "email": email,
            "csrf_token": csrf_token
        })

        if response.status_code != 200:
            print(f"Forgot password request failed: {response.status_code}")
            return

        if "OTP code" in response.text:
            otp_code = "123456"
            response = self.client.post("/forgotpassword/code-validation", data={
                "code": otp_code,
                "csrf_token": get_csrf_token(response)  
            })
            if response.status_code != 200:
                print(f"OTP validation failed: {response.status_code}")
            else:
                print("OTP validated successfully")

                response = self.client.get("/resetpassword/")
                if response.status_code != 200:
                    print(f"Failed to load reset password form: {response.status_code}")
                    return

                csrf_token = get_csrf_token(response)
                
                new_password = fake.password()
                response = self.client.post("/resetpassword/", data={
                    "password": new_password,
                    "confirm_password": new_password,
                    "csrf_token": csrf_token
                })

                if response.status_code != 200:
                    print(f"Password reset failed: {response.status_code}")
                else:
                    print(f"Password reset successful. New password: {new_password}")
        else:
            print("OTP code form not found, possibly forgot password failed.")

class AuthUser(HttpUser):
    tasks = [SignupBehavior, LoginBehavior, ForgotPasswordBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()