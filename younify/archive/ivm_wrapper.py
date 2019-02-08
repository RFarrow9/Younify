# Wrapper for E-WorkBook Inventory APIs. Written against version 10.3.3.
# Version 0.1.0

import requests
import json
import pandas
import urllib3
import math

urllib3.disable_warnings()

s = None
root_url = None
debug = True

domain_list = ["equipment", "material", "sample"]


class IvmSession:
    def __init__(self, server, username, password, verify=False):
        endpoint = "/apilogin"
        url = server + endpoint
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}
        data = {"username": username, "password": password}

        r = requests.post(url, headers=headers, data=data, verify=verify)
        r.raise_for_status()

        token = r.headers['X-AUTH-TOKEN']
        token = "Bearer " + token

        if debug:
            print(token)

        session = requests.Session()
        session.headers.update({"Authorization": token,
                                "Accept": "application/json",
                                "Content-Type": "application/json"})
        session.verify = verify

        global s
        global root_url

        s = session
        root_url = server


class IvmTypeConfig:
    # todo: change this so it's more like IvmSession, and can be accessed anywhere. That way, it could be
    # todo: refreshed from any other class.
    """Class for configuration of types in one domain, as returned by Inventory."""
    def __init__(self):
        self.types_array = []

        for domain in domain_list:
            url = root_url + "/rest/v1/" + domain + "/physical/meta"
            r = s.get(url)
            r.raise_for_status()

            for type_dict in r.json()["types"]:
                self.types_array.append(type_dict)

    def types(self):
        object_array = []
        for type_dict in self.types_array:
            object_array.append(IvmType(type_dict["name"], type_dict["domain"]))
        return object_array

    def type_names(self):
        results_array = []
        for type_dict in self.types_array:
            results_array.append(type_dict["name"])
        return results_array

    def get_custom_attributes(self, ivm_type):  # TODO: This does nothing. Also, should this not be a type method?
        for type_dict in self.types_array:
            if type_dict["name"] == ivm_type.name:
                print("yep")


class IvmListElement:
    """Base class for attributes/methods common to the elements of Inventory's list configuration (Group, List etc).
    The purpose is to provide the methods to build the massive json document required to update the Lists configuration.
    Sub-classes contain the configuration required to use these methods and, occasionally, methods which are specific
    to that element-type."""
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.parent_array_label = ""
        self.name_label = ""
        self.json = {}

    def get_element(self):
        """Search for an element by its label (or name) and update the object's json attribute from the default blank
        template. Use this if you don't want to just overwrite everything."""
        for element_dict in self.parent.json[self.parent_array_label]:
            if element_dict[self.name_label] == self.name:
                self.json = element_dict
            else:
                pass

    def add_child(self, child_object):
        """Adds child json to parent. If the child is already present under parent, it will be overwritten."""
        found = False
        new_list = []
        for old_element_dict in self.json[child_object.parent_array_label]:
            if child_object.name == old_element_dict[child_object.name_label]:
                new_list.append(child_object.json)
                found = True
            else:
                new_list.append(old_element_dict)
        if not found:
            new_list.append(child_object.json)
        self.json[child_object.parent_array_label] = new_list


