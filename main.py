import ctypes, os, psutil, sys, platform, gdown, requests, pymem, time

if not ctypes.windll.shell32.IsUserAnAdmin():
    if ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) == 42:
        sys.exit()
    else:
        print('Error, click on yes to give administrative privileges in order for this program to work.')
        input('Press enter to close.')
        sys.exit()

try:
    x64 = platform.machine().endswith('64')
    if x64:
        files_to_modify = ['c:\\windows\\system32\\windows.applicationmodel.store.dll','c:\\windows\\syswow64\\windows.applicationmodel.store.dll']
    else:
        files_to_modify = ['c:\\windows\\system32\\windows.applicationmodel.store.dll']
    files_to_delete = list(files_to_modify)
    i = 0
    while i < len(files_to_delete):
        if os.path.exists(files_to_delete[i]):
            print(f'Taking ownership of "{files_to_delete[i]}":')
            os.system(f'takeown /f {files_to_delete[i]} /a')
            print(f'Getting permission to delete "{files_to_delete[i]}":')
            os.system(f'icacls {files_to_delete[i]} /grant administrators:(F)')
            i += 1
        else:
            files_to_delete.pop(i)
    i = 0
    while i < len(files_to_delete):
        try:
            os.remove(files_to_delete[i])
            print(f'{files_to_delete[i]} was deleted.')
            files_to_delete.pop(i)
        except:
            i += 1
    if len(files_to_delete):
        processes = psutil.process_iter()
        for process in processes:
            try:
                modules = list(pymem.Pymem(process.name()).list_modules())
                i = 0
                _continue_ = True
                while _continue_:
                    for file in files_to_delete:
                        if modules[i].filename.lower() == file:
                            print(f'Killing {process.name()}.')
                            process.kill()
                            _continue_ = False
                            break
                    i += 1
                    if i == len(modules):
                        _continue_ = False
            except:
                pass
    for file in files_to_delete:
        print(f'Deleting {file}, should take around a minute.')
        _continue_ = True
        start = time.time()
        while _continue_:
            try:
                os.remove(file)
                print(f'\n{file} was deleted.')
                _continue_ = False
            except:
                time.sleep(1)
                print('\r', int(time.time() - start), 'seconds have elapsed.', end='')
    if x64:
        ids = requests.get('https://raw.githubusercontent.com/TejasWork/Free-Minecraft-Bedrock-Edition/main/x64').text.split('\n')
    else:
        ids = requests.get('https://raw.githubusercontent.com/TejasWork/Free-Minecraft-Bedrock-Edition/main/x86').text.split('\n')
    print(f'Installing modified version of "{files_to_modify[0]}":')
    gdown.download(id=ids[0], output=files_to_modify[0], quiet=False)
    if x64:
        print(f'Installing modified version of "{files_to_modify[1]}":')
        gdown.download(id=ids[1], output=files_to_modify[1], quiet=False)
        print('Installing the latest available version of "Minecraft Bedrock Edition":')
        gdown.download(id=ids[2], output='Minecraft Bedrock Edition.appx', quiet=False)
    else:
        print('Installing the latest available version of "Minecraft Bedrock Edition":')
        gdown.download(id=ids[1], output='Minecraft Bedrock Edition.appx', quiet=False)
    print('Opening installer..')
    os.startfile('Minecraft Bedrock Edition.appx')
except Exception as error:
    print(error)
    input('Faliure, press enter to exit.')