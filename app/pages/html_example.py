import reflex as rx

def html_example():
    return rx.container(
        rx.heading("HTML Examples in Reflex", size="9"),
        
        rx.heading("Method 1: Using rx.el (HTML elements)", size="6", margin_top="4"),
        rx.el.div(
            rx.el.h1("This is an H1 tag"),
            rx.el.p("This is a paragraph tag"),
            rx.el.span("This is a span tag", style={"color": "blue"}),
            rx.el.button("Click me", type="button"),
            style={"padding": "20px", "border": "1px solid #ccc", "margin": "10px 0"}
        ),
        
        rx.heading("Method 2: Using rx.script for JavaScript", size="6", margin_top="4"),
        rx.script("console.log('Hello from Reflex!');"),
        
        rx.heading("Method 3: Using rx.html.raw for raw HTML", size="6", margin_top="4"),
        rx.html.raw("""
            <div style="padding: 20px; background: #f0f0f0; margin: 10px 0;">
                <h2>Raw HTML</h2>
                <p>This is raw HTML content</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                    <li>Item 3</li>
                </ul>
            </div>
        """),
        
        rx.heading("Method 4: Using Reflex components (Recommended)", size="6", margin_top="4"),
        rx.vstack(
            rx.heading("This is a Reflex heading component"),
            rx.text("This is a Reflex text component"),
            rx.button("This is a Reflex button", color_scheme="blue"),
            spacing="4",
        ),
        
        rx.heading("Method 5: Mixing HTML and Reflex components", size="6", margin_top="4"),
        rx.el.div(
            rx.heading("Reflex heading inside HTML div"),
            rx.el.p("HTML paragraph with ", rx.text("Reflex text", color="red", as_="span"), " inside"),
            style={"padding": "20px", "border": "2px solid green", "margin": "10px 0"}
        ),
        
        max_width="1000px",
        padding="6",
    )