class IvmListConfig(IvmListElement):
    """Sub-class for the configuration as returned by Inventory. Only inherits IvmListElement class to make use of
    the save function."""
    def __init__(self, name=None, parent=None):
        super(IvmListConfig, self).__init__(name, parent)

        url = root_url + "/rest/v1/settings/lists"

        r = s.get(url)
        r.raise_for_status()

        self.json = r.json()

    def add_list(self, new_list):
        """Uses attributes of a NewList object to update the IVM lists configuration json. Appends to lists rather
        than overwriting."""
        custom = new_list.custom
        subgroup = new_list.subgroup
        group = new_list.group
        values = new_list.values

        if custom:
            group_object = IvmGroup(group, self)
            group_object.get_element()

            if subgroup:
                parent = IvmSubGroup(subgroup, group_object)
                parent.get_element()
            else:
                parent = group_object

            new_list.parent = parent
            new_list.get_element()

            new_list.add_values(values)

            parent.add_child(new_list)
            if subgroup:
                group_object.add_child(parent)
                self.add_child(group_object)
            else:
                self.add_child(parent)
        else:
            new_list.parent = self
            new_list.get_element()

            new_list.add_values(values)

            self.add_child(new_list)

    def get_values(self, list_name):  # TODO: Re-write this method. It is an atrocity. It's also case-sensitive.
        """Searches for named list and returns an array of the child values. An empty array is returned if the list
        has no child values or does not exist."""
        for group_dict in self.json["customListGroups"]:
            group_object = IvmGroup(group_dict["groupName"], self)
            group_object.get_element()  # TODO: Should get element just be in the init? That would make parent mandatory

            list_object = IvmList(list_name, parent=group_object)
            list_object.get_element()
            values = list_object.get_values()
            if len(values) != 0:
                return values

            for subgroup_dict in group_object.json["subGroups"]:
                subgroup_object = IvmSubGroup(subgroup_dict["groupName"], parent=group_object)
                subgroup_object.get_element()

                list_object = IvmList(list_name, parent=subgroup_object)
                list_object.get_element()
                values = list_object.get_values()
                if len(values) != 0:
                    return values

        list_object = IvmList(list_name, parent=self, custom=False)
        list_object.get_element()
        values = list_object.get_values()
        return values

    def save(self):
        """Saves edited configuration back to Inventory."""
        url = root_url + "/rest/v1/settings/lists"
        data = json.dumps(self.json)

        r = s.put(url, data=data)
        r.raise_for_status()

        print(r.status_code)


class IvmGroup(IvmListElement):
    """IvmListElement subclass for List Group elements."""
    def __init__(self, name, parent):
        super(IvmGroup, self).__init__(name, parent)
        self.parent_array_label = "customListGroups"
        self.name_label = "groupName"
        self.json = {'subGroups': [], 'groupName': self.name, 'lists': []}


class IvmSubGroup(IvmListElement):
    """IvmListElement subclass for Sub Group elements."""
    def __init__(self, name, parent):
        super(IvmSubGroup, self).__init__(name, parent)
        self.parent_array_label = "subGroups"
        self.name_label = "groupName"
        self.json = {'subGroups': [], 'groupName': self.name, 'lists': []}


class IvmList(IvmListElement):
    """IvmListElement subclass for List elements. Not to be confused with the NewList class. IvmList is used to
    construct the json required to save back to Inventory."""
    def __init__(self, name, values=None, group=None, subgroup=None, parent=None, custom=True):
        super(IvmList, self).__init__(name, parent)
        assert len(self.name) < 41
        self.name_label = "name"
        self.values = values
        self.group = group
        self.subgroup = subgroup
        self.custom = custom
        if custom:  # TODO: Should probably double-check I'm meant to remove these spaces.
            self.parent_array_label = "lists"
            self.json = {"listId": self.name.replace(" ", ""), "options": [], "type": "CUSTOM", "name": self.name}
        else:
            self.parent_array_label = "flexibleSystemLists"
            self.json = {"listId": self.name.replace(" ", ""), "options": [], "type": "SYSTEM_FLEXIBLE",
                         "name": self.name}

    def get_order(self):
        """List values have an associated index value. This returns the index of the final item plus one. (or zero,
        indicating an empty list."""
        order = 0
        for value_dict in self.json["options"]:
            if value_dict["order"] > order:
                order = value_dict["order"]
        return order + 1

    def add_values(self, values):  # TODO: used by IvmListConfig.add_list() should this be private?
        """Builds value dictionaries from list of value... um... values and appends them to self.json"""
        if values is not None:
            for value in values:
                value_object = IvmValue(value, self)
                value_object.get_element()
                if value_object.json["order"] == 0:
                    order = self.get_order()
                    value_object.json["order"] = order
                self.add_child(value_object)

    def get_values(self):  # todo: should this be private?
        """Return values already present in self.json. This is used by the IvmListConfig.get_values"""
        results_array = []
        for value_dict in self.json["options"]:
            results_array.append(value_dict["value"])

        return results_array


