import reflex as rx
from app.state import State
from app.config import Config
from reflex_google_auth import google_login, google_oauth_provider


_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def index():
    """Login page: Shows Google login button if not authenticated, redirects to /explore if authenticated."""
    return rx.container(
        rx.script("""
            (function() {
                let lastRedirectPath = '';
                let lastIsAuthenticated = false;
                
                function performRedirect(path) {
                    if (path && path !== window.location.pathname) {
                        console.log('Home: Redirecting to:', path);
                        window.location.href = path;
                    }
                }
                
                function checkAndRedirect() {
                    const hiddenInput = document.getElementById('redirect_path_hidden');
                    const authInput = document.getElementById('is_authenticated_hidden');
                    
                    if (hiddenInput) {
                        const currentPath = hiddenInput.value || '';
                        if (currentPath && currentPath !== lastRedirectPath && currentPath !== '') {
                            lastRedirectPath = currentPath;
                            performRedirect(currentPath);
                            return;
                        }
                    }
                    
                    if (authInput) {
                        const isAuth = authInput.value === 'true';
                        if (isAuth && !lastIsAuthenticated && window.location.pathname === '/') {
                            lastIsAuthenticated = isAuth;
                            performRedirect('/explore');
                            return;
                        }
                        lastIsAuthenticated = isAuth;
                    }
                }
                
                // より頻繁にチェック（50ms間隔）
                setInterval(checkAndRedirect, 50);
                
                // 初回チェック
                setTimeout(checkAndRedirect, 10);
            })();
        """),
        rx.input(
            id="redirect_path_hidden",
            type="hidden",
            value=State.redirect_path,
        ),
        rx.input(
            id="is_authenticated_hidden",
            type="hidden",
            value=State.is_authenticated,
        ),
        rx.cond(
            State.is_authenticated,
            rx.fragment(
                rx.text("Redirecting to explore page...", size="4"),
                rx.script("window.location.href = '/explore';"),
            ),
            rx.vstack(
                rx.heading("Weekend Explorer", size="9", margin_bottom="2"),
                rx.text(
                    "Welcome! Please log in with your Google account to continue.",
                    size="5",
                    color="gray",
                    margin_bottom="6",
                ),
                rx.cond(
                    GOOGLE_CLIENT_ID != "",
                    google_oauth_provider(
                        google_login(
                            on_success=State.on_google_login_success,
                        ),
                        client_id=GOOGLE_CLIENT_ID,
                    ),
                    rx.vstack(
                        rx.text(
                            "Google OAuth is not configured.",
                            size="3",
                            color="red",
                            margin_bottom="2",
                        ),
                        rx.text(
                            f"Please set GOOGLE_CLIENT_ID in your .env file.",
                            size="2",
                            color="gray",
                        ),
                        spacing="2",
                    ),
                ),
                rx.script(f"""
                    console.log('Current origin:', window.location.origin);
                    console.log('GOOGLE_CLIENT_ID configured:', '{GOOGLE_CLIENT_ID}' !== '');
                    console.log('GOOGLE_CLIENT_ID value:', '{GOOGLE_CLIENT_ID}');
                """),
                rx.cond(
                    State.message != "",
                    rx.callout(
                        State.message,
                        icon="info",
                        color_scheme=State.message_type,
                        width="100%",
                        margin_top="4",
                    ),
                ),
                spacing="4",
                align="center",
                padding="8",
            ),
        ),
        max_width="800px",
        padding="6",
        center_content=True,
    )
