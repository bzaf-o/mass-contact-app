import flet as ft
import pyperclip
import os
import importlib.util

# Import default messages from config file
try:
    import config as messages
except ImportError:
    # If the file doesn't exist, use these backup options
    messages = {
        "BTAR Promo": """Do mark your calendar for BTAR scholarship applications, it usually opens early February. 

It's a scholarship under YTAR, full tuition coverage for all MQA-accredited courses and competitive allowance. No bond to serve, but must complete a community project before graduation.

You can read more here: https://www.yayasantar.org.my/tarscholarship""",
    
    "Nudge": """Hello, just bumping this message a bit. I would really appreciate your response on this whenever it's possible for you :) 

In case you prefer not to be contacted further/are not XX, then please let me know as well. Thank you!"""
    }

class walinkgen:
    @staticmethod
    def clean_phone_number(phone_number):
        # Remove all non-digit characters except '+'
        cleaned = ''.join(filter(str.isdigit, phone_number))
        
        # Remove the 0 in front if present and add 6 if not already starting with 6
        if cleaned.startswith('0'):
            cleaned = '60' + cleaned[1:]
        elif not cleaned.startswith('6'):
            cleaned = '6' + cleaned
            
        return cleaned
    
    @staticmethod
    def generate_walink(phone_number):
        cleaned_number = walinkgen.clean_phone_number(phone_number)
        return f"wa.me/{cleaned_number}"

class MessageManager:
    def __init__(self, filename="saved_messages.py"):
        self.filename = filename
        self.messages = self.load_messages()
    
    def load_messages(self):
        if os.path.exists(self.filename):
            try:
                # Import the messages from the config file
                spec = importlib.util.spec_from_file_location("saved_messages", self.filename)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module.saved_messages
            except (ImportError, AttributeError, Exception):
                # If file exists but can't be loaded, return default messages
                return messages.copy()
        else:
            # Create file with default messages if it doesn't exist
            self.create_default_messages_file()
            return messages.copy()
    
    def create_default_messages_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('''# config.py
saved_messages = {
    "BTAR Promo": """Do mark your calendar for BTAR scholarship applications, it usually opens early February. 

It's a scholarship under YTAR, full tuition coverage for all MQA-accredited courses and competitive allowance. No bond to serve, but must complete a community project before graduation.

You can read more here: https://www.yayasantar.org.my/tarscholarship""",
    
    "Nudge": """Hello, just bumping this message a bit. I would really appreciate your response on this whenever it's possible for you :) 

In case you prefer not to be contacted further/are not XX, then please let me know as well. Thank you!"""
}
''')
    
    def save_messages(self):
        # Saves messages to file
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('# saved_messages.py\n')
            f.write('saved_messages = {\n')
            for title, content in self.messages.items():
                # Escape triple quotes and handle multiline strings properly
                escaped_content = content.replace('"""', '"\\'"\\'"'')
                if '\n' in content:
                    f.write(f'    "{title}": """{escaped_content}""",\n')
                else:
                    f.write(f'    "{title}": "{escaped_content}",\n')
            f.write('}\n')
    
    def add_message(self, title, content):
        # Add new message
        self.messages[title] = content
        self.save_messages()
    
    def edit_message(self, old_title, new_title, new_content):
        # Edit existing message
        if old_title in self.messages:
            del self.messages[old_title]
        self.messages[new_title] = new_content
        self.save_messages()
    
    def delete_message(self, title):
        # Delete an existing message
        if title in self.messages:
            del self.messages[title]
            self.save_messages()
            return True
        return False

class ThemeManager:
    def __init__(self):
        self.is_dark = False
        self.primary_dark = "#1d2a45"
        self.accent_dark = "#b89449"
        self.primary_light = "#ffffff"
        self.accent_light = "#2563eb"
        
    def get_theme(self):
        if self.is_dark:
            return {
                "bg_primary": self.primary_dark,
                "bg_surface": "#2d3b5a",
                "text_primary": "#ffffff",
                "text_secondary": "#e2e8f0",
                "accent": self.accent_dark,
                "border": "#374151",
                "card_bg": "#25314d",
                "hover": "#34415e",
                "icon_color": self.accent_dark
            }
        else:
            return {
                "bg_primary": self.primary_light,
                "bg_surface": "#f8fafc",
                "text_primary": "#1e293b",
                "text_secondary": "#64748b",
                "accent": self.accent_light,
                "border": "#e2e8f0",
                "card_bg": "#ffffff",
                "hover": "#f1f5f9",
                "icon_color": self.accent_light
            }