class IvmValue(IvmListElement):
    """IvmListElement subclass for List Value elements."""
    def __init__(self, name, parent):
        super(IvmValue, self).__init__(name, parent)
        self.parent_array_label = "options"
        self.name_label = "value"
        self.json = {"order": 0, "@tag": "EnumeratedListOption", "value": name}


class IvmType:
    """Class describing Ivm Type configuration."""
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.attributes = []

        self.json = self.get_json()

    def get_json(self):
        types = IvmTypeConfig()
        for type_dict in types.types_array:
            if type_dict["name"] == self.name:
                return type_dict
        return {"name": self.name,
                "description": "null",
                "attributes": [],
                "label": "null",
                "valid": "true",
                "domain": self.domain}

    def add_attribute(self, attribute_object):  # TODO: Attribute labels need to be unique.
        """Add an attribute object to the parent Type so the attribute can be saved to Inventory."""
        self.attributes.append(attribute_object)
        self.json["attributes"].append(attribute_object.json)

    def create(self):
        """Creates type from object json. Fails if type already exists."""
        if self.exists():
            print("Type already exists: " + self.name)  # todo: throw an exception? I dunno.
        else:
            self.save()

    def save(self):
        """Updates type configuration, overwriting what's already there."""
        url = root_url + "/rest/v1/" + self.domain + "/virtual/meta/type"

        data = json.dumps(self.json)

        r = s.put(url, data=data)
        r.raise_for_status()

        print(r.status_code)

    def exists(self):
        """Checks Inventory for types with the same name."""
        return bool(self.name in IvmTypeConfig().type_names())


class IvmAttribute:
    """Class describing IVM Type Attribute configuration."""
    def __init__(self, name, field_type, item_specific, required, list_id):
        self.name = name
        self.field_type = field_type
        self.item_specific = item_specific
        self.required = required
        self.json = {"fieldType": field_type,
                     "itemSpecific": item_specific,
                     "required": required,
                     "label": name}

        if field_type == "select":
            self.json["listIds"] = list_id


class IvmItem:
    def __init__(self, item_dict):
        self.id = item_dict["system"]["uniqueId"]
        self.record = item_dict["system"]["virtualUid"]
        self.type = item_dict["system"]["recordType"]
        self.guid = item_dict["system"]["guid"]
        self.name = item_dict["core"]["printName"]
        self.created_by = item_dict["system"]["createdBy"]
        self.domain = item_dict["system"]["domain"]
        self.json = item_dict

    def get_attributes(self, attribute_group="core"):  # todo: I don't like the format of this. (thing/attribute)
        attribute_group_list = self.json.keys()
        attributes = []
        for group in attribute_group_list:
            if group == attribute_group or attribute_group == "all":
                attribute_list = self.json[group].keys()
                for attribute in attribute_list:
                    attributes.append(group + "/" + attribute)

        return attributes

    def edit_attribute(self, attribute, value):
        attribute_path_array = attribute.split("/")
        self.json[attribute_path_array[0]][attribute_path_array[1]] = value

        # Some items have this sourceEntity field which points to the E-WorkBook entity where the item was initially
        # registered. If that entity is subsequently deleted, the sourceEntity field contains a dictionary with an
        # error message. Trying to save an item containing that error dictionary causes Inventory to respond with a 500.
        # Since this field should never need to be updated, I'm just going to delete it, and handle the key error for
        # items which were created in Inventory itself, and therefore don't have a sourceEntity.
        try:
            del self.json["system"]["sourceEntity"]
        except KeyError:
            pass

    def save(self):
        url = root_url + "/rest/v1/" + self.domain + "/physical/" + self.guid
        save_json = self.json
        save_json["version"] = save_json["system"]["version"]
        del save_json["system"]["version"]
        data = json.dumps(save_json)

        print(data)

        r = s.put(url, data=data)
        r.raise_for_status()

        self.json = r.json()

    def delete(self):
        """This function will delete the item, any associated links, and any aliquot items split off it."""
        url = root_url + "/rest/v1/" + self.domain + "/physical/" + self.guid

        self.delete_links()

        r = s.delete(url)
        r.raise_for_status()

    def delete_links(self):
        """Deletes all child aliquots and all component links."""
        splits = self.links(link_type="Split", relationship="parent")
        for split in splits:
            split.child.delete()
        components = self.links(link_type="Component", relationship="all")
        for component in components:
            component.delete()

    def links(self, link_type="all", relationship="all"):
        return IvmLinkSearch(self.id, link_type=link_type, relationship=relationship).links


