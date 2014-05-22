import sublime, sublime_plugin
import os
import zipfile
import platform
import subprocess

class OpenPackageCommand(sublime_plugin.WindowCommand):
  DEFAULT_NAME = "<default>"
  
  def run(self):
    """コマンドのエントリ. 
    
    パッケージ一覧をクイックパネルに表示する. 
    """
    installed_packages_dir_path = sublime.installed_packages_path()
    self.installed_packages_list = [ p for p in os.listdir(installed_packages_dir_path) if p.endswith('.sublime-package')]
    
    packages_dir_path = sublime.packages_path()
    self.packages_list = [ p for p in os.listdir(packages_dir_path) if os.path.isdir(packages_dir_path + '\\' + p) ]
    
    self.all_packages_list = self.installed_packages_list + self.packages_list
    self.window.show_quick_panel(self.all_packages_list, self.on_done)
    
  def on_done(self, i):
    """パッケージ選択後の処理. 
    
    別ウィンドウで選択されたパッケージを開く. 
    
    Installed Packageのパッケージならzip形式のファイルを解凍する. 
    """
    if i < 0:
      print("canneled")
      return
    
    if i < len(self.installed_packages_list):
      # case of Installed Packages
      package_file_name = self.installed_packages_list[i]
      package_name = os.path.splitext(package_file_name)[0]
      package_file_name = sublime.installed_packages_path() + '/' + package_file_name
      
      # Installed Packagesなら設定ファイルにあるディレクトリに解凍
      settings = sublime.load_settings("Open Sublime Package.sublime-settings")
      extraction_path = settings.get("extraction_path", None)
      
      if type(extraction_path) == str:
        # 文字列 => そのまま使う
        pass
      elif type(extraction_path) == dict:
        # 辞書 => ホスト名に応じてパスを決める
        host = platform.node()
        if host in extraction_path:
          extraction_path = extraction_path[host]
        elif self.DEFAULT_NAME in extraction_path:
          extraction_path = extraction_path[self.DEFAULT_NAME]
        else:
          sublime.error_message("Open Sublime Package: Missing extraction path.")
          return
      else:
        sublime.error_message("Open Sublime Package: Missing extraction path.")
        return
      
      # extraction_pathにパッケージを解凍
      extraction_path = extraction_path + '/' + package_name
      
      # Confirm existing file/directory
      if os.path.isfile(extraction_path):
        sublime.error_message("Open Sublime Package: '" + extraction_path + "' is exists and it is file.")
        return
      elif os.path.isdir(extraction_path) and not sublime.ok_cancel_dialog("Overwrite '%s'?" % extraction_path):
        return
      
      # Extract zip file
      
      with zipfile.ZipFile(package_file_name) as zf:
        zf.extractall(extraction_path)
      
      package_path = extraction_path
    else:
      # case of Packages
      package_name = self.packages_list[i - len(self.installed_packages_list)]
      package_path = sublime.packages_path() + '\\' + package_name
    
    # Open package
    open_folder(package_path)

def open_folder(dir_path):
  """dir_pathにあるディレクトリをSublime Text 3で開く.
  
  現状の実装ではsubprocess.Popenを用いて, 新しいウィンドウを起動する. 
  (これはSideBarEnhancementsパッケージを参考にしたものである)
  """
  subprocess.Popen([sublime.executable_path(), dir_path], cwd=dir_path)
