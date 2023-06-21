
from django_neomodel import DjangoNode
from neomodel import StringProperty, StructuredNode,RelationshipTo


class User(StructuredNode):
    name = StringProperty()
    email = StringProperty()
    password = StringProperty()
    ip_address = StringProperty()
    signed_in = RelationshipTo("User", "SIGNED_IN")



