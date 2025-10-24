from enum import Enum

class SecurityLogKeyEnum(Enum):
    LoggedIn = "logged_in"
    Logout = "logout"
    LoginFailed = "login_failed"
    PasswordAuthenticationRequested = "password_authentication_requested"
    PasswordAuthenticated = "password_authenticated"
    PasswordAuthenticationFailed = "password_authentication_failed"
    RemovedLoginSession = "removed_login_session"
    PasswordChanged = "password_changed"
    PasswordChangeRequested = "password_change_requested"
