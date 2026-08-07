from src.ui.theme.colors import Colors
from src.ui.theme.radius import Radius


class Styles:

    SEARCH = f"""
    QLineEdit{{
        background:{Colors.SEARCH};
        color:{Colors.TEXT};
        border:1px solid {Colors.BORDER};
        border-radius:{Radius.SEARCH}px;
        padding-left:18px;
        font-size:15px;
    }}

    QLineEdit:focus{{
        border:1px solid {Colors.PRIMARY};
    }}
    """

    BUTTON = f"""
    QPushButton{{
        background:{Colors.PANEL_LIGHT};
        color:{Colors.TEXT};
        border:1px solid {Colors.BORDER};
        border-radius:{Radius.BUTTON}px;
    }}

    QPushButton:hover{{
        border:1px solid {Colors.PRIMARY};
    }}
    """

    CARD = f"""
    background:{Colors.PANEL};
    border:1px solid {Colors.BORDER};
    border-radius:{Radius.CARD}px;
    """