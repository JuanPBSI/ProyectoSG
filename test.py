import os
from glob import glob


map(os.remove,glob('./parsedLogs/*/log_*'))
map(os.remove,glob('./logs/*/log_*'))
