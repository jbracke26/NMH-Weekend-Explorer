import reflex as rx
from app.state import State
from app.pages import home

def callback_page():
    return rx.container(
        rx.text("Processing login...", size="5"),
        rx.script("""
            (function() {
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                
                if (code) {
                    fetch('/handle_callback', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({code: code})
                    }).then(() => {
                        window.location.href = '/';
                    }).catch(() => {
                        window.location.href = '/';
                    });
                } else {
                    window.location.href = '/?error=No authorization code received';
                }
            })();
        """),
        max_width="600px",
        padding="6",
        center_content=True,
    )

def register_routes(app: rx.App):
    app.add_page(home.index, route="/")
    app.add_page(callback_page, route="/auth/google/callback")
