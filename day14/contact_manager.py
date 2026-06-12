"""Contact Management System — Week 2 mini-project.

A command-line contact manager that combines the core Week 2 Python
concepts: a dict for storage, sets for tags, lists for notes,
comprehensions for search, one function per operation, and JSON for
persistence with error handling.

Data model:
    contacts = {
        contact_id (int): {
            "name": str,
            "phone": str,
            "email": str,
            "tags": set[str],
            "notes": list[str],
        },
        ...
    }
"""

import json


def add_contact(contacts, name, phone, email, tags=None, notes=None):
    """Add a new contact and return its generated id.

    Args:
        contacts (dict): Store to add to (modified in place).
        name (str): Contact full name.
        phone (str): Phone number.
        email (str): Email address.
        tags (set[str], optional): Initial tags. Defaults to empty.
        notes (list[str], optional): Initial notes. Defaults to empty.

    Returns:
        int: The id assigned to the new contact.

    Example:
        >>> store = {}
        >>> add_contact(store, "Ali", "0300", "ali@x.com")
        1
    """
    new_id = max(contacts.keys(), default=0) + 1
    contacts[new_id] = {
        "name": name,
        "phone": phone,
        "email": email,
        "tags": set(tags) if tags else set(),
        "notes": list(notes) if notes else [],
    }
    return new_id


def search_contacts(contacts, query):
    """Find contacts whose name, phone, or email contains a query.

    Uses a dict comprehension with a case-insensitive partial match.

    Args:
        contacts (dict): The contact store.
        query (str): Substring to look for.

    Returns:
        dict: Matching {id: record} pairs.

    Example:
        >>> store = {1: {"name": "Ali", "phone": "0300",
        ...               "email": "ali@x.com", "tags": set(),
        ...               "notes": []}}
        >>> list(search_contacts(store, "ali"))
        [1]
    """
    q = query.lower()
    return {
        cid: rec
        for cid, rec in contacts.items()
        if q in rec["name"].lower()
        or q in rec["phone"].lower()
        or q in rec["email"].lower()
    }


def update_contact(contacts, contact_id, **fields):
    """Update one or more fields of an existing contact.

    Args:
        contacts (dict): The contact store.
        contact_id (int): Id of the contact to update.
        **fields: Field names mapped to new values (name, phone,
            email).

    Returns:
        bool: True if updated, False if the id was not found.

    Example:
        >>> store = {1: {"name": "Ali", "phone": "0300",
        ...               "email": "a@x.com", "tags": set(),
        ...               "notes": []}}
        >>> update_contact(store, 1, phone="0311")
        True
    """
    if contact_id not in contacts:
        return False
    for key, value in fields.items():
        if key in ("name", "phone", "email"):
            contacts[contact_id][key] = value
    return True


def delete_contact(contacts, contact_id):
    """Delete a contact by id.

    Args:
        contacts (dict): The contact store.
        contact_id (int): Id to remove.

    Returns:
        bool: True if deleted, False if the id was not found.
    """
    if contact_id in contacts:
        del contacts[contact_id]
        return True
    return False


def add_tag(contacts, contact_id, tag):
    """Add a tag to a contact using a set operation.

    Args:
        contacts (dict): The contact store.
        contact_id (int): Target contact id.
        tag (str): Tag to add.

    Returns:
        bool: True if added, False if the id was not found.
    """
    if contact_id not in contacts:
        return False
    contacts[contact_id]["tags"].add(tag)
    return True


def remove_tag(contacts, contact_id, tag):
    """Remove a tag from a contact using a set operation.

    Args:
        contacts (dict): The contact store.
        contact_id (int): Target contact id.
        tag (str): Tag to remove (ignored if absent).

    Returns:
        bool: True if the id exists, False otherwise.
    """
    if contact_id not in contacts:
        return False
    contacts[contact_id]["tags"].discard(tag)
    return True


def find_by_tag(contacts, tag):
    """Return all contacts that carry a given tag.

    Args:
        contacts (dict): The contact store.
        tag (str): Tag to filter by.

    Returns:
        dict: Matching {id: record} pairs.

    Example:
        >>> store = {1: {"name": "Ali", "phone": "", "email": "",
        ...               "tags": {"work"}, "notes": []}}
        >>> list(find_by_tag(store, "work"))
        [1]
    """
    return {
        cid: rec for cid, rec in contacts.items()
        if tag in rec["tags"]
    }


