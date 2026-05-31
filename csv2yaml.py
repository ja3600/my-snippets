import csv
import yaml
from collections import defaultdict

def csv_to_ansible_inventory(csv_file, group_field="group"):
    inventory = defaultdict(lambda: {"hosts": {}})

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            hostname = row["hostname"]
            group = row[group_field]

            host_vars = {k: v for k, v in row.items()
                         if k not in ["hostname", group_field]}

            # ansible_host is the standard field
            if "ip" in host_vars:
                host_vars["ansible_host"] = host_vars.pop("ip")

            inventory[group]["hosts"][hostname] = host_vars

    return yaml.dump(dict(inventory), sort_keys=False)

# Example usage:
print(csv_to_ansible_inventory("devices.csv"))
