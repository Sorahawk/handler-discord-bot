
# external libraries
import io
import re
import random
import discord
import operator
import requests
import subprocess
import googletrans

from lxml import html
from urllib.parse import urljoin
from discord.ext.tasks import loop
from datetime import datetime, time, timedelta, timezone


# internal scripts - order of import matters; load the scripts in order of lowest to highest dependency
import var_global
from var_global import *
from var_secret import *

from func_http import *
from func_message import *

from func_embed import *

from func_info import *
from func_news import *
from func_quest import *

from bot_methods import *
