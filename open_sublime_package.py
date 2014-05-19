import sublime, sublime_plugin
import os
import zipfile
import platform
import subprocess

class OpenPackageCommand(sublime_plugin.WindowCommand):
  DEFAULT_NAME = "<default>"
  
  def run(self):
    self.installed_packages_dir_path = sublime.installed_packages_path()
    self.packages_dir_path = sublime.packages_path()
    
    
  def on_done(self, i):
    pass


def open_folder(dir_path):
  """dir_pathにあるディレクトリをSublime Text 3で開く.
  
  現状の実装ではsubprocess.Popenを用いて, 新しいウィンドウを起動する. 
  (これはSideBarEnhancementsパッケージを参考にしたものである)
  """
  subprocess.Popen([sublime.executable_path(), dir_path], cwd=dir_path)
