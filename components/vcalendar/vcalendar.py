from django_components import component


@component.register("vcalendar")
class Calendar(component.Component):
    class Media:
        css = "vcalendar/vcalendar.css"
        js = "vcalendar/vcalendar.js"

    template_name = "vcalendar/vcalendar.html"

    def get_context_data(self, date):
        return {
            "date": date,
        }

    def get(self, request, *args, **kwargs):
        context = {
            "date": request.GET.get("date", ""),
        }
        return self.render_to_response(context)


@component.register("vcalendar_relative")
class CalendarRelative(component.Component):
    template_name = "vcalendar.html"

    class Media:
        css = "vcalendar.css"
        js = "vcalendar.js"

    def get_context_data(self, date):
        return {
            "date": date,
        }

    def get(self, request, *args, **kwargs):
        context = {
            "date": request.GET.get("date", ""),
        }
        return self.render_to_response(context)
