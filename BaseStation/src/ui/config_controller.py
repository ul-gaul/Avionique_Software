SECTION_HEADER_KEY = "__section_header__"
OTHER_SECTION = "__others__"
RESERVED_WORDS = [SECTION_HEADER_KEY, OTHER_SECTION]


class ConfigController:
    def __init__(self, chemin_fichier):
        self.data = {
            "sections": [],
            "unarranged": [],
            OTHER_SECTION: []
        }
        self.settings_data = {OTHER_SECTION: []}
        self.file_path = chemin_fichier
        with open(chemin_fichier, "r") as f:
            sections = self.parse_fichier(f.read())
            for section in sections:
                section_name = None
                for name, value in section:
                    if name == SECTION_HEADER_KEY:
                        section_name = self.add_section(value)
                        continue
                    self.add_setting(name, value, section_name)
        self.arrange_sections()

    def save_to_file(self):
        with open(self.file_path, "w") as f:
            for item in self.generer_texte_fichier():
                f.write(item)

    def set_value(self, section, name, value):
        self.settings_data[section][self.data[section].index(name)]["value"] = value

    def get_value(self, section, name):
        return self.settings_data[section][self.data[section].index(name)]["value"]

    def cancel(self):
        self.close()

    def get_sections(self):
        return self.data["sections"]

    def get_settings(self, section_name=None):
        try:
            return self.settings_data[section_name]
        except KeyError:
            return []

    def get_setting_value(self, name):
        for section_name in self.data["sections"]:
            try:
                return self.get_value(section_name, name)
            except ValueError:
                continue

    @staticmethod
    def _infer_type(value_str):
        pass

    def add_section(self, section_name):
        original_name = section_name
        n = 2
        # generate unique section name
        while section_name in self.data["sections"]:
            section_name = "{}#{}".format(original_name, n)
            n += 1
        self.data["sections"].append(section_name)
        return section_name

    def add_setting(self, name, value, section_name):
        self.data["unarranged"].append({"section": section_name, "name": name, "value": value})

    def arrange_sections(self):
        # put settings in suitable section
        for setting in self.data["unarranged"]:
            if setting["section"] is None:
                self.data[OTHER_SECTION].append(setting["name"])
                self.settings_data[OTHER_SECTION].append(setting)
            else:
                try:
                    self.data[setting["section"]].append(setting["name"])
                    self.settings_data[setting["section"]].append(setting)
                except KeyError:
                    self.data[setting["section"]] = [setting["name"]]
                    self.settings_data[setting["section"]] = [setting]
        self.data["unarranged"] = []
        # remove empty sections
        for section_name in self.data["sections"]:
            try:
                if not self.data[section_name]:
                    self.data["sections"].remove(section_name)
            except KeyError:
                self.data["sections"].remove(section_name)
        # last section is always __others__
        self.data["sections"].append(OTHER_SECTION)

    def generer_texte_fichier(self):
        for section_name in self.data["sections"]:
            if section_name in RESERVED_WORDS:
                continue
            yield ("[{}]\n".format(section_name) +
                   "\n".join("{} = {}".format(setting["name"], setting["value"])
                             for setting in self.settings_data[section_name]) +
                   "\n\n")

    def parse_fichier(self, corpsFichier: str):
        sections = corpsFichier.split("[")
        if len(sections) > 1:
            for section in sections[1:]:
                yield self.parse_section(section)

    @staticmethod
    def parse_section(sectionStr: str):
        section_tokens = sectionStr.split("\n")
        section_header = section_tokens[0].strip("]\n") if section_tokens[0].find("]") > -1 else ""
        yield SECTION_HEADER_KEY, section_header
        for row in section_tokens[1:]:
            items = [t.strip(" \n") for t in row.split("=") if t]
            if len(items) > 1:
                name, value = items[0], items[1]
                yield name, value
