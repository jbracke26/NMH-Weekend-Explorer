import reflex as rx
from typing import Optional

from reflex_google_auth import GoogleAuthState


class State(GoogleAuthState):
    """アプリ全体の状態 + Google ログイン状態を管理する State."""

    # 表示用の現在ユーザー情報
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_picture: str = ""

    # シンプルな認証フラグ
    is_authenticated: bool = False

    # メッセージ表示用
    message: str = ""
    message_type: str = "info"

    def on_google_login_success(self):
        """Google ログイン成功時に呼び出されるフック."""
        # GoogleAuthState が検証済みトークン情報を持っている前提
        if not getattr(self, "token_is_valid", False):
            self.message = "Google login failed."
            self.message_type = "error"
            return

        info = getattr(self, "tokeninfo", {}) or {}
        self.current_user_name = info.get("name") or ""
        self.current_user_email = info.get("email") or ""
        self.current_user_picture = info.get("picture") or ""

        if not self.current_user_email:
            self.message = "Could not get email from Google."
            self.message_type = "error"
            self.is_authenticated = False
            return

        self.is_authenticated = True
        self.message = "Logged in with Google."
        self.message_type = "success"

    def logout(self):
        """ログアウトして状態をクリア."""
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_picture = ""
        self.is_authenticated = False
        self.message = "Logged out."
        self.message_type = "info"

    def clear_message(self):
        """メッセージをクリア."""
        self.message = ""
        self.message_type = "info"