
# external libraries
import io
import re
import json
import httpx
import random
import discord
import traceback
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

from func_utils import *

from func_embed import *

from func_info import *
from func_news import *
from func_quest import *

from bot_methods import *
