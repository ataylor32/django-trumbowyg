import copy

from django.conf import settings as django_settings
from django.forms.widgets import Media, Textarea
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
    @property
    def media(self):
        extra_media = copy.deepcopy(settings.EXTRA_MEDIA)

        if "css" in extra_media:
            css = extra_media["css"]

            if "all" not in css:
                css["all"] = []
        else:
            css = {"all": []}

        if "js" in extra_media:
            js = extra_media["js"]
        else:
            js = []

        css["all"].insert(0, "trumbowyg/ui/trumbowyg.min.css")
        css["all"].insert(1, "trumbowyg/plugins/colors/ui/trumbowyg.colors.min.css")

        js.insert(0, "trumbowyg/trumbowyg.min.js")
        js.insert(1, "trumbowyg/plugins/colors/trumbowyg.colors.min.js")
        js.insert(2, "trumbowyg/plugins/fontsize/trumbowyg.fontsize.min.js")
        js.insert(3, "trumbowyg/plugins/upload/trumbowyg.upload.min.js")
        js.insert(4, "trumbowyg/admin.js")

        if get_trumbowyg_language().startswith("en") is False:
            js.insert(5, "trumbowyg/langs/{0}.min.js".format(get_trumbowyg_language()))

        return Media(css=css, js=js)

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
                        ["formatting", "fontsize", "strong", "em"],
                        ["foreColor", "backColor"],
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
