from pyuac import main_requires_admin
import os
import subprocess


@main_requires_admin(return_output=True)
def setup_upload_user(user_name, user_pw):
    """
    Executes Windows CMD shell commands to create and set permissions
    for an upload user.
    :param user_name: the upload user name
    :param user_pw: the upload user password
    :return: none
    """

    print("setup_upload_user: Create upload user.")
    # os.system('dir C:\\Users\\TracyTD')
    command_str1 = f'net user /add {user_name} {user_pw} /passwordchg:no /passwordreq:yes'
    os.system(command_str1)

    command_str2 = f'net localgroup sftp_users {user_name} /add'
    os.system(command_str2)

    command_str3 = f'net localgroup users {user_name} /delete'
    os.system(command_str3)
    input("Press enter to continue. >")


def setup_folder_structure(cust_folder):
    """
    Creates the necessary upload and backup folder structures by executing
    Powershell commands.
    :param cust_folder: Customer name to be used for folder structure
    :return: none
    """

    print("setup_folder_structure: Creating upload and backup folder structures.")
    ps_execute_str = f'C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'
    print(f'Ready to run Powershell commands with {ps_execute_str}')

    ps_command_str1 = f'if ((Test-Path -Path "F:\\sftp\\{cust_folder}") ' \
                      f'-match $False) {{md F:\\sftp\\{cust_folder}}}'
    subprocess.call(ps_command_str1, shell=True)

    ps_command_str2 = f'if ((Test-Path -Path "F:\\sftp\\{cust_folder}\\.log") ' \
                      f'-match $False) {{md F:\\sftp\\{cust_folder}\.log}}'
    subprocess.call(ps_command_str2, shell=True)

    ps_command_str3 = f'if ((Test-Path -Path "Z:\\sftp\\{cust_folder}") ' \
                      f'-match $False) {{md Z:\\sftp\\{cust_folder}}}'
    subprocess.call(ps_command_str3, shell=True)

    input("Press enter to continue. >")


@main_requires_admin(return_output=True)
def grant_upload_user_permissions(user_name, cust_folder):
    """
    Grants permission for the upload user to write to the upload folder
    using Windows CMD commands.
    :param user_name:
    :param cust_folder:
    :return:
    """

    print("grant_upload_user_permissions: Allowing upload user to write"
          "to upload folder.")
    # os.system('dir C:\\Users\\TracyTD')

    command_str4 = f'icacls "F:\\sftp\\{cust_folder}" /grant {user_name}:(OI)(CI)M /T'
    os.system(command_str4)

    input("Press enter to close the window. >")


def print_instructions():
    """
    Prints out instructions for the user to complete tasks that cannot
    be automated here.
    :return: none
    """

    print(
        """
        \n\n Next Steps\n
        =========\n\n
        To setup SSH access for uploads do the following:\n
        1.  Open the CopSSH control panel and perform the following steps.\n
        2.	On the Users tab, click the Add button.\n
        3.	On the first page of the CopSSH user activation page, click the Forward button.\n
        4.	On the user page, select the new upload_customer account you created. Click Forward.\n
        5.	On the select options page, change access type to SFTP.\n
        6.	On the select options page, for home directory enter the path created in step 2 (Create local folders for customer) above. For example, F:\sftp\[Customer]. \n
        7.	On the select options page, verify the 3 checks boxes are selected, click Forward.\n
        8.	On the confirm activation page, click Apply.\n
        
        =========\n\n
        
        For customers uploading with PWC FAST the public key needs to be placed in the right location\n
        Go to an existing FAST customer folder eg. F:\sftp\Toll\.ssh and copy the two files (authorized_keys and id_rsa.pub)\n
        and put them in F:\sftp\[Customer]\.ssh\n
        """
    )
    print(
        """
        =========\n\n
        If you have made a mistake and wish to remove an upload user, type\n
        net user "user name" /delete\n

        If that doesn't work, type\n
        net user "user name" /delete /domain\n
        
        You may delete folders and files in both the F and Z drives manually.
        """
    )


def setup_user_main():
    """
    Partially automates the user upload set up process on the TD virtual
    machine using a few bits of information
    :return: none
    """

    print('Please enter the customer upload name - usually something '
          'like upload_customername:')
    upload_name = input()

    print('Please enter the upload password - 20 plus upper- and lower-case'
          'letters and numbers (no special symbols):')
    upload_pw = input()

    print('Please enter the customer name for folder structure - '
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

    print_instructions()


if __name__ == "__main__":
    setup_user_main()
