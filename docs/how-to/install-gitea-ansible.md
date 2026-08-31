---
okf_version: 0.2
type: documentation
title: "How-To: Deploy Sovereign Gitea via Automated Ansible Playbook"
timestamp: "2026-08-20T23:00:00Z"
topics: ["dsom", "how-to", "gitea", "ansible", "playbook", "gitops", "https"]
description: "Step-by-step instructions for automated deployment of Gitea over HTTPS using rootless Podman and Ansible playbooks with high-entropy credential vaulting and 5-year TLS certificate generation."
resource: "file:///docs/how-to/install-gitea-ansible.md"
sources: ["https://linuxmalaysia.github.io/podman-elastic-stack-ai/GITEA_GUIDE/"]
generated: "google-jules"
verified: true
status: "approved"
stale_after: "2027-08-20T00:00:00Z"
---

# 🛠️ How-To: Deploy Sovereign Gitea via Automated Ansible Playbook

This guide details how to automate the standalone deployment of a self-hosted Gitea GitOps stack over rootless Podman using Ansible playbooks. The workflow handles OS dependencies, linger enablement, secret vaulting, 5-year Sovereign TLS certificate generation, Quadlet systemd unit deployment, and installation screen bypass automatically.

---

## 1. Overview & Architecture

Using Ansible for deployment guarantees idempotent, reproducible infrastructure provisioning.

### Key Architecture Specs

* **Default Domain / Host IP:** `10.17.250.28` (or target inventory host)
* **Database Backend:** PostgreSQL 15 (Alpine)
* **Application Server:** Gitea 1.26.1
* **HTTP/HTTPS Port:** `3000` (Mapped to container port `3000` over HTTPS)
* **SSH Port:** `2222` (Mapped to container port `22` for Git over SSH)
* **Security & TLS:** TLS certificates generated via `community.crypto` and signed by Sovereign CA.
* **Automated Bypass:** Bypasses web installation screen programmatically (`GITEA__security__INSTALL_LOCK: "true"`).

---

## 2. Prerequisites & Ansible Setup

Ensure Ansible and required collection packages are installed on the control node:

```bash
# Install required Ansible collections for Podman and Crypto tasks
ansible-galaxy collection install containers.podman community.crypto community.general
```

Verify target inventory connectivity:

```bash
ansible -i inventory/hosts.yml target_hosts -m ping
```

---

## 3. Ansible Role & Playbook Structure

The deployment relies on Ansible role variables and task definitions:

### Role Defaults (`roles/gitea/defaults/main.yml`)

```yaml
gitea_domain: "localhost"
gitea_root_url: "https://localhost:3000/"
gitea_http_port: 3000
gitea_ssh_port: 2222
gitea_db_password: "dSoM_G1t3a_H@rd3n3d_99X"
```

### Main Task Execution Flow (`roles/gitea/tasks/main.yml`)

```yaml
- name: Generate and deploy TLS certificates
  ansible.builtin.import_tasks: tls.yml

- name: Ensure Quadlet directory exists
  ansible.builtin.file:
    path: ~/.config/containers/systemd/
    state: directory
    mode: '0755'

- name: Deploy Gitea Kube Quadlet (YAML & Kube)
  ansible.builtin.template:
    src: "{{ item }}.j2"
    dest: "~/.config/containers/systemd/{{ item }}"
    mode: '0644'
  loop:
    - gitea-stack.yaml
    - gitea-stack.kube
  notify: reload systemd user daemon

- name: Reload systemd user daemon for Quadlet generation
  ansible.builtin.shell: systemctl --user daemon-reload
  changed_when: false

- name: Ensure Gitea service is enabled and started
  ansible.builtin.systemd:
    name: gitea-stack.service
    state: started
    enabled: yes
    scope: user
    daemon_reload: yes
```

### Sovereign TLS Task Automation (`roles/gitea/tasks/tls.yml`)

```yaml
- name: Ensure local certs directory exists
  ansible.builtin.file:
    path: "{{ playbook_dir }}/../vault/generated"
    state: directory
    mode: '0700'
  delegate_to: localhost
  run_once: true
  become: false

- name: Generate Gitea private key
  community.crypto.openssl_privatekey:
    path: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.key"
    size: 2048
  delegate_to: localhost
  become: false

- name: Generate Gitea CSR
  community.crypto.openssl_csr:
    path: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.csr"
    privatekey_path: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.key"
    common_name: "{{ inventory_hostname }}"
    subject_alt_name:
      - "IP:{{ ansible_host }}"
      - "DNS:{{ inventory_hostname }}"
  delegate_to: localhost
  become: false

- name: Sign Gitea certificate with Sovereign CA
  community.crypto.x509_certificate:
    path: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.crt"
    csr_path: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.csr"
    ownca_path: "{{ playbook_dir }}/../vault/dsom-elasticsearch-ca.crt"
    ownca_privatekey_path: "{{ playbook_dir }}/../vault/dsom-elasticsearch-ca.key"
    provider: ownca
    ownca_not_after: "+1825d"
  delegate_to: localhost
  become: false

- name: Ensure target cert directory exists
  ansible.builtin.file:
    path: "~/.config/gitea/certs"
    state: directory
    mode: '0755'
  become: false

- name: Deploy Sovereign CA certificate
  ansible.builtin.copy:
    src: "{{ playbook_dir }}/../vault/dsom-elasticsearch-ca.crt"
    dest: "~/.config/gitea/certs/ca.crt"
    mode: '0644'
  become: false

- name: Deploy Gitea certificate
  ansible.builtin.copy:
    src: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.crt"
    dest: "~/.config/gitea/certs/gitea.crt"
    mode: '0644'
  become: false

- name: Deploy Gitea key
  ansible.builtin.copy:
    src: "{{ playbook_dir }}/../vault/generated/{{ inventory_hostname }}-gitea.key"
    dest: "~/.config/gitea/certs/gitea.key"
    mode: '0600'
  become: false

- name: Install Sovereign CA to Host Trust Store
  ansible.builtin.copy:
    src: "{{ playbook_dir }}/../vault/dsom-elasticsearch-ca.crt"
    dest: /usr/local/share/ca-certificates/sovereign-ca.crt
    mode: '0644'
  become: true
  become_user: root
  notify: update ca-certificates
```

---

## 4. Playbook Execution Commands

### Deploy Locally on Active Host

```bash
ansible-playbook playbooks/dsom/setup_gitea.yml
```

### Deploy Remote Host Inventory

```bash
ansible-playbook -i inventory/hosts.yml playbooks/dsom/setup_gitea.yml -e "target_hosts=gitea_production_nodes"
```

### Deploy Using Ansible Vault for Encrypted Passwords

```bash
ansible-playbook -i inventory/hosts.yml playbooks/dsom/setup_gitea.yml --ask-vault-pass
```

---

## 5. Post-Deployment Verification

Verify that Gitea systemd service and containers are active on target host:

```bash
# Verify systemd user service status
systemctl --user status gitea-stack.service

# Verify podman containers are running
podman pod ps
podman ps
```

---

## 6. Securing Secrets in Ansible & Git (Best Practices)

1. **Ansible Vault:** Always store database and admin credentials in encrypted vault files (`ansible-vault create`).
2. **Dynamic Ingestion:** Use `lookup('ansible.builtin.env', 'GITEA_DB_PASSWORD')` for runtime terminal injection.
3. **Repository Exclusions:** Confirm `.gitignore` includes `*.env`, `*credentials.txt`, and private key files (`*.key`).

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
