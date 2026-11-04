
import json
import sys
import xml.etree.ElementTree as ET

import yaml


class AuditInputError(Exception):
    """An inventory or policy cannot be read or used."""


class Device:
    def __init__(self, element):
        self.id = element.get("id")
        self.role = element.get("role")
        self.os = element.get("os")
        self.owner = (element.findtext("owner") or "").strip()
        self.interfaces = [
            item.get("status")
            for item in element.findall("interface")
        ]

    def count_down(self):
        return self.interfaces.count("down")


def version_parts(version):
    return tuple(int(part) for part in version.split("."))


def read_inputs(xml_path, yaml_path):
    try:
        root = ET.parse(xml_path).getroot()
    except (OSError, ET.ParseError) as error:
        raise AuditInputError(
            f"Could not read XML '{xml_path}': {error}"
        ) from error

    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            policy = yaml.safe_load(file)
    except (OSError, yaml.YAMLError) as error:
        raise AuditInputError(
            f"Could not read YAML '{yaml_path}': {error}"
        ) from error

    if not isinstance(policy, dict):
        raise AuditInputError(
            f"YAML '{yaml_path}' must contain a mapping"
        )

    if "min_os" in policy and not isinstance(policy["min_os"], dict):
        raise AuditInputError(
            f"YAML '{yaml_path}' key 'min_os' must contain a mapping"
        )

    return root, policy


def audit(root, policy):
    devices = [
        Device(element)
        for element in root.findall("device")
    ]

    kept = [device for device in devices if device.id]

    roles = {}
    interfaces = {"up": 0, "down": 0, "other": 0}
    violations = []
    compliant = []

    for device in kept:
        roles[device.role] = roles.get(device.role, 0) + 1

        for status in device.interfaces:
            group = status if status in ("up", "down") else "other"
            interfaces[group] += 1

        failed = False
        min_os = policy.get("min_os", {})

        if min_os and device.role not in min_os:
            violations.append({
                "device": device.id,
                "type": "unknown_role",
                "role": device.role
            })
            failed = True

        elif min_os:
            try:
                older = (
                    version_parts(device.os)
                    < version_parts(str(min_os[device.role]))
                )
            except (AttributeError, ValueError, TypeError) as error:
                raise AuditInputError(
                    f"Bad OS version for device '{device.id}': {error}"
                ) from error

            if older:
                violations.append({
                    "device": device.id,
                    "type": "os_outdated",
                    "found": device.os,
                    "required": str(min_os[device.role])
                })
                failed = True

        if policy.get("require_owner", False) and not device.owner:
            violations.append({
                "device": device.id,
                "type": "missing_owner"
            })
            failed = True

        if "max_down_interfaces" in policy:
            down = device.count_down()

            if down > policy["max_down_interfaces"]:
                violations.append({
                    "device": device.id,
                    "type": "too_many_down",
                    "down": down
                })
                failed = True

        if not failed:
            compliant.append(device.id)

    return {
        "site": root.get("site"),
        "total_devices": len(kept),
        "skipped_devices": len(devices) - len(kept),
        "roles": roles,
        "interfaces": interfaces,
        "violations": violations,
        "compliant": sorted(compliant)
    }


def main():
    if len(sys.argv) != 3:
        print(
            "usage: python pa2.py DEVICES.xml POLICY.yaml",
            file=sys.stderr
        )
        return 2

    try:
        root, policy = read_inputs(sys.argv[1], sys.argv[2])
        report = audit(root, policy)

        with open("audit.json", "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)

        print("Audit written to audit.json")
        print(
            f"Devices: {report['total_devices']}, "
            f"violations: {len(report['violations'])}"
        )

    except (AuditInputError, OSError, TypeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
