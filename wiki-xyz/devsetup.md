# System Setup and Configuration

**Table of Contents:**

- [Mamba Install](#mamba-install)
- [ZSH Configs](#zsh-configs)
- [SSH Configs](#ssh-configs)
  - [Config Examples](#config-examples)
- [GIT Configs](#git-configs)
  - [Password Access](#password-access)
  - [SSH Access](#ssh-access)
- [Package Setup](#package-setup)
  - [Python Poetry](#python-poetry)
- [Jupyter Setup](#jupyter-setup)
  - [IPyKernels](#ipykernels)
    - [Bash Kernel](#bash-kernel)
    - [R Kernel (IRkernel)](#r-kernel-irkernel)
- [Custom Terminal](#custom-terminal)
  - [Conda Default](#conda-default)
  - [PathSet Alias](#pathset-alias)
  - [Bash Prompt](#bash-prompt)
  - [-ZSH Prompt](#-zsh-prompt)
  - [Source Commands](#source-commands)
- [VSCode Setups](#vscode-setups)
  - [VSCode-R Setup](#vscode-r-setup)
  - [VSCode-Tunnel Setup](#vscode-tunnel-setup)
  - [Cursor-Tunnel Setup](#cursor-tunnel-setup)
- [RStudio Setup](#rstudio-setup)
  - [Plugin Guides](#plugin-guides)
- [Server-Side](#server-side)
  - [PHP Setup](#php-setup)
- [Linux Command](#linux-command)
  - [Users + Passwords](#users--passwords)
- [Other Tools + Apps](#other-tools--apps)
  - [Quarto Setup](#quarto-setup)
  - [Ollama Setup](#ollama-setup)
  - [Replit REPL SSH](#replit-repl-ssh)

## Mamba Install

Download and install (Mamba)Conda via [Miniforge](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)

```shell
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

A general good set of defaults for `.condarc` or `.mambarc`:

```yaml
channels:
  - conda-forge
auto_activate_base: true
```

## ZSH Configs

```shell
sudo apt install zsh
```

(In VSCode, the relevant setting would become:`<br>`  `"terminal.integrated.defaultProfile.linux": "zsh"`)

## SSH Configs

Make SSH Public / Private Key Pair, and add public key to remote machines.

```shell
ssh-keygen -t rsa
ssh-copy-id user@remotehost
```

When connecting to remote instances (e.g. VSCode servers), be sure to specify publickey, as preferred login.

### Config Examples

Multiple machines, single aliases, with GSSAPI:

```ssh
Host *.portal.from.edu
   User colinconwell
   GSSAPIDelegateCredentials yes
   PreferredAuthentications gssapi-with-mic,publickey

Host machine1
    HostName machine1.portal.from.edu

Host machine2
    HostName machine2.portal.from.edu
```

One machine, multiple aliases, with public key:

```ssh
Host bigram bigboi hefty
  User colinconwell
    HostName 142.623.52.636
    # ControlPersist yes
    # IdentityFile ~/.ssh/ssids/id_ed25519
    PreferredAuthentications publickey,password
```

## GIT Configs

### Password Access

Password is now a personal access token, which can be accessed by navigating to github.com, then... `<br>`  `Settings > Developer Settings > Personal Access Tokens`

(Alternatively, with the right cookies in place, you might just be able to [click this link](https://github.com/settings/tokens).)

After generating a token, use the following command to store your credentials the next time they are required:

```shell
git config --global credential.helper store
```

You can also store your credentials manually using 1 of 2 methods:

**Method 1**: **File Storage**

First, create a `~/.git-credentials` file in the same directory where `.git` is located. Then, add the following line:

```text
https://<username>:<personal_access_token>@github.com
```

**Method 2**: RC Preference

You can also store your GIT credentials as environment variables in your `.bashrc` or `.zshrc` preference file with the added lines:

```shell
export GITHUB_USERNAME="your_github_username"
export GITHUB_TOKEN="your_personal_access_token"
```

### SSH Access

(Main reference [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/).)

To access GitHub via SSH, first generate a new SSH key pair associated with your GitHub account:

```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Then, add the SSH key (in `id_ed25519.pub`) to your GitHub account:

github.com > `Settings > SSH and GPG keys > New SSH key`

Next, add the following to your `.ssh/config` file:

```ssh
Host github.com
    IdentityFile ~/.ssh/id_ed25519
```

Finally, when cloning repositories, be sure to specify the SSH URL:

```shell
git clone git@github.com:username/repository.git
```


## Package Setup

More to be written here, but [python poetry](https://python-poetry.org/) seems to be the most promising on this front.

### Python Poetry

Poetry can be installed in a virtual environment as follows:

```shell
pip install poetry
```

After an initial build (`poetry build`), version updates can be made as follows:

```shell
poetry version patch  # for small updates
poetry version minor  # for new features
poetry version major  # for breaking changes
```

Poetry requires the presence of a `pyproject.toml` file. Example for a GitHub-hosted package:

```toml
[tool.poetry]
name = "package_name"
version = "0.1.0"
description = "A Library for the Art of Programming"
authors = ["Colin Conwell <colinconwell@gmail.com>"]
readme = "README.md"
packages = [{include = "package_name"}]

[tool.poetry.dependencies]
python = "^3.7"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

If you want to publish the package to PyPi (with an account), run `poetry publish`

## Jupyter Setup

```shell
mamba create --name jupyter python=3.11 pip
mamba activate jupyter
pip install --upgrade jupyterlab
```

Optionally, add Jupyter-AI:

```shell
pip install --upgrade jupyterlab jupyter_ai jupyter_ai_magics
```

### IPyKernels

Want to use an environment you've created in a jupyter notebook?

First, make sure `ipykernel` is installed in your environment:

```shell
mamba install ipykernel # or pip install ipykernel
```

Then, add the kernel (replacing `myenv`) to your specs by running:

```shell
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

You can see the list of installed kernels with the command:

```shell
jupyter kernelspec list
```

You can uninstall a given kernel with the command:

```shell
jupyter kernelspec remove myenv
```

#### Bash Kernel

```shell
pip install bash_kernel
python -m bash_kernel.install
```

#### R Kernel (IRkernel)

(If using R in an R session....)

```r
install.packages("IRkernel")
IRkernel::installspec(name='ir', displayname='R')
```

(Outside of an R session....)

```shell
conda install -c conda-forge r-irkernel
```

## Custom Terminal

### Conda Default

```shell
# >>> activate default conda >>>
DEFAULT_CONDA_ENV="workspace"

if [[ -z "$CONDA_DEFAULT_ENV" ]]; then
    conda activate "$DEFAULT_CONDA_ENV"; fi

ENV1=$CONDA_DEFAULT_ENV"
ENV2=$DEFAULT_CONDA_ENV"

if [[ ENV1 != ENV2 ]]; then
    conda activate "$DEFAULT_CONDA_ENV"; fi
```

### PathSet Alias

```shell
# >>> path names alias >>>
WORKZONE="/home/coco/workzone"
NICKNAME="remote-machine-tag"
ENVSETUP="$WORKZONE/environment"
```

### Bash Prompt

```shell
PS1='\[\e[32m\]($DEFAULT_CONDA_ENV)\[\e[0m\] \[\e[36m\]\u@$NICKNAME\[\e[0m\] \w \$ '
```

### -ZSH Prompt

```zsh
PROMPT='$(CONDA_DEFAULT_ENV) %F{cyan}%n@$NICKNAME%f ${${(%):-%~}%/} %# '
```

(To include the trailing slash, simply use `%~` instead of `${(%):-%~}`)

Alternatively, if custom prompts are defined:

```zsh
PROMPT='$(conda_prompt) %F{cyan}%n@%m%f $(custom_path) %# '
```

### Source Commands

```shell
script="$ENVSETUP/Easy-Shell.sh"

# if script exists, source it:
if [[ -f "$script" ]]; then
    source "$script"; fi
```

## VSCode Setups

### VSCode-R Setup

**References:**

- https://docs.posit.co/ide/desktop-pro/1.3.881-1/remote-desktop.html
- https://github.com/REditorSupport/vscode-R/issues/584
- https://cran.r-project.org/web/packages/ssh/vignettes/intro.html

### VSCode-Tunnel Setup

Main instructions [here](https://code.visualstudio.com/docs/remote/tunnels).
Download options [here](https://code.visualstudio.com/#alt-downloads).

1. Install Code CLI:

```shell
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
```

OR (if you have sudo access)...

```shell
sudo snap install code --classic
```

2. TMUX or Screen a session and in that session, run:

```shell
code tunnel --name your_tunnel_name
```

Note that the name will default to the hostname of the machine you're connecting from.

3. To keep the tunnel alive persistently, run:

```shell
code tunnel service install
```

### Cursor-Tunnel Setup

Install the Cursor CLI. Then, apply the rest of the VSCode-Tunnel instructions above, replacing `code` with `cursor`.

(Uninstall):

```shell
code tunnel service uninstall
cone tunnel unregister
```

## RStudio Setup

### Plugin Guides

- https://github.com/daattali/addinslist
- Recommended Plugins:
  - ggedit
  - citr
  - esquisse

## Server-Side

### PHP Setup

```shell
brew install php composer
```

**Intellisense (Lint)**

Configure IDE to use stubs (e.g. for pgSQL): [github.com/JetBrains/phpstorm-stubs](https://github.com/JetBrains/phpstorm-stubs)

## Linux Command

### Users + Passwords

To add a new user and set their password:

```shell
sudo adduser username
sudo passwd username
```

To change a user's password (as admin):

```shell
sudo passwd username
```

To login as a different user:

```shell
su - username
```

## Other Tools + Apps

Generally speaking, it's a good idea to set up some folder in your \$PATH that contains executables (e.g. `/your_name/storage/exectuables`).

### Quarto Setup

To install quarto on a remote machine (without sudo), use [this method](https://nbdev.fast.ai/getting_started.html):

(After [downloading Quarto](https://quarto.org/docs/get-started/) to a location of your choice...)

```shell
dpkg -x quarto*.deb .
mv opt/quarto ./
rmdir opt
mkdir -p ~/.local/bin
ln -s "$(pwd)"/quarto/bin/quarto ~/.local/bin
```

### Ollama Setup

See [this link](https://ollama.com/download/linux) for typical setups.

For remote installations without sudo (needed only for startup service), use [this method](https://github.com/ollama/ollama/blob/main/docs/linux.md#manual-install) (without prepending sudo).

### Replit REPL SSH

A guide to setting up SSH keys for Replit REPLs can be found [here](https://docs.replit.com/replit-workspace/ssh).

```shell
ssh-keygen -t ed25519 -f ~/.ssh/replit -q -N ""
```
