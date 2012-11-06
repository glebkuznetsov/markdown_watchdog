#!/usr/bin/env python

"""
A script that watches changes to a .md file and compiles to an output file
in response to each change (save) event.
"""

import os
import subprocess
import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

MARKDOWN_CSS_LINK = '<link href="http://kevinburke.bitbucket.org/markdowncss/markdown.css" rel="stylesheet"></link>'

class MarkdownCompilerEventHandler(FileSystemEventHandler):
  """EventHandler that runs markdown whenever any .md file changes."""
  def on_modified(self, event):
    src = event.src_path
    (src_root, src_ext) = os.path.splitext(src)
    if src_ext == '.md':
      outfile = src_root + '.html'
      outfile_fh = open(outfile, 'w')
      outfile_fh.write(MARKDOWN_CSS_LINK + '\n\n')
      subprocess.call(['markdown_py', event.src_path], stdout=outfile_fh)
      outfile_fh.close()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Correct usage: markdown_watchdog.py root"
    print "Exiting."
    sys.exit()
  root = sys.argv[1]

  event_handler = MarkdownCompilerEventHandler()
  observer = Observer()
  observer.schedule(event_handler, path=root)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
