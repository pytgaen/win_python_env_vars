# Windows Environment Variables Manager 🛠️

A command-line tool to easily manage Windows environment variables, allowing you to handle both user and system variables.

## ✨ Features

- 📋 List all environment variables
- 🔍 Get the value of a specific variable
- ✏️ Set or update a variable
- 🗑️ Delete a variable
- 🔄 Manage PATH (add/remove directories)
- 👥 Support for both user and system variables (admin mode required for system variables)

## 📥 Installation

Not need.

## 📚 Usage

### 🔰 Basic Commands

```bash
# List all variables
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager list

# Get a variable
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager get VARIABLE_NAME

# Set a variable
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager set VARIABLE_NAME "value"

# Delete a variable
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager unset VARIABLE_NAME
```

### 🛣️ PATH Management

```bash
# Add a directory to PATH
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager add-to-path "C:\my\directory"

# Remove a directory from PATH
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager remove-from-path "C:\my\directory"

# Add local bin directory to user PATH
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager add-to-path "C:\Users\%USERNAME%\.local\bin"
```

### ⚙️ Global Options

- `--user`: Manage user environment variables (default)
- `--system`: Manage system environment variables (requires administrator rights)

### 💡 Examples

```bash
# List system variables
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager --system list

# Set a user variable
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager --user set MY_VAR "my_value"

# Get a variable (searches user variables first, then system)
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager get --auto JAVA_HOME

# Add local bin to PATH (useful for user-installed tools)
uvx --from git+https://github.com/pytgaen/win_python_env_vars win-env-manager --user add-to-path "C:\Users\%USERNAME%\.local\bin"
```

## 📋 Requirements

- 🪟 Windows (Windows 7 or higher)
- 🐍 Python 3.6 or higher

## 🔒 Security / Admin Note

Access to system environment variables requires administrator privileges. Make sure to run the program with appropriate rights when using the `--system` option.

## License

This project is licensed under the [GNU LGPLv3](./LICENSE). See the LICENSE file for more details.
