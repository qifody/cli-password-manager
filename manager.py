from security import (
    generate_salt,
    hash_password,
    verify_password,
    derive_key,
    encrypt_data,
    decrypt_data,
)

from logger import log_event


class PasswordManager:
    def __init__(self, storage):
        self.logfile = "data/app.log"
        self.storage = storage

        self._vault = None
        self._key = None

        self.is_authenticated = False
        self.failed_attempts = 0


    def login(self, password):

        if self.failed_attempts >= 3:
            log_event("LOGIN_BLOCKED", self.logfile)
            return False

        data = self.storage.load()

        # ---------- FIRST RUN ----------
        if "master_hash" not in data:

            log_event("VAULT_CREATED", self.logfile)

            salt = generate_salt()
            hashed_password = hash_password(password, salt)

            self._key = derive_key(password, salt)

            self._vault = {"entries": {}}

            encrypted_vault = encrypt_data(self._vault, self._key)

            new_data = {
                "master_hash": hashed_password,
                "salt": salt,
                "vault": encrypted_vault
            }

            self.storage.save(new_data)

            self.is_authenticated = True
            return True


        # ---------- NORMAL LOGIN ----------

        salt = data["salt"]
        stored_hash = data["master_hash"]

        if verify_password(password, stored_hash, salt):

            log_event("LOGIN_SUCCESS", self.logfile)

            self._key = derive_key(password, salt)

            decrypted_vault = decrypt_data(data["vault"], self._key)

            self._vault = decrypted_vault

            self.is_authenticated = True
            self.failed_attempts = 0

            return True

        else:

            log_event("LOGIN_FAILED", self.logfile)

            self.failed_attempts += 1
            return False


    def _check_auth(self):
        if not self.is_authenticated:
            raise PermissionError("User not authenticated")


    def _save_vault(self):

        encrypted_vault = encrypt_data(self._vault, self._key)

        data = self.storage.load()

        new_data = {
            "master_hash": data["master_hash"],
            "salt": data["salt"],
            "vault": encrypted_vault
        }

        self.storage.save(new_data)


    def add_entry(self, site, username, password):

        self._check_auth()

        if site in self._vault["entries"]:
            raise ValueError("Site already registered")

        self._vault["entries"][site] = {
            "username": username,
            "password": password,
        }

        self._save_vault()

        log_event(f"ENTRY_ADDED {site}", self.logfile)


    def get_entry(self, site):

        self._check_auth()

        if site not in self._vault["entries"]:
            raise KeyError("Entry not found")

        log_event(f"ENTRY_REQUESTED {site}", self.logfile)

        return self._vault["entries"][site]


    def delete_entry(self, site):

        self._check_auth()

        if site not in self._vault["entries"]:
            raise KeyError("Entry not found")

        del self._vault["entries"][site]

        self._save_vault()

        log_event(f"ENTRY_DELETED {site}", self.logfile)


    def list_entries(self):

        self._check_auth()

        log_event("ENTRY_LISTED", self.logfile)

        return list(self._vault["entries"].keys())