# screenshot_if_different_py
範囲指定してスクリーンショットを取得し、監視範囲に差分があれば保存する。  Save screenshot when the monitoring range changed.


Microsoft Windows [Version 10.0.19042.1526]
2022/03/16  16:02

 遠隔会議/セミナーの画面共有を監視して、差分があればスクリーンショット保存するようにしたい
 pyautoguiでスクリーンショットを撮れる
 さっそくインストール

 pipのアップグレード
 〇python -m pip install --upgrade pip --proxy xxx.xxx.xxx.xxx:yyyy (以下、プロキシ設定は記載しない)
    Installing collected packages: pip
      Uninstalling pip-19.1.1:
      Successfully installed pip-22.0.4

 pyautoguiをインストール・・・pymsgboxで失敗。
 ×pip install pyautogui
    PyMsgBox-1.0.9.tar.gz (18 kB)  Installing build dependencies ... error

 pyautoguiのバージョンを下げてインストール・・・失敗。
 ×pip install pymsgbox==1.0.8

 pyautoguiのバージョンをさらに下げてインストール・・・成功。
 〇pip install pymsgbox==1.0.7

 改めてpyautoguiをインストール・・・pyscreezeで失敗。
 ×pip install pyautogui
    PyScreeze-0.1.28.tar.gz (25 kB)  Installing build dependencies ... error

 pyscreezeのバージョンを下げてインストール・・・失敗。
 ×pip install pyscreeze==0.1.27

 pyscreezeのバージョンをさらに下げてインストール・・・成功。
 〇pip install pyscreeze==0.1.26

 改めてpyautoguiをインストール・・・成功。
 〇pip install pyautogui
    PyAutoGUI-0.9.53.tar.gz (59 kB)
        ;

 使ってみたら、pyautogui/__init__.pyでエラー
 ×import pyautogui
    File "C:\bin\Python37\lib\site-packages\pyautogui\__init__.py", line 221, in <module>
       locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__
    AttributeError: module 'pyscreeze' has no attribute 'locateOnWindow'

 インターネットで調べて、C:\bin\Python37\Lib\site-packages\pyautogui\__init__.pyを編集
 https://github.com/asweigart/pyautogui/issues/598
   C:\bin\Python37\Lib\site-packages\pyautogui\__init__.py  v0.9.53  221行目
       - locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__
       + locateOnWindow.__doc__ = pyscreeze.locateOnScreen.__doc__

 動いた！
 ここまで 2022/03/17

 スクリーンショットを撮るのはpyautoguiじゃなくても良いみたい？
 pyscreezeだけあれば良さそうなので、C:\bin\Python37\Lib\site-packages\pyautogui\__init__.pyを編集する必要無さそう。
 pyautogui必要無かった。
 import pyautoguiをやめ、import pyscreezeとして完成。
 ここまで 2022/03/18



#以下、コマンドライン上でやったこと



$>>>  python -m pip install --upgrade pip --proxy ANY_PROXY_ADDRESS
Installing collected packages: pip
  Found existing installation: pip 19.1.1
    Uninstalling pip-19.1.1:
      Successfully uninstalled pip-19.1.1
Successfully installed pip-22.0.4



$>>>  pip install pyautogui --proxy ANY_PROXY_ADDRESS
Collecting pyautogui
  Using cached PyAutoGUI-0.9.53.tar.gz (59 kB)
  Preparing metadata (setup.py) ... done
Collecting pymsgbox
  Using cached PyMsgBox-1.0.9.tar.gz (18 kB)
  Installing build dependencies ... error
  error: subprocess-exited-with-error

  × pip subprocess to install build dependencies did not run successfully.
  │ exit code: 1
  ╰─> [7 lines of output]
      WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001F6974CDF28>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/setuptools/
      WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001F696DB0208>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/setuptools/
      WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001F696DB02B0>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/setuptools/
      WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001F696DB0400>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/setuptools/
      WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x000001F696DB0550>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/setuptools/
      ERROR: Could not find a version that satisfies the requirement setuptools>=40.8.0 (from versions: none)
      ERROR: No matching distribution found for setuptools>=40.8.0
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: subprocess-exited-with-error

× pip subprocess to install build dependencies did not run successfully.
│ exit code: 1
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.



$>>>  pip install pymsgbox --proxy ANY_PROXY_ADDRESS
Collecting pymsgbox
  Using cached PyMsgBox-1.0.9.tar.gz (18 kB)
  Installing build dependencies ... canceled
