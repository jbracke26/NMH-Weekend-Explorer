COLORS = {
    "primary": "#6366f1",
    "bg": "var(--color-background)",
    "bg_secondary": "var(--gray-2)",
    "text": "var(--gray-12)",
    "text_muted": "var(--gray-11)",
    "border": "var(--gray-6)",
    "hover": "var(--gray-3)",
}

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
}

SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
}

RADIUS = {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
}


def card_style(**kwargs):
    """Clean card style following system theme"""
    defaults = {
        "background": COLORS["bg"],
        "border": f"1px solid {COLORS['border']}",
        "border_radius": RADIUS["md"],
        "box_shadow": SHADOWS["sm"],
    }
    return {**defaults, **kwargs}


def button_style(variant="primary", **kwargs):
    """Clean button style"""
    base = {
        "border_radius": RADIUS["sm"],
        "transition": "all 0.2s ease",
    }

    if variant == "primary":
        base.update(
            {
                "background": COLORS["primary"],
                "color": "white",
                "_hover": {"opacity": "0.9"},
            }
        )

    return {**base, **kwargs}


def hover_lift(**kwargs):
    """Simple hover effect"""
    defaults = {
        "transition": "transform 0.2s ease, box-shadow 0.2s ease",
        "_hover": {
            "transform": "translateY(-2px)",
            "box_shadow": SHADOWS["md"],
        },
    }
    return {**defaults, **kwargs}
