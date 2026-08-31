---
okf_version: 0.2
type: documentation
title: "How-To: Deploy Sovereign Gitea via Rootless Podman & Quadlet"
timestamp: "2026-08-20T23:00:00Z"
topics: ["dsom", "how-to", "gitea", "podman", "quadlet", "gitops", "https"]
description: "Step-by-step instructions for standalone deployment of Gitea over HTTPS using rootless Podman pods and Podman 5 systemd Quadlets with automated web installation bypass."
resource: "file:///docs/how-to/install-gitea-podman-quadlet.md"
sources: ["https://linuxmalaysia.github.io/podman-elastic-stack-ai/GITEA_GUIDE/"]
generated: google-jules
verified: true
status: approved
stale_after: "2027-08-20T00:00:00Z"
---
# 🚀 How-To: Deploy Sovereign Gitea via Rootless Podman & Quadlet

This guide provides step-by-step instructions for deploying a standalone, self-hosted Gitea GitOps core natively on unprivileged rootless Podman infrastructure (using Podman Pods or systemd Quadlets) enforced over HTTPS.

---

## 1. Overview & Architecture

Gitea serves as the local "Sovereign" Source of Truth for all GitOps repositories and infrastructure-as-code.

### Architecture Specifications

* **Target Host / Domain:** `10.17.250.28` (or your host IP / FQDN)
* **Database Backend:** PostgreSQL 15 (Alpine)
* **Application Server:** Gitea 1.26.3
* **HTTP/HTTPS Port:** `3000` (Mapped to container port `3000` over HTTPS)
* **SSH Port:** `2222` (Mapped to container port `22` for Git over SSH)
* **Security & Protocol:** HTTPS enforced with TLS certificates signed by Sovereign CA.
* **Automated Installation Bypass:** The Gitea Web UI installer is bypassed programmatically via runtime environment variables (`GITEA__security__INSTALL_LOCK: "true"`).

---

## 2. Prerequisites

Before running any installation steps, verify the host system requirements:

1. **Enable User Linger:**
   Rootless container services run within unprivileged user space. Enabling linger ensures systemd user daemons and containers remain active across reboots and SSH session logouts:

   ```bash
   sudo loginctl enable-linger $(whoami)
   ```

2. **Verify Podman & Dependencies:**
   Confirm that Podman (v4+ or v5+) and Podman Compose are installed:

   ```bash
   podman --version
   podman-compose --version
   ```

---

## 3. Step-by-Step Installation Commands

### Step A: Generate TLS Certificates & Directory Setup

1. **Create Configuration and Certificate Directories:**

   ```bash
   mkdir -p ~/.config/gitea/certs
   chmod 0755 ~/.config/gitea/certs
   ```

2. **Generate Private Key and Self-Signed / Sovereign Certificate:**

   ```bash
   # Generate 2048-bit RSA Private Key with owner-only permissions (0600)
   openssl genrsa -out ~/.config/gitea/certs/gitea.key 2048
   chmod 0600 ~/.config/gitea/certs/gitea.key

   # Generate 5-year Self-Signed / Sovereign Certificate with Subject Alt Name (SAN)
   openssl req -new -x509 -key ~/.config/gitea/certs/gitea.key \
     -out ~/.config/gitea/certs/gitea.crt -days 1825 \
     -subj "/C=MY/ST=Kuala Lumpur/L=Kuala Lumpur/O=Sovereign/OU=IT/CN=10.17.250.28" \
     -addext "subjectAltName = DNS:10.17.250.28, IP:10.17.250.28, DNS:localhost, IP:127.0.0.1"
   chmod 0644 ~/.config/gitea/certs/gitea.crt
   ```

   > **Security & Rootless UID Mapping Note:** In rootless Podman, the invoking host user UID (e.g. 1000) maps to UID 0 (root) inside the container namespace, whereas Gitea runs internally as unprivileged user `git` (UID/GID 1000 inside container, mapped to host subuid range e.g. 100999).
   > Because of this namespace mapping, a host key file with mode `0600` owned by host UID 1000 is inaccessible to container UID 1000 unless permissions are `0644` or group permissions allow access (`chmod 0640` with appropriate group ownership).
   > If Gitea reports permission denied reading `gitea.key`, verify user mapping via `podman exec gitea-app id` or `podman exec gitea-stack-gitea-app id` and adjust `gitea.key` read permissions accordingly.

3. **Install Sovereign CA in Host Trust Store:**

   * **On Debian / Ubuntu:**

     ```bash
     sudo cp ~/.config/gitea/certs/gitea.crt /usr/local/share/ca-certificates/sovereign-gitea-ca.crt
     sudo update-ca-certificates
     ```

   * **On Red Hat / AlmaLinux / CentOS:**

     ```bash
     sudo cp ~/.config/gitea/certs/gitea.crt /etc/pki/ca-trust/source/anchors/sovereign-gitea-ca.crt
     sudo update-ca-trust
     ```

