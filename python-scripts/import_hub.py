import io
import re
import random
import discord
import requests
import subprocess
import googletrans

from lxml import html
from discord.ext.tasks import loop
from datetime import datetime, time, timedelta, timezone


import var_global
from var_global import *
from var_secret import *

from func_http import *
from func_embed import *
from func_message import *

from bot_tasks import *
from bot_methods import *
