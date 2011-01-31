from django import template

from urllib import urlencode
from cgi import parse_qs

register = template.Library()

class ExtendQsDisplayNode(template.Node):
    def __init__(self, orig_qs_exp, name, val_exp):
        self.orig_qs_exp = template.Variable(orig_qs_exp)
        self.name = name
        self.val_exp = template.Variable(val_exp)
    
    def render(self, context):
        out_qs = dict(self.orig_qs_exp.resolve(context))
        val = self.val_exp.resolve(context)
        out_qs[self.name] = val
        #if self.as_var:
        #    context[self.as_var] = display
        #    return ""
        return urlencode(out_qs, doseq=1)


@register.tag(name="extend_qs")
def do_extend_qs(parser, token):
    """
    Example: {% extend_qs request.GET page page_obj.next_page_number %}
    """
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' takes three arguments" % bits[0])
    return ExtendQsDisplayNode(*bits[1:])