class IvmLink:
    def __init__(self, config):
        self.json = config
        self.guid = config["id"]
        self.id = config["uniqueId"]
        self.parent = item_from_id(config["attributes"]["parent"])
        self.child = item_from_id(config["attributes"]["child"])
        self.type = config["attributes"]["type"]

    def delete(self):
        if self.type == "Split":
            print("As this link is a split aliquot, the child item will be deleted - not just the link.")
            self.child.delete()
        else:
            url = root_url + "/rest/v1/links/delete"
            data = [self.id]
            data = json.dumps(data)

            r = s.post(url, data=data)
            r.raise_for_status()


class IvmLinkSearch:
    def __init__(self, item_id, link_type="all", relationship="all"):
        """Returns an array of link objects for given item id."""
        self.link_types = []
        self.search_id = item_id
        self.total_pages = 0

        # TODO: Do I need to have an 'if not in' to check for invalid options? Also is this scalable?
        if link_type == "Split" or link_type == "all":
            self.link_types.append("Split")
        if link_type == "Component" or link_type == "all":
            self.link_types.append("Component")

        link_dicts = []

        if relationship == "parent" or relationship == "all":
            links_to_children = self._get_links("parent")
            for x in links_to_children:
                link_dicts.append(x)
        if relationship == "child" or relationship == "all":
            links_to_parents = self._get_links("child")
            for x in links_to_parents:
                link_dicts.append(x)

        self.links = []
        for x in link_dicts:
            link_object = IvmLink(x)
            self.links.append(link_object)

    def _get_links(self, relationship):
        url = root_url + "/rest/v1/links/query"
        s.params = {"itemUid": self.search_id, "linkTypes": self.link_types, "relationship": relationship}

        r = s.get(url)
        r.raise_for_status()

        return r.json()


class IvmItemSearch:
    def __init__(self, domain, search_term="", date_field=None, start_date=None, end_date=None, location=None):
        self.url = root_url + "/rest/v1/" + domain + "/physical/query"
        self.item_filter = []

        if location is None:
            location = []

        if date_field is not None:
            if start_date is None and end_date is None:  # TODO: assert start_date or end_date is not None ???
                print("Must supply at least one date for date query.")  # TODO: Should I start raising errors for this stuff
                date_filter = ""  # TODO: Yes.
            elif start_date != end_date and end_date is None:
                date_filter = {date_field: [{"gte": start_date}, {"lte": start_date}]}
            elif start_date != end_date and start_date is None:
                date_filter = {date_field: [{"gte": end_date}, {"lte": end_date}]}
            elif start_date == end_date:
                date_filter = {date_field: [{"gte": end_date}, {"lte": end_date}]}
            else:
                date_filter = {date_field: [{"gte": start_date}, {"lte": end_date}]}

            self.item_filter.append(date_filter)

        self.data = {"location": location,
                     "filter": [],
                     "itemFilter": self.item_filter,
                     "defaultFiltersOn": "true",
                     "text": search_term}

        self.data = json.dumps(self.data)

    def count(self):
        result_dict = self._get_items(page=0, size=1)
        count = result_dict["page"]['totalPages']

        return count

    def get_items(self, max_results=None, size=5):
        result_array = []
        result_dict = self._get_items()
        total_pages = result_dict["page"]["totalPages"]

        if max_results is None:
            for x in range(total_pages):
                result_dict = self._get_items(page=x)
                for y in result_dict["items"]:
                    result_array.append(y)
        else:
            total_pages = int(math.ceil(max_results/size))
            remainder = max_results % size
            if remainder == 0:
                page_offset = 0
            else:
                page_offset = 1

            for x in range(total_pages - page_offset):
                result_dict = self._get_items(page=x, size=size)
                for y in result_dict["items"]:
                    result_array.append(y)

            result_dict = self._get_items(page=total_pages - page_offset, size=size)
            for x in range(remainder):
                print("x = " + str(x))
                result_array.append(result_dict["items"][x])

        item_array = []
        for x in result_array:
            item = IvmItem(x)
            item_array.append(item)

        return item_array

    def _get_items(self, page=0, size=5):
        s.params = {"page": page, "size": size}

        r = s.post(self.url, data=self.data)
        r.raise_for_status()

        return r.json()


