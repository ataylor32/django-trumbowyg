from django.conf import settings as django_settings
from django.forms.widgets import Textarea
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import settings


def get_trumbowyg_language():
    """
    Get and convert language from django to trumbowyg format

    Example:
        Django uses: pt-br and trumbowyg use pt_br
    """
    language = getattr(settings, "TRUMBOWYG_LANGUAGE", django_settings.LANGUAGE_CODE)
    return language.replace("-", "_")


class TrumbowygWidget(Textarea):
    class Media:
        css = {
            "all": (
                "trumbowyg/ui/trumbowyg.min.css",
            )
        }
        js = [
            "trumbowyg/trumbowyg.min.js",
            "trumbowyg/plugins/upload/trumbowyg.upload.min.js",
            "trumbowyg/admin.js",
        ] + (
            []
            if get_trumbowyg_language().startswith("en")
            else ["trumbowyg/langs/{0}.min.js".format(get_trumbowyg_language())]
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs)
        script = """
            <script>
                $("#id_{name}").trumbowyg({{
                    lang: "{lang}",
                    semantic: {semantic},
                    resetCss: true,
                    autogrow: true,
                    removeformatPasted: true,
                    btnsDef: {{
                        image: {{
                            dropdown: ["upload", "insertImage", "base64", "noembed"],
                            ico: "insertImage"
                        }}
                    }},
                    btns: [
                        ["formatting", "strong", "em"],
                        ["link"],
                        ["image"],
                        ["justifyLeft", "justifyCenter", "justifyRight", "justifyFull"],
                        ["unorderedList", "orderedList"],
                        ["horizontalRule"],
                        ["blockquote"],
                        ["removeformat"],
                        ["viewHTML"],
                        ["fullscreen"]
                    ],
                    plugins: {{
                        upload: {{
                            serverPath: "{path}",
                            fileFieldName: "image",
                            statusPropertyName: "success",
                            urlPropertyName: "file"
                        }}
                    }},
                    svgPath: "{svg_path}",
                }});
            </script>
        """.format(
            name=name,
            lang=get_trumbowyg_language(),
            semantic=settings.SEMANTIC,
            path=reverse("trumbowyg_upload_image"),
            svg_path=static("trumbowyg/ui/icons.svg"),
        )
        output += mark_safe(script)
        return output
