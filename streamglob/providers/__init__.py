import abc
import re

from stevedore import extension
from orderedattrdict import AttrDict

from .. import session
from .. import config
from functools import wraps

# from . import base
# from . import mlb
# from .mlb import *

PROVIDERS = AttrDict()
DEFAULT_PROVIDER=None

def get(provider, *args, **kwargs):
    # raise Exception(provider)
    try:
        return PROVIDERS.get(provider)(*args, **kwargs)
    except TypeError:
        raise Exception(provider, PROVIDERS)

def load():
    global PROVIDERS
    global DEFAULT_PROVIDER
    mgr = extension.ExtensionManager(
        namespace='streamglob.providers',
        # invoke_args=(parsed_args.width,),
    )

    PROVIDERS = AttrDict((x.name, x.plugin) for x in mgr)
    # raise Exception(PROVIDERS)
    if len(config.settings.profile.providers):
        # first listed in config
        DEFAULT_PROVIDER = list(config.settings.profile.providers.keys())[0]
    else:
        # first loaded
        DEFAULT_PROVIDER = list(PROVIDERS.keys())[0]

# @with_filters(DateFilter, FixedListingFilter)
# class TestProvider(base.SimpleProviderViewMixin, base.BaseProvider):

#     SESSION_CLASS = session.StreamSession
#     @property
#     def filters(self):
#         return AttrDict([
#             ("foo",  FixedListingFilter(["foo", "bar", "baz"]))
#         ])

#     def login(self):
#         print(self.session)

#     def listings(self):
#         return [ MediaItem(title=t) for t in ["a", "b" ,"c" ] ]

# PROVIDERS_RE = re.compile(r"(.+)Provider$")
# PROVIDERS = [ k.replace("Provider", "").lower()
#               for k in globals() if PROVIDERS_RE.search(k) ]