def get_statistics(contacts):
    """Compute summary statistics for the contact store.

    Args:
        contacts (dict): The contact store.

    Returns:
        dict: Keys "total" (int) and "top_tags" (list of
            (tag, count) tuples, most common first).

    Example:
        >>> store = {1: {"name": "A", "phone": "", "email": "",
        ...               "tags": {"work"}, "notes": []}}
        >>> get_statistics(store)["total"]
        1
    """
    tag_counts = {}
    for rec in contacts.values():
        for tag in rec["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(
        tag_counts.items(), key=lambda pair: pair[1], reverse=True
    )
    return {"total": len(contacts), "top_tags": top_tags}


def save_to_json(contacts, path):
    """Save contacts to JSON, converting each tag set to a list.

    Sets are not JSON-serializable, so every contact's tag set is
    converted to a sorted list before writing.

    Args:
        contacts (dict): The contact store.
        path (str): Destination file path.

    Returns:
        bool: True on success, False on any I/O or type error.
    """
    try:
        serializable = {
            cid: {**rec, "tags": sorted(rec["tags"])}
            for cid, rec in contacts.items()
        }
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(serializable, handle, indent=2)
        return True
    except (OSError, TypeError) as error:
        print(f"Save failed: {error}")
        return False


def load_from_json(path):
    """Load contacts from JSON, converting tag lists back to sets.

    Args:
        path (str): Source file path.

    Returns:
        dict: The loaded store (empty dict on missing/corrupt file).
            Integer ids are restored and tags become sets again.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except FileNotFoundError:
        print("No saved file found; starting with an empty store.")
        return {}
    except json.JSONDecodeError as error:
        print(f"Corrupt JSON file: {error}")
        return {}

    restored = {}
    for cid, rec in raw.items():
        rec["tags"] = set(rec.get("tags", []))
        rec["notes"] = list(rec.get("notes", []))
        restored[int(cid)] = rec
    return restored


def _print_menu():
    """Print the numbered CLI menu options."""
    print("\n=== Contact Manager ===")
    print("1. Add contact")
    print("2. Search contacts")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Add tag")
    print("6. Find by tag")
    print("7. Statistics")
    print("8. Save to file")
    print("9. Load from file")
    print("0. Exit")


def run_menu(contacts=None, data_file="contacts.json"):
    """Run the interactive command-line menu loop.

    Args:
        contacts (dict, optional): Existing store; empty if None.
        data_file (str): JSON file used for the save/load options.
    """
    if contacts is None:
        contacts = {}

    while True:
        _print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_id = add_contact(
                contacts,
                input("Name: "),
                input("Phone: "),
                input("Email: "),
            )
            print(f"Added contact #{new_id}.")
        elif choice == "2":
            results = search_contacts(contacts, input("Query: "))
            for cid, rec in results.items():
                print(f"#{cid}: {rec['name']} | {rec['phone']}")
            if not results:
                print("No matches found.")
        elif choice == "3":
            cid = int(input("Contact id: "))
            ok = update_contact(contacts, cid, name=input("New name: "))
            print("Updated." if ok else "Id not found.")
        elif choice == "4":
            cid = int(input("Contact id: "))
            print("Deleted." if delete_contact(contacts, cid)
                  else "Id not found.")
        elif choice == "5":
            cid = int(input("Contact id: "))
            print("Tag added." if add_tag(contacts, cid, input("Tag: "))
                  else "Id not found.")
        elif choice == "6":
            results = find_by_tag(contacts, input("Tag: "))
            for cid, rec in results.items():
                print(f"#{cid}: {rec['name']}")
            if not results:
                print("No contacts with that tag.")
        elif choice == "7":
            stats = get_statistics(contacts)
            print(f"Total contacts: {stats['total']}")
            print(f"Top tags: {stats['top_tags']}")
        elif choice == "8":
            print("Saved." if save_to_json(contacts, data_file)
                  else "Save failed.")
        elif choice == "9":
            contacts = load_from_json(data_file)
            print(f"Loaded {len(contacts)} contacts.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


def main():
    """Entry point: load saved contacts, then run the menu."""
    contacts = load_from_json("contacts.json")
    run_menu(contacts)


if __name__ == "__main__":
    main()
