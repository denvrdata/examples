# Understanding SSH and Best Practices for Secure Access

As a cloud hosting provider, we frequently encounter situations where users lose access to their virtual machines (VMs) due to mismanagement of SSH keys or improper file permissions. This blog aims to shed light on SSH, its importance, and best practices to ensure uninterrupted and secure access to your machines.

## What is SSH?
Secure Shell (SSH) is a cryptographic network protocol that provides a secure way to access remote systems over an unsecured network. It is widely used for managing servers, virtual machines, and network devices. SSH ensures confidentiality, integrity, and authentication by encrypting the communication between the client and the server.

## How Does SSH Work?
SSH operates on a client-server model. Here's a quick breakdown:
1.	**Client-Server Communication:** A user (client) initiates a connection request to a remote machine (server) running an SSH daemon.
2.	**Authentication:** The server authenticates the client using a combination of username and either a password or an SSH key.
3.	**Secure Session:** Once authenticated, a secure session is established, allowing the user to execute commands, transfer files, or perform administrative tasks.

## The Role of SSH Keys
SSH keys are a pair of cryptographic keys (private and public) used for authentication:
1. **Private Key:** Stored securely on your local machine. Never share this key.
2. **Public Key:** Uploaded to the `~/.ssh/authorized_keys` file on the server. The server uses this to validate your private key.

This method is more secure than password authentication because keys are harder to crack and eliminate the need to transmit sensitive information like passwords over the network.

## Why Permissions Matter
Permissions on your SSH keys and related files are crucial for security. Incorrect permissions can lead to vulnerabilities or authentication failures.

•	**Private Key:** Must have restricted access (e.g., `chmod 600 ~/.ssh/id_rsa`).

•	**Public Key:** Can have more permissive access but should still be controlled.

•	**Authorized Keys File:** Ensure it is properly secured (e.g., `chmod 600 ~/.ssh/authorized_keys`).

Improper permissions can result in your keys being accessible to unauthorized users, compromising your access and the security of the VM.

## Common Scenarios Leading to Lost Access
1.	**Lost SSH Key:** Misplacing the private key file.
2.	**Changed Permissions:** Altering permissions on `~/.ssh` or `authorized_keys` inadvertently.
3.	**Modified Authorized Keys:** Overwriting or accidentally deleting entries in the `authorized_keys` file.

## How to Prevent Losing Access
1.	**Backup Your Keys:** Always keep a backup of your private key in a secure location.
2.	**Use a Password Manager:** Store and manage SSH keys securely using tools like 1Password or LastPass.
3.	**Set Correct Permissions:**
    - Private key: `chmod 600 ~/.ssh/id_rsa`
    - Public key: `chmod 644 ~/.ssh/id_rsa.pub`
    - .ssh directory: `chmod 700 ~/.ssh`
4.	**Restrict Access:** Limit who can access your private key. Ensure your local machine is secure.
5.	**Audit Regularly:** Periodically review and clean up the authorized_keys file to remove unused or obsolete keys.

## Regaining Access to a VM
If you lose access to your VM due to SSH issues, contact support. If self-service options fail, reach out to your cloud provider for assistance.
However, if your SSH key is lost, permissions are incorrect, or the authorized_keys file has been modified and no backup or console access is available, you will permanently lose access to your VM or container. This is why it is critical to follow best practices and maintain backups of your keys.

## Best Practices for Keeping SSH Secure
1.	**Use Key-Based Authentication:** Avoid password-based SSH logins entirely.
2.	**Disable Root Login:** Prevent direct root access by disabling it in the SSH configuration file (/etc/ssh/sshd_config).
3.	**Keep SSH Updated:** Regularly update SSH software to patch vulnerabilities.
4.	**Use SSH Agent:** Manage your private keys securely in memory using an SSH agent like ssh-agent or gpg-agent.
5.	**Rotate Keys Periodically:** Generate new keys periodically and update them on all authorized servers.


## Final Remarks
SSH is the backbone of secure access to your cloud-hosted infrastructure. By understanding how SSH works and following best practices, you can minimize risks, prevent losing access, and maintain seamless connectivity to your VMs. At Denvr Dataworks, we are committed to empowering users with the tools and knowledge to manage their systems securely and efficiently.

For more tips and support, explore our [documentation](https://docs.denvrdata.com/docs) or contact our team. Your security is our priority!