---

### Step B: Create Storage Volumes & Podman Pod

1. **Create Podman Pod with HTTP (3000) and SSH (2222) Port Mappings:**

   ```bash
   podman pod create \
       --name gitea-stack \
       --publish 3000:3000 \
       --publish 2222:22
   ```

2. **Create Storage Volumes:**

   ```bash
   podman volume create gitea_db_data
   podman volume create gitea_app_data
   ```

---

### Step C: Secure Secrets Management (`gitea.env`)

To prevent embedding plaintext credentials in CLI parameters or systemd unit files, generate a high-entropy password and store environment secrets in a strict `0600` file:

```bash
GITEA_SECURE_DB_PASS=$(openssl rand -base64 24)

cat <<EOF > gitea.env
POSTGRES_USER=gitea
POSTGRES_PASSWORD=${GITEA_SECURE_DB_PASS}
POSTGRES_DB=gitea
POSTGRES_MAX_CONNECTIONS=200
POSTGRES_SHARED_BUFFERS=256MB
POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
POSTGRES_MAINTENANCE_WORK_MEM=64MB
POSTGRES_WORK_MEM=16MB
GITEA__database__DB_TYPE=postgres
GITEA__database__HOST=127.0.0.1:5432
GITEA__database__NAME=gitea
GITEA__database__USER=gitea
GITEA__database__PASSWD=${GITEA_SECURE_DB_PASS}
GITEA__server__PROTOCOL=https
GITEA__server__DOMAIN=10.17.250.28
GITEA__server__ROOT_URL=https://10.17.250.28:3000/
GITEA__server__HTTP_PORT=3000
GITEA__server__SSH_PORT=2222
GITEA__server__SSH_LISTEN_PORT=22
GITEA__server__CERT_FILE=/etc/gitea/certs/gitea.crt
GITEA__server__KEY_FILE=/etc/gitea/certs/gitea.key
GITEA__security__INSTALL_LOCK=true
EOF
chmod 0600 gitea.env
```

---

### Step D: Deploy PostgreSQL Database Container

Deploy PostgreSQL 15 within the rootless pod:

```bash
podman run --detach \
    --name gitea-db \
    --pod gitea-stack \
    --restart always \
    --env-file gitea.env \
    --volume gitea_db_data:/var/lib/postgresql/data:Z \
    docker.io/library/postgres:15-alpine
```

---

### Step E: Deploy Gitea HTTPS Application Container

Deploy Gitea 1.26.3 with volume mounts for certificates (including `:ro,Z` for SELinux relabeling), application data, and timezone:

```bash
podman run --detach \
    --name gitea-app \
    --pod gitea-stack \
    --restart always \
    --env-file gitea.env \
    --volume gitea_app_data:/data:Z \
    --volume ~/.config/gitea/certs:/etc/gitea/certs:ro,Z \
    --volume /etc/localtime:/etc/localtime:ro \
    docker.io/gitea/gitea:1.26.3
```

---

### Step F: Systemd Quadlet & Unit File Integration

To manage the standalone stack via user-level systemd:

#### Option 1: Podman Native Systemd Generation

```bash
mkdir -p ~/.config/systemd/user/
cd ~/.config/systemd/user/
podman generate systemd --name gitea-stack --files --new
systemctl --user daemon-reload
systemctl --user enable --now pod-gitea-stack.service
```

#### Option 2: Podman 5 Native Quadlet Kube (`gitea-stack.kube` & `gitea-stack.yaml`)

1. Create `~/.config/containers/systemd/gitea-stack.kube`:

   ```ini
   [Unit]
   Description=Gitea GitOps Service (Podman Kube Quadlet)
   After=network-online.target

   [Kube]
   Yaml=gitea-stack.yaml
   PublishPort=3000:3000
   PublishPort=2222:22

   [Install]
   WantedBy=default.target
   ```

