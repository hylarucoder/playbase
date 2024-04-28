from django_components import component


@component.register("todo")
class Calendar(component.Component):
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "todo/todo.html"
