from django_components import component


@component.register("calendar_nested")
class CalendarNested(component.Component):
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "vcalendar.html"

    def get_context_data(self, date):
        return {
            "date": date,
        }

    def get(self, request, *args, **kwargs):
        context = {
            "date": request.GET.get("date", ""),
        }
        return self.render_to_response(context)

    class Media:
        css = "vcalendar.css"
        js = "vcalendar.js"