ERROR: Operation cancelled by user



$>>>  pip3 install pymsgbox==1.0.8 --proxy ANY_PROXY_ADDRESS
Collecting pymsgbox==1.0.8
  Downloading PyMsgBox-1.0.8.tar.gz (18 kB)
  Installing build dependencies ... canceled
ERROR: Operation cancelled by user



$>>>  pip3 install pymsgbox==1.0.7 --proxy ANY_PROXY_ADDRESS
Collecting pymsgbox==1.0.7
  Downloading PyMsgBox-1.0.7.tar.gz (18 kB)
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: pymsgbox
  Building wheel for pymsgbox (setup.py) ... done
  Created wheel for pymsgbox: filename=PyMsgBox-1.0.7-py3-none-any.whl size=7326 sha256=6e601afac1ebfb9f86dc6ec47e247215f007fdb9b444485b8b603ff06d3edff1
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\57\a1\d5\59080c50fe33e5d5fcac2178d2a8229c03e02dfcd6f06c74fd
Successfully built pymsgbox
Installing collected packages: pymsgbox
Successfully installed pymsgbox-1.0.7



$>>>  pip install pyautogui --proxy ANY_PROXY_ADDRESS
Collecting pyautogui
  Using cached PyAutoGUI-0.9.53.tar.gz (59 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: pymsgbox in c:\bin\python37\lib\site-packages (from pyautogui) (1.0.7)
Collecting PyTweening>=1.0.1
  Downloading pytweening-1.0.4.tar.gz (14 kB)
  Preparing metadata (setup.py) ... done
Collecting pyscreeze>=0.1.21
  Downloading PyScreeze-0.1.28.tar.gz (25 kB)
  Installing build dependencies ... canceled
ERROR: Operation cancelled by user



$>>>  pip install pyscreeze==0.1.27 --proxy ANY_PROXY_ADDRESS
Collecting pyscreeze==0.1.27
  Downloading PyScreeze-0.1.27.tar.gz (25 kB)
  Installing build dependencies ... canceled
ERROR: Operation cancelled by user



$>>>  pip install pyscreeze==0.1.26 --proxy ANY_PROXY_ADDRESS
Collecting pyscreeze==0.1.26
  Downloading PyScreeze-0.1.26.tar.gz (23 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: Pillow>=5.2.0 in c:\bin\python37\lib\site-packages (from pyscreeze==0.1.26) (6.0.0)
Building wheels for collected packages: pyscreeze
  Building wheel for pyscreeze (setup.py) ... done
  Created wheel for pyscreeze: filename=PyScreeze-0.1.26-py3-none-any.whl size=11938 sha256=f816f863f0121caaac2ed227b1ef082879a8b91f57675366d8dbf190b5175fad
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\42\22\f9\345a4a833dfa4c9c903db7a283960598051b2fa2136004ac3d
Successfully built pyscreeze
Installing collected packages: pyscreeze
Successfully installed pyscreeze-0.1.26



$>>>  pip install pyautogui --proxy ANY_PROXY_ADDRESS
Collecting pyautogui
  Using cached PyAutoGUI-0.9.53.tar.gz (59 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: pymsgbox in c:\bin\python37\lib\site-packages (from pyautogui) (1.0.7)
Collecting PyTweening>=1.0.1
  Using cached pytweening-1.0.4.tar.gz (14 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: pyscreeze>=0.1.21 in c:\bin\python37\lib\site-packages (from pyautogui) (0.1.26)
Collecting pygetwindow>=0.0.5
  Downloading PyGetWindow-0.0.9.tar.gz (9.7 kB)
  Preparing metadata (setup.py) ... done
Collecting mouseinfo
  Downloading MouseInfo-0.1.3.tar.gz (10 kB)
  Preparing metadata (setup.py) ... done
Collecting pyrect
  Downloading PyRect-0.2.0.tar.gz (17 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: Pillow>=5.2.0 in c:\bin\python37\lib\site-packages (from pyscreeze>=0.1.21->pyautogui) (6.0.0)
Collecting pyperclip
  Downloading pyperclip-1.8.2.tar.gz (20 kB)
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: pyautogui, pygetwindow, PyTweening, mouseinfo, pyperclip, pyrect
  Building wheel for pyautogui (setup.py) ... done
  Created wheel for pyautogui: filename=PyAutoGUI-0.9.53-py3-none-any.whl size=36589 sha256=4a2a731c6c97f9941098e110f2c7475667d011378fd8fed53adf4fa08270476f
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\23\db\81\a14b5eca81ccb97c15e5bbea8d5394b8cbf6b36451d89dd648
  Building wheel for pygetwindow (setup.py) ... done
  Created wheel for pygetwindow: filename=PyGetWindow-0.0.9-py3-none-any.whl size=11088 sha256=b1822ad7afdba999ac121744699aa57aab427fe773f2e0f68bcc56b1dea996ed
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\91\7e\35\62d9062a06cfc46fea39e26860253da36f258b3f3fd96c91c3
  Building wheel for PyTweening (setup.py) ... done
  Created wheel for PyTweening: filename=pytweening-1.0.4-py3-none-any.whl size=5828 sha256=5ddf062c1ad8a3b7efd4b27da66fcebabe01c7519d80ad94930742fa420598a8
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\13\0b\3b\73efc9b0421547a03ed3208c92a88ccddae2ce853c1e6da7e9
  Building wheel for mouseinfo (setup.py) ... done
  Created wheel for mouseinfo: filename=MouseInfo-0.1.3-py3-none-any.whl size=10910 sha256=8b1e36b8b9a91088c604f477009c58b5adb9bd3aaf35584721fdfa0411d37c71
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\43\9a\7f\373736bf37b94b358be41fb2f317a0f9940a1dcb7a733e1707
  Building wheel for pyperclip (setup.py) ... done
  Created wheel for pyperclip: filename=pyperclip-1.8.2-py3-none-any.whl size=11113 sha256=e46f86506aee7aac8cb8a6739df0a15cfadb463a5f394eb9b845c16259d12ff7
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\9f\18\84\8f69f8b08169c7bae2dde6bd7daf0c19fca8c8e500ee620a28
  Building wheel for pyrect (setup.py) ... done
  Created wheel for pyrect: filename=PyRect-0.2.0-py2.py3-none-any.whl size=11174 sha256=c9ccebfa186248be4588919a259ff67e428252065fa646b305d91147da5cffd0
  Stored in directory: c:\users\ANY_USER\appdata\local\pip\cache\wheels\a8\c4\b9\73048d5fa590952161184f5367220620d40958f3c0b8e8c03d
Successfully built pyautogui pygetwindow PyTweening mouseinfo pyperclip pyrect
Installing collected packages: PyTweening, pyrect, pyperclip, pygetwindow, mouseinfo, pyautogui
Successfully installed PyTweening-1.0.4 mouseinfo-0.1.3 pyautogui-0.9.53 pygetwindow-0.0.9 pyperclip-1.8.2 pyrect-0.2.0



$ python aaa.py
Traceback (most recent call last):
  File "aaa.py", line 6, in <module>
    import pyautogui
  File "C:\bin\Python37\lib\site-packages\pyautogui\__init__.py", line 221, in <module>
    locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__
AttributeError: module 'pyscreeze' has no attribute 'locateOnWindow'



https://github.com/asweigart/pyautogui/issues/598
sergiodantasz commented on 29 Jan
Hi Everyone! I hope everyone is doing well. It looks like there is an easy fix for this one.

pyautogui/pyautogui/__init__.py

Line 221 in 5e4acb8

 locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__ 
Here on this line we just need to change

locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__
To This:

locateOnWindow.__doc__ = pyscreeze.locateOnScreen.__doc__
Update this and your inputs will work. The locateOnWindow changed to locateOnScreen.

++@asweigart, FYI

Tested on: Windows Version	10.0.19042 Build 19042
Current Python:        3.9.2
Current PyAutoGUI:     0.9.53
The file location for me was: 'C:\Users`{UserName}`\AppData\Roaming\Python\Python39\site-packages\pyautogui*init*.py'

Do not look in the C:\Program Files\Python39 folders

VALEU PAI, SALVOU DEMAIS !! ESTAAMOS JUNTOS MEU REI ! EH NOIS

@BolisettySujith BolisettySujith mentioned this issue on 9 Feb
Improve README.md BolisettySujith/J.A.R.V.I.S#4
 Open
@abuzze
abuzze commented 13 days ago
You should update pyscreeze to at least 0.1.28. to fix this error.

pip3 install pyscreeze -U



$>>> C:\bin\Python37\Lib\site-packages\pyautogui
__init__.py  v0.9.53  221行目
    locateOnWindow.__doc__ = pyscreeze.locateOnWindow.__doc__
    locateOnWindow.__doc__ = pyscreeze.locateOnScreen.__doc__

