test_in=\
'''
Site,model,hostname,ip,os,group
Dallas,cat8400 ,r1,10.0.0.1,ios,routers
Dallas,asr1002,r2,10.0.0.2,ios,routers
Houston,cat9500,sw1,10.0.1.10,nxos,switches
'''

test_out=/
'''
all:
  children:
    sites:
      children:
        Dallas:
          hosts:
            r1:
              ansible_host: 10.0.0.1
              os: ios
              model: cat8400
            r2:
              ansible_host: 10.0.0.2
              os: ios
              model: asr1002
        Houston:
          hosts:
            sw1:
              ansible_host: 10.0.1.10
              os: nxos
              model: cat9500

    roles:
      children:
        routers:
          hosts:
            r1:
              ansible_host: 10.0.0.1
            r2:
              ansible_host: 10.0.0.2
        switches:
          hosts:
            sw1:
              ansible_host: 10.0.1.10

    models:
      children:
        cat8400:
          hosts:
            r1:
        asr1002:
          hosts:
            r2:
        cat9500:
          hosts:
            sw1:
'''


import csv
import yaml
from collections import defaultdict

def csv_to_ansible_inventory(csv_file):
    # Parent groups
    inventory = {
        "all": {
            "children": {
                "sites": {"children": {}},
                "roles": {"children": {}},
                "models": {"children": {}}
            }
        }
    }

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            site = row["Site"].strip()
            model = row["model"].strip()
            hostname = row["hostname"].strip()
            ip = row["ip"].strip()
            os = row["os"].strip()
            role = row["group"].strip()

            # Host variables
            host_vars = {
                "ansible_host": ip,
                "os": os,
                "model": model,
                "site": site
            }

            # --- SITE GROUPS ---
            sites_group = inventory["all"]["children"]["sites"]["children"]
            sites_group.setdefault(site, {"hosts": {}})
            sites_group[site]["hosts"][hostname] = host_vars

            # --- ROLE GROUPS ---
            roles_group = inventory["all"]["children"]["roles"]["children"]
            roles_group.setdefault(role, {"hosts": {}})
            roles_group[role]["hosts"][hostname] = {"ansible_host": ip}

            # --- MODEL GROUPS ---
            models_group = inventory["all"]["children"]["models"]["children"]
            models_group.setdefault(model, {"hosts": {}})
            models_group[model]["hosts"][hostname] = {}

    return yaml.dump(inventory, sort_keys=False)


# Example usage:
print(csv_to_ansible_inventory("devices.csv"))