2. Create `~/.config/containers/systemd/gitea-stack.yaml` with mode `0600` (substituting `${HOME}` for your target user home path):

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     labels:
       app: gitea-stack
     name: gitea-stack
   spec:
     containers:
       - name: gitea-db
         image: docker.io/library/postgres:15-alpine@sha256:4770281b16c891e4a6828551a37c22e4eb24eb20755b38031d27976192ddf39f
         args:
           - -c
           - max_connections=200
           - -c
           - shared_buffers=256MB
           - -c
           - effective_cache_size=1GB
           - -c
           - maintenance_work_mem=64MB
           - -c
           - work_mem=16MB
         env:
           - name: POSTGRES_USER
             value: gitea
           - name: POSTGRES_PASSWORD
             value: "<GENERATE_HIGH_ENTROPY_DB_PASSWORD>"
           - name: POSTGRES_DB
             value: gitea
           - name: POSTGRES_MAX_CONNECTIONS
             value: "200"
           - name: POSTGRES_SHARED_BUFFERS
             value: "256MB"
           - name: POSTGRES_EFFECTIVE_CACHE_SIZE
             value: "1GB"
           - name: POSTGRES_MAINTENANCE_WORK_MEM
             value: "64MB"
           - name: POSTGRES_WORK_MEM
             value: "16MB"
         volumeMounts:
           - mountPath: /var/lib/postgresql/data
             name: gitea-db-data

       - name: gitea-app
         image: docker.io/gitea/gitea:1.26.3@sha256:f232490d16d1ff86ea562ba76a6b8762d02c8eb1608ebcfecaa8f3df9df30b42
         ports:
           - containerPort: 3000
             hostPort: 3000
           - containerPort: 22
             hostPort: 2222
         env:
           - name: GITEA__database__DB_TYPE
             value: postgres
           - name: GITEA__database__HOST
             value: 127.0.0.1:5432
           - name: GITEA__database__NAME
             value: gitea
           - name: GITEA__database__USER
             value: gitea
           - name: GITEA__database__PASSWD
             value: "<GENERATE_HIGH_ENTROPY_DB_PASSWORD>"
           - name: GITEA__server__PROTOCOL
             value: https
           - name: GITEA__server__DOMAIN
             value: "10.17.250.28"
           - name: GITEA__server__ROOT_URL
             value: "https://10.17.250.28:3000/"
           - name: GITEA__server__HTTP_PORT
             value: "3000"
           - name: GITEA__server__SSH_PORT
             value: "2222"
           - name: GITEA__server__SSH_LISTEN_PORT
             value: "22"
           - name: GITEA__server__CERT_FILE
             value: /etc/gitea/certs/gitea.crt
           - name: GITEA__server__KEY_FILE
             value: /etc/gitea/certs/gitea.key
           - name: GITEA__security__INSTALL_LOCK
             value: "true"
         volumeMounts:
           - mountPath: /data
             name: gitea-app-data
           - mountPath: /etc/gitea/certs
             name: gitea-certs
             readOnly: true
           - mountPath: /etc/localtime
             name: etc-localtime
             readOnly: true

     volumes:
       - name: gitea-db-data
         persistentVolumeClaim:
           claimName: gitea_db_data
       - name: gitea-app-data
         persistentVolumeClaim:
           claimName: gitea_app_data
       - name: gitea-certs
         hostPath:
           path: /home/{{ ansible_user }}/.config/gitea/certs
           type: Directory
       - name: etc-localtime
         hostPath:
           path: /etc/localtime
           type: File
   ```

3. Reload systemd user daemon and start Quadlet service:

   ```bash
   systemctl --user daemon-reload
   systemctl --user start gitea-stack.service
   ```

---

## 4. Post-Installation Account, Token & Repository Setup (CLI & API)

Once Gitea is active over HTTPS on port 3000, perform initial administrative setup programmatically using `podman exec` (Gitea CLI) and `curl` (Gitea API).

### A. Create Admin Account via Gitea CLI

Execute user creation directly inside the container. Note that under manual Podman Pod deployment the container is named `gitea-app`, whereas under Quadlet Kube deployment Podman names the container `gitea-stack-gitea-app`:

```bash
read -sp "Enter Gitea Admin Password: " GITEA_ADMIN_PASS

# For Podman CLI Pod deployment:
podman exec -u git gitea-app gitea admin user create \
    --username dsom-admin \
    --password "${GITEA_ADMIN_PASS}" \
    --email admin@dsom.local \
    --admin

# For Quadlet Kube deployment (gitea-stack-gitea-app):
# podman exec -u git gitea-stack-gitea-app gitea admin user create --username dsom-admin --password "${GITEA_ADMIN_PASS}" --email admin@dsom.local --admin
```

### B. Create Access Token & Organisation via API

To prevent exposing credentials in process listings or command history, pass authentication via a mode-0600 `curl` config file (`~/.gitea-auth-config`):

```bash
# Prepare secure 0600 curl config file
cat <<EOF > ~/.gitea-auth-config
user = "dsom-admin:${GITEA_ADMIN_PASS}"
EOF
chmod 0600 ~/.gitea-auth-config

# 1. Create route-scoped setup token
curl -s --cacert ~/.config/gitea/certs/gitea.crt --config ~/.gitea-auth-config \
     -X POST "https://10.17.250.28:3000/api/v1/users/dsom-admin/tokens" \
     -H "Content-Type: application/json" \
     -d '{"name": "setup-token", "scopes": ["write:org", "write:repository", "write:user"]}' > token_resp.json

# Remove authentication config file immediately
rm -f ~/.gitea-auth-config

