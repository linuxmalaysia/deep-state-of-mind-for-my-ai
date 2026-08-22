import os
import json
import re
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_plugin_json_exists_and_conforms():
    plugin_path = os.path.join(ROOT_DIR, "plugin.json")
    assert os.path.isfile(plugin_path), "plugin.json must exist at repository root"
    
    with open(plugin_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "$schema" in data, "plugin.json must have $schema"
    assert data["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert "name" in data, "plugin.json must have name"
    
    name = data["name"]
    assert 1 <= len(name) <= 64, "name must be between 1 and 64 chars"
    assert re.match(r"^[a-z0-9]([a-z0-9\.\-]*[a-z0-9])?$", name), "name must match character constraints"
    assert "--" not in name and ".." not in name, "name cannot contain consecutive hyphens or periods"
    
    if "extensions" in data:
        assert isinstance(data["extensions"], dict), "extensions must be a dictionary"
        for ns in data["extensions"].keys():
            assert "." in ns, f"extension namespace {ns} must follow reverse-domain format"

def test_mcp_json_exists_and_conforms():
    mcp_path = os.path.join(ROOT_DIR, "mcp.json")
    assert os.path.isfile(mcp_path), "mcp.json must exist at repository root"
    
    with open(mcp_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "$schema" in data, "mcp.json must have $schema"
    assert data["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    assert "mcpServers" in data, "mcp.json must contain mcpServers object"
    assert isinstance(data["mcpServers"], dict)
    
    for srv_name, srv in data["mcpServers"].items():
        assert "type" in srv, f"server {srv_name} must have a type"
        assert srv["type"] in ["stdio", "streamable-http", "sse"], f"server {srv_name} type must be a valid variant"
        if srv["type"] == "stdio":
            assert "command" in srv
            # Ensure no ${PLUGIN_ROOT} in command directly
            assert "${PLUGIN_ROOT}" not in srv["command"]

def test_governance_doc_registered():
    doc_path = os.path.join(ROOT_DIR, "docs", "governance", "DSOM-AGENT-PLUGINS-SPECIFICATION.md")
    assert os.path.isfile(doc_path), "DSOM-AGENT-PLUGINS-SPECIFICATION.md must exist"

def test_packager_skill_registered():
    skill_path = os.path.join(ROOT_DIR, ".agents", "skills", "agent-plugin-packager", "SKILL.md")
    assert os.path.isfile(skill_path), "agent-plugin-packager SKILL.md must exist"