def main(page: ft.Page):
    # Window configuration, currently 9:16
    page.window.width = 360  # 9 * 40
    page.window.height = 640  # 16 * 40
    page.window.min_width = 300
    page.window.min_height = 533
    page.window.resizable = True
    page.window.maximized = False
    page.window.center()  # Start in the middle of the screen
    
    # Theme setup
    theme_manager = ThemeManager()
    page.fonts = {
        "Jost": "https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&display=swap"
    }
    page.theme = ft.Theme(font_family="Jost")
    page.dark_theme = ft.Theme(font_family="Jost")
    
    page.title = "Mass Contact App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Init message manager
    message_manager = MessageManager()
    
    # Confirmation snackbar, yummy
    confirmation_snackbar = ft.SnackBar(
        content=ft.Text("", font_family="Jost", text_align=ft.TextAlign.CENTER),
        behavior=ft.SnackBarBehavior.FLOATING,
        margin=20
    )
    
    def show_confirmation(message):
        confirmation_snackbar.content = ft.Text(message, font_family="Jost", text_align=ft.TextAlign.CENTER)
        confirmation_snackbar.open = True
        page.update()
    
    def apply_theme():
        theme = theme_manager.get_theme()
        page.bgcolor = theme["bg_primary"]
        
        # Update all components with new theme
        whatsapp_section.bgcolor = theme["card_bg"]
        messages_section.bgcolor = theme["card_bg"]
        footer_container.bgcolor = theme["card_bg"]
        
        # Update text colors
        whatsapp_title.color = theme["text_primary"]
        whatsapp_subtitle.color = theme["text_secondary"]
        messages_title.color = theme["text_primary"]
        messages_subtitle.color = theme["text_secondary"]
        generated_link.color = theme["accent"]
        footer_text.color = theme["text_secondary"]
        
        # Update input fields
        phone_input.border_color = theme["border"]
        phone_input.color = theme["text_primary"]
        phone_input.focused_border_color = theme["accent"]
        phone_input.label_style = ft.TextStyle(color=theme["text_secondary"], font_family="Jost")
        phone_input.text_style = ft.TextStyle(font_family="Jost")
        
        # Update buttons
        generate_btn.style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=theme["accent"],
            elevation=8,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
        
        add_btn.style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=theme["accent"],
            elevation=8,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
        
        # Update message tiles container
        message_container.border = ft.border.all(1, theme["border"])
        message_container.bgcolor = theme["bg_surface"]
        
        # Update dialog text styles
        add_title.text_style = ft.TextStyle(font_family="Jost")
        add_content.text_style = ft.TextStyle(font_family="Jost")
        edit_title.text_style = ft.TextStyle(font_family="Jost")
        edit_content.text_style = ft.TextStyle(font_family="Jost")
        
        # Refresh message list to update colors instantly
        refresh_message_list()
        
        page.update()
    
    def toggle_theme(e):
        theme_manager.is_dark = not theme_manager.is_dark
        page.theme_mode = ft.ThemeMode.DARK if theme_manager.is_dark else ft.ThemeMode.LIGHT
        theme_btn.icon = ft.Icons.DARK_MODE if theme_manager.is_dark else ft.Icons.LIGHT_MODE
        theme_btn.tooltip = "Switch to Light Mode" if theme_manager.is_dark else "Switch to Dark Mode"
        apply_theme()
    
    # Theme toggle button
    theme_btn = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Switch to Dark Mode",
        on_click=toggle_theme,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor={"": "#b89449", "hovered": "#a8833a"}
        )
    )
    
    # WhatsApp Link Generator Section
    def generate_walink(e):
        phone_number = phone_input.value.strip()
        if not phone_number:
            show_confirmation("Enter a phone number")
            return
        
        try:
            whatsapp_link = walinkgen.generate_walink(phone_number)
            pyperclip.copy(whatsapp_link)
            show_confirmation("Copied WhatsApp link: " + whatsapp_link)
            generated_link.value = f"Generated: {whatsapp_link}"
            page.update()
        except Exception as ex:
            show_confirmation(f"Error generating link: {str(ex)}")
    
    phone_input = ft.TextField(
        label="Phone Number",
        hint_text="e.g., 012-659 0007",
        width=400,
        prefix_icon=ft.Icons.PHONE,
        border_radius=8,
        filled=True,
        text_size=14,
        text_style=ft.TextStyle(font_family="Jost"),
        label_style=ft.TextStyle(font_family="Jost"),
        text_align=ft.TextAlign.LEFT
    )
    
    generated_link = ft.Text(
        value="",
        size=14,
        weight=ft.FontWeight.W_600,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER
    )
    
    generate_btn = ft.ElevatedButton(
        text="Generate & Copy WhatsApp Link",
        icon=ft.Icons.LINK,
        on_click=generate_walink,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=8
        )
    )
    
    whatsapp_title = ft.Text(
        "WhatsApp Link Generator", 
        size=24, 
        weight=ft.FontWeight.W_700,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER
    )
    
    whatsapp_subtitle = ft.Text(
        "Enter a phone number to generate a WhatsApp link.",
        size=14,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER
    )
    
    whatsapp_section = ft.Container(
        content=ft.Column([
            ft.Row([
                whatsapp_title,
                theme_btn
            ], alignment=ft.MainAxisAlignment.CENTER),
            whatsapp_subtitle,
            ft.Container(phone_input, alignment=ft.alignment.center),
            ft.Container(generate_btn, alignment=ft.alignment.center),
            generated_link
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=25,
        margin=10,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4)
        ),
        width=600
    )
    
    # Pre-saved Messages Section
    message_tiles = ft.Column(spacing=8)
    
    def copy_message(message_title, message_content):
        pyperclip.copy(message_content)
        show_confirmation(f"Copied {message_title} message")
    
    def on_tile_hover(e, title, content):
        theme = theme_manager.get_theme()
        if e.data == "true":
            e.control.bgcolor = theme["hover"]
        else:
            e.control.bgcolor = theme["bg_surface"]
        e.control.update()
    
    def refresh_message_list():
        message_tiles.controls.clear()
        theme = theme_manager.get_theme()
        
        for title, content in message_manager.messages.items():
            # Create a new container for each message with current theme
            tile_container = ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.MESSAGE, color=theme["icon_color"]),
                    title=ft.Text(
                        title, 
                        weight=ft.FontWeight.W_600,
                        font_family="Jost",
                        color=theme["text_primary"],
                        text_align=ft.TextAlign.LEFT
                    ),
                    subtitle=ft.Text(
                        content[:60] + "..." if len(content) > 60 else content,  # Changed from 80 to 60 characters
                        font_family="Jost",
                        color=theme["text_secondary"],
                        text_align=ft.TextAlign.LEFT
                    ),
                    trailing=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.CONTENT_COPY,
                            icon_color=theme["icon_color"],
                            tooltip="Copy Message",
                            on_click=lambda e, t=title, c=content: copy_message(t, c),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6)
                            )
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=theme["icon_color"],
                            tooltip="Edit Message",
                            on_click=lambda e, t=title, c=content: open_edit_dialog(t, c),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6)
                            )
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_400,
                            tooltip="Delete Message",
                            on_click=lambda e, t=title: open_delete_dialog(t),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6)
                            )
                        )
                    ], tight=True, spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                border_radius=8,
                bgcolor=theme["bg_surface"],
                on_hover=lambda e, t=title, c=content: on_tile_hover(e, t, c)
            )
            
            message_tiles.controls.append(tile_container)
        
        page.update()
    
    # Add Message Dialog
    def open_add_dialog(e):
        add_title.value = ""
        add_content.value = ""
        add_dialog.open = True
        page.update()
    
    def save_new_message(e):
        title = add_title.value.strip()
        content = add_content.value.strip()
        
        if not title or not content:
            show_confirmation("Please fill in both title and content.")
            return
        
        if title in message_manager.messages:
            show_confirmation("A message with this title already exists!")
            return
        
        message_manager.add_message(title, content)
        refresh_message_list()
        add_dialog.open = False
        show_confirmation(f"Added new message: {title}")
        page.update()
    
    add_title = ft.TextField(
        label="Message Title", 
        width=600,  # Increased from 400 to 600 (1.5x wider)
        border_radius=8,
        text_style=ft.TextStyle(font_family="Jost"),
        label_style=ft.TextStyle(font_family="Jost"),
        text_align=ft.TextAlign.LEFT
    )
    add_content = ft.TextField(
        label="Message Content", 
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=600,  # Increased from 400 to 600 (1.5x wider)
        border_radius=8,
        text_style=ft.TextStyle(font_family="Jost"),
        label_style=ft.TextStyle(font_family="Jost"),
        text_align=ft.TextAlign.LEFT
    )
    
    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add New Message", font_family="Jost", text_align=ft.TextAlign.CENTER),
        content=ft.Column([add_title, add_content], tight=True, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ft.Row([
                ft.TextButton(
                    "Cancel", 
                    on_click=lambda e: setattr(add_dialog, 'open', False) or page.update()
                ),
                ft.TextButton(
                    "Save", 
                    on_click=save_new_message
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Edit Message Dialog
    def open_edit_dialog(old_title, old_content):
        edit_old_title.value = old_title
        edit_title.value = old_title
        edit_content.value = old_content
        edit_dialog.open = True
        page.update()
    
    def save_edited_message(e):
        old_title = edit_old_title.value
        new_title = edit_title.value.strip()
        new_content = edit_content.value.strip()
        
        if not new_title or not new_content:
            show_confirmation("Please fill in both title and content.")
            return
        
        message_manager.edit_message(old_title, new_title, new_content)
        refresh_message_list()
        edit_dialog.open = False
        show_confirmation(f"Updated message: {new_title}")
        page.update()
    
    edit_old_title = ft.TextField(visible=False)
    edit_title = ft.TextField(
        label="Message Title", 
        width=600,
        border_radius=8,
        text_style=ft.TextStyle(font_family="Jost"),
        label_style=ft.TextStyle(font_family="Jost"),
        text_align=ft.TextAlign.LEFT
    )
    edit_content = ft.TextField(
        label="Message Content", 
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=600,
        border_radius=8,
        text_style=ft.TextStyle(font_family="Jost"),
        label_style=ft.TextStyle(font_family="Jost"),
        text_align=ft.TextAlign.LEFT
    )
    
    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Message", font_family="Jost", text_align=ft.TextAlign.CENTER),
        content=ft.Column([edit_title, edit_content], tight=True, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ft.Row([
                ft.TextButton(
                    "Cancel", 
                    on_click=lambda e: setattr(edit_dialog, 'open', False) or page.update()
                ),
                ft.TextButton(
                    "Save", 
                    on_click=save_edited_message
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Delete Confirmation Dialog
    def open_delete_dialog(title):
        delete_title.value = title
        delete_dialog.open = True
        page.update()
    
    def confirm_delete(e):
        title = delete_title.value
        if message_manager.delete_message(title):
            refresh_message_list()
            show_confirmation(f"Deleted message: {title}")
        delete_dialog.open = False
        page.update()
    
    delete_title = ft.TextField(visible=False)
    delete_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Delete Message", font_family="Jost", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Are you sure you want to delete this message?", font_family="Jost", text_align=ft.TextAlign.CENTER),
        actions=[
            ft.Row([
                ft.TextButton(
                    "Cancel", 
                    on_click=lambda e: setattr(delete_dialog, 'open', False) or page.update()
                ),
                ft.TextButton(
                    "Delete", 
                    on_click=confirm_delete, 
                    style=ft.ButtonStyle(color=ft.Colors.RED)
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Messages Section UI
    messages_title = ft.Text(
        "Pre-saved Messages", 
        size=24, 
        weight=ft.FontWeight.W_700,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER
    )
    
    messages_subtitle = ft.Text(
        "Click the copy icon to copy a message to your clipboard.",
        size=14,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER
    )
    
    add_btn = ft.ElevatedButton(
        text="Add New Message",
        icon=ft.Icons.ADD,
        on_click=open_add_dialog,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=8
        )
    )
    
    message_container = ft.Container(
        content=message_tiles,
        margin=ft.margin.only(top=10),
        padding=15,
        border_radius=10
    )
    
    messages_section = ft.Container(
        content=ft.Column([
            ft.Row([messages_title], alignment=ft.MainAxisAlignment.CENTER),
            messages_subtitle,
            ft.Container(add_btn, alignment=ft.alignment.center),
            message_container
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=25,
        margin=10,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4)
        ),
        width=600
    )
    
    # Footer Section
    footer_text = ft.Text(
        "Created by Balqis Zafirah",
        size=14,
        font_family="Jost",
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_500
    )
    
    github_link = ft.TextButton(
        content=ft.Text("Github", font_family="Jost", size=14),
        on_click=lambda e: page.launch_url("https://github.com/bzaf-o/mass-contact-app")
    )
    
    email_link = ft.TextButton(
        content=ft.Text("Email", font_family="Jost", size=14),
        on_click=lambda e: page.launch_url("mailto:balqiszafirah.o@gmail.com")
    )
    
    footer_container = ft.Container(
        content=ft.Column([
            footer_text,
            ft.Row([
                github_link,
                ft.Text("•", font_family="Jost", size=14),
                email_link
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        margin=10,
        border_radius=15,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2)
        ),
        width=600
    )
    
    # Init the message list
    refresh_message_list()
    
    # Add dialogs to page
    page.overlay.extend([add_dialog, edit_dialog, delete_dialog, confirmation_snackbar])
    
    # Apply initial theme
    apply_theme()
    
    # Main layout
    page.add(
        ft.Column([
            whatsapp_section,
            messages_section,
            footer_container
        ], scroll=ft.ScrollMode.ADAPTIVE, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)