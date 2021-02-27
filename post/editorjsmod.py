from django_editorjs import EditorJsField
from django_editorjs.widgets import EditorJsWidget
from django.forms import Media

#The widget has been modified so that image and attaches plugins are not loaded from the cdn
#as the modified local versions are being used
#(They have been modified to upload dummy files insted of the actual file)
class EditorJsWidgetMod(EditorJsWidget):
    @property
    def media(self):
        return Media(
            css={"all": ["django-editorjs.css"]},
            js=(
                "https://cdn.jsdelivr.net/combine/npm/@editorjs/editorjs@2.18.0,npm/@editorjs/paragraph@2.7.0,npm/@editorjs/header@2.5.0,npm/@editorjs/list@1.5.0,npm/@editorjs/checklist@1.1.0,npm/@editorjs/quote@2.3.0,npm/@editorjs/raw@2.1.2,npm/@editorjs/embed@2.3.1,npm/@editorjs/delimiter@1.1.0,npm/@editorjs/warning@1.1.1,npm/@editorjs/link@2.2.1,npm/@editorjs/marker@1.2.2,npm/@editorjs/table@1.2.2",
                "django-editorjs.js",
                "editorjs-ImageTool.js",
                "editorjs-AttachesTool.js"
            ),
        )

class EditorJsFieldMod(EditorJsField):
    def formfield(self, *args, **kwargs):
        kwargs["widget"] = EditorJsWidgetMod(editorjs_config=self._editorjs_config)
        return super(EditorJsField,self).formfield(*args, **kwargs)