# Extract token and token ID for subsequent requests
GITEA_TOKEN=$(grep -o '"sha1":"[^"]*' token_resp.json | cut -d'"' -f4)
GITEA_TOKEN_ID=$(grep -o '"id":[^,]*' token_resp.json | cut -d':' -f2)
rm -f token_resp.json

# 2. Create Organisation using Access Token
curl -s --cacert ~/.config/gitea/certs/gitea.crt -X POST "https://10.17.250.28:3000/api/v1/orgs" \
     -H "Authorization: token ${GITEA_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"username": "songketmailsdnbhd-group", "visibility": "public"}'

# 3. Create Repository under Organisation
curl -s --cacert ~/.config/gitea/certs/gitea.crt -X POST "https://10.17.250.28:3000/api/v1/orgs/songketmailsdnbhd-group/repos" \
     -H "Authorization: token ${GITEA_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"name": "um-elastic-soc", "private": false}'
```

### C. Register Host SSH Public Key (Port 2222) & Revoke Token

```bash
# 1. Prepare JSON payload containing public key
cat <<EOF > ssh-key-payload.json
{
  "title": "node-admin-key",
  "key": "$(cat ~/.ssh/id_dsom_ed25519.pub)",
  "read_only": false
}
EOF

# 2. Upload key via Gitea API
curl -s --cacert ~/.config/gitea/certs/gitea.crt -X POST "https://10.17.250.28:3000/api/v1/user/keys" \
     -H "Authorization: token ${GITEA_TOKEN}" \
     -H "Content-Type: application/json" \
     -d @ssh-key-payload.json
rm -f ssh-key-payload.json

# 3. Revoke temporary setup token
curl -s --cacert ~/.config/gitea/certs/gitea.crt -X DELETE "https://10.17.250.28:3000/api/v1/users/dsom-admin/tokens/${GITEA_TOKEN_ID}" \
     -H "Authorization: token ${GITEA_TOKEN}"
unset GITEA_TOKEN GITEA_ADMIN_PASS GITEA_TOKEN_ID

# 4. Verify SSH fingerprint out-of-band before appending to known_hosts
ssh-keygen -lf <(ssh-keyscan -p 2222 10.17.250.28 2>/dev/null)
# Verify output fingerprint matches host admin key, then append:
ssh-keyscan -p 2222 10.17.250.28 >> ~/.ssh/known_hosts
```

---

## 5. Git Remote & Client Access (HTTPS & SSH)

### HTTPS Setup

```bash
# Trust Sovereign CA in Git
git config --global http.sslCAInfo ~/.config/gitea/certs/gitea.crt

# Add remote and push
git remote add sovereign "https://10.17.250.28:3000/songketmailsdnbhd-group/um-elastic-soc.git"
git push sovereign main
```

### SSH Setup (Port 2222)

```bash
# Add SSH remote pointing to mapped port 2222
git remote add gitea ssh://git@10.17.250.28:2222/songketmailsdnbhd-group/um-elastic-soc.git

# Fetch and Push
git fetch gitea
git push gitea main
```

---

## 6. Maintenance & Troubleshooting

### Service Status & Logs

Support commands cover both systemd unit names (`pod-gitea-stack.service` for generated systemd, `gitea-stack.service` for Quadlet Kube):

```bash
# Check service status (Generated systemd or Quadlet Kube)
systemctl --user status pod-gitea-stack.service
systemctl --user status gitea-stack.service

# View live container logs
journalctl --user -u pod-gitea-stack.service -f
journalctl --user -u gitea-stack.service -f

# Restart active service
systemctl --user restart pod-gitea-stack.service
systemctl --user restart gitea-stack.service
```

### Troubleshooting: "Permission Denied" Reading `gitea.key`

If Gitea container fails to read key permissions on startup, check user namespace identity via `podman exec gitea-app id` or `podman exec gitea-stack-gitea-app id`:

```bash
# Ensure readable permissions for host user session
chmod 0644 ~/.config/gitea/certs/gitea.crt
chmod 0644 ~/.config/gitea/certs/gitea.key

systemctl --user daemon-reload
systemctl --user restart gitea-stack.service
```

### Decommissioning & Cleanup

To ensure neither Option 1 nor Option 2 remains active after cleanup, stop and disable both unit names:

```bash
# Stop and disable both possible service unit instances
systemctl --user disable --now pod-gitea-stack.service 2>/dev/null || true
systemctl --user disable --now gitea-stack.service 2>/dev/null || true

# Remove unit and Quadlet manifest files
rm -f ~/.config/systemd/user/*gitea-stack*
rm -f ~/.config/containers/systemd/*gitea-stack*
systemctl --user daemon-reload

# Remove containers, pods, and storage volumes
podman pod rm -f gitea-stack 2>/dev/null || true
podman volume rm gitea_db_data gitea_app_data 2>/dev/null || true
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