def types_from_dataframe(df):
    """Allows IvmType and IvmAttribute objects to be initialised en masse from a data-frame with the following fields:
    Type Name, Attribute Name, Field Type, Item Specific, Required, Domain, List ID"""
    type_list = list(set(df["Type Name"]))
    results_array = []

    for type_name in type_list:
        type_df = df.loc[df["Type Name"] == type_name]
        domain = list(type_df["Domain"])[0].lower()

        type_object = IvmType(type_name, domain)

        attribute_list = list(type_df["Attribute Name"])
        attribute_set = list(set(type_df["Attribute Name"]))
        if len(attribute_list) != len(attribute_set):
            print("You have duplicate attributes for type: " + type_name)
            print("Script will exit so you can correct this.")
            raise SystemExit

        for attribute_name in attribute_list:
            attribute_df = type_df.loc[type_df["Attribute Name"] == attribute_name]
            field_type = list(attribute_df["Field Type"])[0]
            item_specific = list(attribute_df["Item Specific"])[0]
            required = list(attribute_df["Required"])[0]
            list_id = list(attribute_df["List ID"])  # This has to be an array. TODO: Add capability for multiple lists.

            attribute_object = IvmAttribute(attribute_name, field_type, item_specific, required, list_id)
            type_object.add_attribute(attribute_object)

        results_array.append(type_object)

    return results_array


def lists_from_dataframe(df):
    """Allows NewList objects to be initialised en masse from a data-frame with the following fields: List Group,
    Sub Group, List, Value."""
    df.fillna(value=0, inplace=True)
    results_array = []
    list_list = list(set(df["List"]))
    for list_name in list_list:
        list_df = df.loc[df["List"] == list_name]
        list_values = list(list_df["Value"])
        group = list(set(list_df["List Group"]))
        subgroup = list(set(list_df["Sub Group"]))
        custom = list(set(list_df["Custom"]))
        if len(group) > 1 or len(subgroup) > 1:
            print("Configuration error. Separate lists cannot have the same name, "
                  "and lists cannot be assigned to multiple groups.")
            print("Skipping " + list_name)
            continue
        elif len(custom) > 1:
            print("A list can be custom or not. Make up your mind.")
            print("Skipping " + list_name)
            continue
        else:
            group = group[0]
            subgroup = subgroup[0]
            custom = custom[0]

        list_object = IvmList(list_name, values=list_values, group=group, subgroup=subgroup, custom=custom)

        results_array.append(list_object)

    return results_array


def item_from_id(item_id):
    url = root_url + "/rest/v1/inventory/physical/" + item_id
    r = s.get(url)
    r.raise_for_status()

    item = IvmItem(r.json())
    return item


def main():
    """Running as main allows you to use a test config file (list_config.csv) referenced below and review
    the resulting json. It also demonstrates usage."""
    server = "https://10.134.66.112:8483"
    IvmSession(server, "mkennedy", "password")

    def lists():
        ivm_lists = IvmListConfig()

        lists_df = pandas.read_csv("list_config.csv")
        list_list = lists_from_dataframe(lists_df)

        for x in list_list:
            ivm_lists.add_list(x)

        print(ivm_lists.json)

        ivm_lists.save()

    def types():
        types_df = pandas.read_csv("type_config.csv")
        types_list = types_from_dataframe(types_df)

        for type_object in types_list:
            type_object.create()

    lists()
    types()


if __name__ == "__main__":
    main()
