from django import template

register = template.Library()

@register.filter
def update_watching(watching):
    watching = True
    #return watching 
#register.filter