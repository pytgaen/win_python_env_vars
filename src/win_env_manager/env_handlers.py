# env_handlers.py
import winreg
import abc
import os


class BaseEnvHandler(metaclass=abc.ABCMeta):
    """Abstract base class for environment variable management"""

    @property
    @abc.abstractmethod
    def root_key(self):
        """Root registry key (HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE)"""
        pass

    @property
    @abc.abstractmethod
    def env_key_path(self):
        """Registry path to environment variables"""
        pass

    def list_vars(self):
        """List all environment variables"""
        env_vars = {}
        with winreg.OpenKey(self.root_key, self.env_key_path) as key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    env_vars[name] = value
                    i += 1
                except OSError:
                    break
        return env_vars

    def get_var(self, var_name, default=None):
        """Get a specific environment variable"""
        try:
            with winreg.OpenKey(self.root_key, self.env_key_path) as key:
                return winreg.QueryValueEx(key, var_name)[0]
        except FileNotFoundError:
            if default is None:
                raise
            return default

    def set_var(self, var_name, value):
        """Set or update an environment variable"""
        with winreg.OpenKey(
            self.root_key, self.env_key_path, 0, winreg.KEY_WRITE
        ) as key:
            winreg.SetValueEx(key, var_name, 0, winreg.REG_EXPAND_SZ, value)
        return True

    def unset_var(self, var_name):
        """Delete an environment variable"""
        try:
            with winreg.OpenKey(
                self.root_key, self.env_key_path, 0, winreg.KEY_WRITE
            ) as key:
                winreg.DeleteValue(key, var_name)
                return True
        except FileNotFoundError:
            return False
        except OSError as e:
            if e.winerror == 2:  # Variable non trouvée
                return False
            raise

    def add_to_path(self, directory):
        """Add directory to PATH if not present"""
        current_path = self.get_var("Path") or ""
        directories = current_path.split(";")

        directory_ = os.path.expandvars(directory)

        if directory_ not in directories:
            new_path = f"{current_path};{directory_}" if current_path else directory_
            self.set_var("Path", new_path)
            return True
        return False

    def remove_from_path(self, directory):
        """Remove directory from PATH if present"""
        current_path = self.get_var("Path") or ""
        directories = current_path.split(";")

        directory_ = os.path.expandvars(directory)

        if directory_ in directories:
            directories.remove(directory_)
            new_path = ";".join(filter(None, directories))
            self.set_var("Path", new_path)
            return True
        return False


class UserEnvHandler(BaseEnvHandler):
    """Handler for user-level environment variables"""

    @property
    def root_key(self):
        return winreg.HKEY_CURRENT_USER

    @property
    def env_key_path(self):
        return "Environment"


class SystemEnvHandler(BaseEnvHandler):
    """Handler for system-level environment variables (requires admin)"""

    @property
    def root_key(self):
        return winreg.HKEY_LOCAL_MACHINE

    @property
    def env_key_path(self):
        return r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
