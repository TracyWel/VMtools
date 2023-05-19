import sys
from pyuac import main_requires_admin
import os
import subprocess


# @main_requires_admin(return_output=True)
def setup_upload_user(user_name, user_pw):
    print("setup_upload_user: Do stuff here that requires being run as an admin.")
    os.system('dir C:\\Users\\TracyTD')
    # command_str1 = f'net user /add {user_name} {user_pw} /passwordchg:no /passwordreq:yes'
    # os.system(command_str1)
    #
    # command_str2 = f'net localgroup sftp_users {user_name} /add'
    # os.system(command_str2)
    #
    # command_str3 = f'net localgroup users {user_name} /delete'
    # os.system(command_str3)
    input("Press enter to continue. >")


def setup_folder_structure(cust_folder):
    print("setup_folder_structure: Do stuff here that requires being run as an admin.")
    ps_execute_str = f'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'
    print(f'Ready to run Powershell commands with {ps_execute_str}')

    # ps_command_str1 = f'if ((Test-Path -Path "F:\\sftp\\{cust_folder}") ' \
    #                   f'-match $False) {{md F:\\sftp\\{cust_folder}}}'
    # subprocess.call(ps_command_str1, shell=True)
    #
    # ps_command_str2 = f'if ((Test-Path -Path "F:\\sftp\\{cust_folder}\\.log") ' \
    #                   f'-match $False) {{md F:\sftp\{cust_folder}\.log}}'
    # subprocess.call(ps_command_str2, shell=True)
    #
    # ps_command_str3 = f'if ((Test-Path -Path "Z:\\sftp\\{cust_folder}") ' \
    #                   f'-match $False) {{md Z:\\sftp\\{cust_folder}}'
    # subprocess.call(ps_command_str3, shell=True)

    input("Press enter to continue. >")


# @main_requires_admin(return_output=True)
def grant_upload_user_permissions(user_name, cust_folder):
    print("grant_upload_user_permissions: Do stuff here that "
          "requires being run as an admin.")
    os.system('dir C:\\Users\\TracyTD')

    # command_str4 = f'icacls "F:\\sftp\\{cust_folder}" /grant {user_name}:(OI)(CI)M /T'
    # os.system(command_str4)
    input("Press enter to close the window. >")


def setup_user_main():
    print('Please ender the customer upload name - usually something '
          'like upload_customername:')
    upload_name = input()

    print('Please ender the upload password - 20 plus letters and '
          'numbers (no special symbols):')
    upload_pw = input()

    print('Please ender the customer name for folder structure - '
          'usually somthing like Customername):')
    folder_name = input()

    setup_upload_user(upload_name, upload_pw)
    # rv = setup_upload_user(upload_name, upload_pw)
    # if not rv:
    #     print("I must have already been Admin!")
    # else:
    #     admin_stdout_str, admin_stderr_str, *_ = rv
    #     if "Do stuff" in admin_stdout_str:
    #         print("It worked.")

    setup_folder_structure(folder_name)

    grant_upload_user_permissions(upload_name, folder_name)
    # rv = grant_upload_user_permissions(upload_name, folder_name)
    # if not rv:
    #     print("I must have already been Admin!")
    # else:
    #     admin_stdout_str, admin_stderr_str, *_ = rv
    #     if "Do stuff" in admin_stdout_str:
    #         print("It worked.")


if __name__ == "__main__":
    setup_user_main()
